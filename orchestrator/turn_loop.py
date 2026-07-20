"""
One full turn:
  load state -> GM sets scene -> Player A acts -> Player B acts ->
  (skill checks / combat actions, resolved in dice.py, never by a model) ->
  GM resolves -> update world state -> log -> commit

Run directly: `python -m orchestrator.turn_loop`
"""

import json

from orchestrator import state, dice
from orchestrator.api_client import call_structured


def gm_system_prompt() -> str:
    """The GM's system prompt plus the actual Deep Salts ruleset appended
    verbatim -- the ruleset is static reference material, not per-turn
    state, so it belongs in the system prompt rather than rebuilt into
    every context string."""
    return (
        state.prompt("gm_system")
        + "\n\n---\n\n# THE ACTUAL RULESET (reference -- follow this, don't improvise around it)\n\n"
        + state.ruleset_text()
    )


def build_gm_scene_context(pub: dict, hidden: dict, gm_mem: str, encounter: dict) -> str:
    parts = [
        f"Public state:\n{json.dumps(pub, indent=2)}\n",
        f"Hidden state (GM eyes only -- do not reveal unless a trigger fires):\n{json.dumps(hidden, indent=2)}\n",
        f"Your private memory so far:\n{gm_mem}\n",
    ]
    if encounter.get("active"):
        parts.append(f"Active encounter (ground truth, narrate consistently with these numbers):\n{json.dumps(encounter['monster'], indent=2)}\n")
    if encounter.get("pending_save_results"):
        parts.append(
            f"Save rolls from last turn's resolution, now resolved -- narrate their consequence "
            f"as this scene opens (fail = a real moment of losing composure/control, not a full "
            f"scripted override): {json.dumps(encounter['pending_save_results'], indent=2)}\n"
        )
    parts.append("Set the scene for this turn. Give both characters something to react to.")
    return "\n".join(parts)


def build_player_context(char_sheet: dict, player_mem: str, gm_narration: str, encounter: dict) -> str:
    parts = [
        f"Your character sheet:\n{json.dumps(char_sheet, indent=2)}\n",
        f"Your private memory so far:\n{player_mem}\n",
        f"What just happened (GM narration, visible to both characters):\n{gm_narration}\n",
    ]
    if encounter.get("active"):
        parts.append(
            f"There is an active hostile encounter:\n{json.dumps(encounter['monster'], indent=2)}\n"
            f"If you want to fight it, declare a combat_action (attack/parry_attempt/called_shot/"
            f"ambush_called_shot) rather than a check_requested -- combat is resolved differently."
        )
    parts.append("Decide what your character does.")
    return "\n".join(parts)


def build_gm_resolution_context(
    pub: dict, hidden: dict, gm_mem: str, name_a: str, name_b: str,
    action_a: dict, action_b: dict, checks: dict, combat_results: dict, encounter: dict,
) -> str:
    parts = [
        f"Public state:\n{json.dumps(pub, indent=2)}\n",
        f"Hidden state (GM eyes only):\n{json.dumps(hidden, indent=2)}\n",
        f"Your private memory so far:\n{gm_mem}\n",
        f"{name_a}'s action: {action_a['action']}\n",
        f"{name_b}'s action: {action_b['action']}\n",
    ]
    if checks:
        parts.append(f"Skill check results (already rolled, do not re-decide these): {json.dumps(checks, indent=2)}\n")
    if combat_results:
        parts.append(
            f"Combat results (already resolved AND already applied to HP/limbs/monster state -- "
            f"do not add these to hp_changes/limb_effects again, only narrate them; use "
            f"hp_changes/limb_effects for anything ELSE this turn, e.g. a hazard or the monster's "
            f"own attack): {json.dumps(combat_results, indent=2)}\n"
        )
    if encounter.get("active"):
        parts.append(f"Current encounter state, after combat above was applied:\n{json.dumps(encounter['monster'], indent=2)}\n")
    parts.append(
        "Resolve this turn. Narrate the outcome. State any inventory/location/flag/insight/status-track "
        "changes explicitly in public_state_deltas -- don't leave them implied in prose only. "
        "Use each character's exact name as it appears above when naming them in deltas."
    )
    return "\n".join(parts)


def maybe_roll_check(char_sheet: dict, action: dict) -> dict | None:
    """Section 3 'genuinely uncertain' checks only. Skipped entirely if a
    combat_action was declared instead -- see maybe_resolve_combat."""
    req = action.get("check_requested")
    if not req or action.get("combat_action"):
        return None
    skill = req["skill"]
    governing_attr = dice.SKILL_ATTRIBUTE_MAP.get(skill, "resolve")
    modifier = dice.attribute_modifier(char_sheet["attributes"][governing_attr])
    dc = dice.default_dc_for(skill)
    result = dice.resolve_check(modifier, dc)
    return {"skill": skill, "governing_attribute": governing_attr, **result.as_dict()}


def maybe_resolve_combat(char_sheet: dict, action: dict, encounter: dict) -> dict | None:
    """Resolves a declared combat_action against the active encounter's
    monster, then applies its HP/limb/stagger/sever effects directly to
    state (monster in `encounter`, mutated in place; the caller writes it
    back). Returns the result for logging/GM narration context."""
    combat = action.get("combat_action")
    if not combat:
        return None
    if not encounter.get("active") and combat["type"] != "parry_attempt":
        # No monster to hit -- nothing to resolve. (parry_attempt with no
        # monster falls through to the default-tolerance path below, though
        # normally the GM shouldn't be offering a parry with nothing to parry.)
        return {"type": combat["type"], "note": "No active encounter -- action had no target, ignored."}

    monster = encounter.get("monster")
    result = dice.resolve_combat_action(
        char_sheet, combat["type"], combat.get("swing"), combat.get("target_limb"), monster,
    )

    # Apply effects directly rather than trusting the GM to restate them --
    # see gm_resolution_context's instruction not to double-count these.
    if monster is not None:
        hit = result.get("limb_hit")
        if hit:
            monster["hp"] = hit["hp_after"]
            limb_key = hit["limb"]
            monster["limbs"][limb_key]["stagger_meter"] = hit["new_stagger_meter"]
            if hit["sever"]:
                monster["limbs"][limb_key]["severed"] = True
    if result.get("damage_taken"):
        char_sheet["hp"] = max(0, char_sheet["hp"] - result["damage_taken"])

    return result


def apply_deltas(pub: dict, hidden: dict, deltas: dict, triggers_fired: list[str],
                  char_by_name: dict, encounter: dict) -> None:
    monster_name = encounter["monster"]["name"] if encounter.get("active") else None

    for change in deltas.get("hp_changes", []):
        if monster_name and change["character"] == monster_name:
            encounter["monster"]["hp"] = max(0, min(encounter["monster"]["max_hp"], encounter["monster"]["hp"] + change["delta"]))
            continue
        key = char_by_name.get(change["character"])
        if not key:
            continue
        sheet = state.character(key)
        sheet["hp"] = max(0, min(sheet["max_hp"], sheet["hp"] + change["delta"]))
        state.write_json(state.CHARACTERS / f"{key}.json", sheet)

    for change in deltas.get("inventory_changes", []):
        key = char_by_name.get(change["character"])
        if not key:
            continue
        sheet = state.character(key)
        names = [item["name"] for item in sheet["inventory"]]
        if change["change"] == "add" and change["item"] not in names:
            sheet["inventory"].append({"name": change["item"], "durability": "constant", "uses_remaining": None})
        elif change["change"] == "remove" and change["item"] in names:
            sheet["inventory"] = [i for i in sheet["inventory"] if i["name"] != change["item"]]
        state.write_json(state.CHARACTERS / f"{key}.json", sheet)

    for change in deltas.get("limb_effects", []):
        if monster_name and change["character"] == monster_name:
            limb = encounter["monster"]["limbs"].get(change["limb"])
            if limb and change["effect"] == "severed":
                limb["severed"] = True
            continue
        key = char_by_name.get(change["character"])
        if not key:
            continue
        sheet = state.character(key)
        limb = sheet["limbs"].get(change["limb"])
        if limb and change["effect"] == "severed":
            limb["severed"] = True
        state.write_json(state.CHARACTERS / f"{key}.json", sheet)

    for change in deltas.get("status_track_changes", []):
        key = char_by_name.get(change["character"])
        if not key:
            continue
        sheet = state.character(key)
        track = change["track"]
        cap = 10 if track in ("blood_loss", "insanity") else (5 if track == "corrosion" else None)
        new_val = sheet["tracks"][track] + change["delta"]
        sheet["tracks"][track] = max(0, min(cap, new_val)) if cap is not None else max(0, new_val)
        state.write_json(state.CHARACTERS / f"{key}.json", sheet)

    for change in deltas.get("insight_changes", []):
        key = char_by_name.get(change["character"])
        if not key:
            continue
        sheet = state.character(key)
        sheet["insight"] = max(0, sheet["insight"] + change["delta"])
        state.write_json(state.CHARACTERS / f"{key}.json", sheet)

    if deltas.get("monster_spawned") and not encounter.get("active"):
        spawn = deltas["monster_spawned"]
        player_level = 1  # leveling isn't mechanized yet -- see build notes
        encounter["monster"] = dice.spawn_monster(spawn["archetype"], player_level, spawn.get("name"))
        encounter["active"] = True

    if deltas.get("encounter_ended"):
        encounter["active"] = False
        encounter["monster"] = None

    new_pending_saves = []
    for save_req in deltas.get("saves_triggered", []):
        key = char_by_name.get(save_req["character"])
        if not key:
            continue
        sheet = state.character(key)
        result = dice.insanity_influence_save(
            track_value=sheet["tracks"][save_req["track"]],
            resolve=sheet["attributes"]["resolve"],
            insight=sheet["insight"],
            situational_mod=save_req.get("situational_mod", 0),
        )
        new_pending_saves.append({"character": save_req["character"], "track": save_req["track"],
                                   "reason": save_req["reason"], **result.as_dict()})
    encounter["pending_save_results"] = new_pending_saves

    if deltas.get("location"):
        pub["location"] = deltas["location"]

    for flag in deltas.get("flags_set", []):
        if flag not in pub["flags_set"]:
            pub["flags_set"].append(flag)

    existing_npc_names = {npc["name"] for npc in pub["known_npcs"]}
    for npc in deltas.get("npcs_revealed", []):
        if npc["name"] not in existing_npc_names:
            pub["known_npcs"].append(npc)
            existing_npc_names.add(npc["name"])

    for trigger_id in triggers_fired:
        for t in hidden["triggers"]:
            if t["id"] == trigger_id:
                t["fired"] = True


def run_turn() -> None:
    pub = state.public_state()
    hidden = state.hidden_state()
    gm_mem = state.gm_memory()
    char_a = state.character("character_a")
    char_b = state.character("character_b")
    mem_a = state.player_memory("player_a")
    mem_b = state.player_memory("player_b")
    encounter = state.encounter_state()

    name_a, name_b = char_a["name"], char_b["name"]
    char_by_name = {name_a: "character_a", name_b: "character_b"}

    session_no = pub["session_number"]
    pub["turn_number"] += 1

    # 1. GM sets the scene
    scene = call_structured(
        "gm", gm_system_prompt(),
        build_gm_scene_context(pub, hidden, gm_mem, encounter), "gm_scene",
    )
    state.append_session_log(session_no, f"GM (turn {pub['turn_number']}):\n{scene['narration']}")
    state.append_text(state.MEMORY / "gm" / "gm_memory.md", f"\n[turn {pub['turn_number']} notes] {scene['gm_private_notes']}\n")
    encounter["pending_save_results"] = []  # surfaced above, now consumed

    # 2. Players act
    action_a = call_structured(
        "player_a", state.prompt("player_system").format(character_name=name_a),
        build_player_context(char_a, mem_a, scene["narration"], encounter), "player_action",
    )
    action_b = call_structured(
        "player_b", state.prompt("player_system").format(character_name=name_b),
        build_player_context(char_b, mem_b, scene["narration"], encounter), "player_action",
    )

    state.append_session_log(session_no, f"{name_a}: {action_a['action']}")
    state.append_session_log(session_no, f"{name_b}: {action_b['action']}")
    state.append_text(state.MEMORY / "player_a" / "memory.md", f"\n[turn {pub['turn_number']}] I: {action_a['action']} ({action_a['private_reasoning']})\n")
    state.append_text(state.MEMORY / "player_b" / "memory.md", f"\n[turn {pub['turn_number']}] I: {action_b['action']} ({action_b['private_reasoning']})\n")

    # 3. Skill checks and combat -- resolved in code, never by the model
    checks = {}
    roll_a = maybe_roll_check(char_a, action_a)
    if roll_a:
        checks[name_a] = roll_a
    roll_b = maybe_roll_check(char_b, action_b)
    if roll_b:
        checks[name_b] = roll_b

    combat_results = {}
    combat_a = maybe_resolve_combat(char_a, action_a, encounter)
    if combat_a:
        combat_results[name_a] = combat_a
    combat_b = maybe_resolve_combat(char_b, action_b, encounter)
    if combat_b:
        combat_results[name_b] = combat_b
    if combat_a or combat_b:
        # Combat mutated char_a/char_b/encounter['monster'] in place above --
        # persist those before the GM resolution call sees them.
        state.write_json(state.CHARACTERS / "character_a.json", char_a)
        state.write_json(state.CHARACTERS / "character_b.json", char_b)

    # 4. GM resolves
    resolution = call_structured(
        "gm", gm_system_prompt(),
        build_gm_resolution_context(pub, hidden, gm_mem, name_a, name_b, action_a, action_b, checks, combat_results, encounter),
        "gm_resolution",
    )

    apply_deltas(pub, hidden, resolution["public_state_deltas"], resolution["triggers_fired"], char_by_name, encounter)

    state.append_session_log(session_no, f"Outcome: {resolution['outcome_narration']}")
    if checks:
        state.append_session_log(session_no, f"Checks: {json.dumps(checks)}")
    if combat_results:
        state.append_session_log(session_no, f"Combat: {json.dumps(combat_results)}")
    state.append_text(state.MEMORY / "gm" / "gm_memory.md", f"[turn {pub['turn_number']} resolution notes] {resolution['gm_private_notes']}\n")
    for key in ("player_a", "player_b"):
        state.append_text(state.MEMORY / key / "memory.md", f"[turn {pub['turn_number']}] What happened: {resolution['outcome_narration']}\n")

    # 5. Persist and commit
    state.write_json(state.WORLD / "public_state.json", pub)
    state.write_json(state.WORLD / "hidden_state.json", hidden)
    state.write_encounter_state(encounter)
    state.git_commit(f"session {session_no}, turn {pub['turn_number']}")


if __name__ == "__main__":
    run_turn()
