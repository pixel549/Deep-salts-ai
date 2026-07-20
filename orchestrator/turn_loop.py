"""
One full turn:
  load state -> GM sets scene -> Player A acts -> Player B acts ->
  (dice, if requested) -> GM resolves -> update world state -> log -> commit

Run directly: `python -m orchestrator.turn_loop`
"""

import json

from orchestrator import state, dice
from orchestrator.api_client import call_structured


def build_gm_scene_context(pub: dict, hidden: dict, gm_mem: str) -> str:
    return (
        f"Public state:\n{json.dumps(pub, indent=2)}\n\n"
        f"Hidden state (GM eyes only -- do not reveal unless a trigger fires):\n"
        f"{json.dumps(hidden, indent=2)}\n\n"
        f"Your private memory so far:\n{gm_mem}\n\n"
        f"Set the scene for this turn. Give both characters something to react to."
    )


def build_player_context(char_sheet: dict, player_mem: str, gm_narration: str) -> str:
    return (
        f"Your character sheet:\n{json.dumps(char_sheet, indent=2)}\n\n"
        f"Your private memory so far:\n{player_mem}\n\n"
        f"What just happened (GM narration, visible to both characters):\n{gm_narration}\n\n"
        f"Decide what your character does."
    )


def build_gm_resolution_context(
    pub: dict, hidden: dict, gm_mem: str, name_a: str, name_b: str,
    action_a: dict, action_b: dict, checks: dict,
) -> str:
    return (
        f"Public state:\n{json.dumps(pub, indent=2)}\n\n"
        f"Hidden state (GM eyes only):\n{json.dumps(hidden, indent=2)}\n\n"
        f"Your private memory so far:\n{gm_mem}\n\n"
        f"{name_a}'s action: {action_a['action']}\n"
        f"{name_b}'s action: {action_b['action']}\n\n"
        f"Dice results (already rolled, do not re-decide these): {json.dumps(checks, indent=2)}\n\n"
        f"Resolve this turn. Narrate the outcome. State any hp/inventory/location/flag "
        f"changes explicitly in public_state_deltas -- don't leave them implied in prose only. "
        f"Use each character's exact name as it appears above when naming them in deltas."
    )


def maybe_roll_check(char_sheet: dict, action: dict) -> dict | None:
    req = action.get("check_requested")
    if not req:
        return None
    skill = req["skill"]
    modifier = char_sheet["stats"]["skills"].get(skill, 0)
    dc = dice.default_dc_for(skill)
    result = dice.resolve_check(modifier, dc)
    return {"skill": skill, **result.as_dict()}


def apply_deltas(pub: dict, hidden: dict, deltas: dict, triggers_fired: list[str], char_by_name: dict) -> None:
    for change in deltas.get("hp_changes", []):
        key = char_by_name.get(change["character"])
        if not key:
            continue
        sheet = state.character(key)
        sheet["stats"]["hp"] = max(0, min(sheet["stats"]["max_hp"], sheet["stats"]["hp"] + change["delta"]))
        state.write_json(state.CHARACTERS / f"{key}.json", sheet)

    for change in deltas.get("inventory_changes", []):
        key = char_by_name.get(change["character"])
        if not key:
            continue
        sheet = state.character(key)
        if change["change"] == "add" and change["item"] not in sheet["inventory"]:
            sheet["inventory"].append(change["item"])
        elif change["change"] == "remove" and change["item"] in sheet["inventory"]:
            sheet["inventory"].remove(change["item"])
        state.write_json(state.CHARACTERS / f"{key}.json", sheet)

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

    name_a, name_b = char_a["name"], char_b["name"]
    char_by_name = {name_a: "character_a", name_b: "character_b"}

    session_no = pub["session_number"]
    pub["turn_number"] += 1

    # 1. GM sets the scene
    scene = call_structured(
        "gm", state.prompt("gm_system"),
        build_gm_scene_context(pub, hidden, gm_mem), "gm_scene",
    )
    state.append_session_log(session_no, f"GM (turn {pub['turn_number']}):\n{scene['narration']}")
    state.append_text(state.MEMORY / "gm" / "gm_memory.md", f"\n[turn {pub['turn_number']} notes] {scene['gm_private_notes']}\n")

    # 2. Players act, in parallel conceptually (sequential calls here for simplicity)
    action_a = call_structured(
        "player_a", state.prompt("player_system").format(character_name=name_a),
        build_player_context(char_a, mem_a, scene["narration"]), "player_action",
    )
    action_b = call_structured(
        "player_b", state.prompt("player_system").format(character_name=name_b),
        build_player_context(char_b, mem_b, scene["narration"]), "player_action",
    )

    state.append_session_log(session_no, f"{name_a}: {action_a['action']}")
    state.append_session_log(session_no, f"{name_b}: {action_b['action']}")
    state.append_text(state.MEMORY / "player_a" / "memory.md", f"\n[turn {pub['turn_number']}] I: {action_a['action']} ({action_a['private_reasoning']})\n")
    state.append_text(state.MEMORY / "player_b" / "memory.md", f"\n[turn {pub['turn_number']}] I: {action_b['action']} ({action_b['private_reasoning']})\n")

    # 3. Dice, if requested -- resolved in code, never by the model
    checks = {}
    roll_a = maybe_roll_check(char_a, action_a)
    if roll_a:
        checks[name_a] = roll_a
    roll_b = maybe_roll_check(char_b, action_b)
    if roll_b:
        checks[name_b] = roll_b

    # 4. GM resolves
    resolution = call_structured(
        "gm", state.prompt("gm_system"),
        build_gm_resolution_context(pub, hidden, gm_mem, name_a, name_b, action_a, action_b, checks),
        "gm_resolution",
    )

    apply_deltas(pub, hidden, resolution["public_state_deltas"], resolution["triggers_fired"], char_by_name)

    state.append_session_log(session_no, f"Outcome: {resolution['outcome_narration']}")
    if checks:
        state.append_session_log(session_no, f"Rolls: {json.dumps(checks)}")
    state.append_text(state.MEMORY / "gm" / "gm_memory.md", f"[turn {pub['turn_number']} resolution notes] {resolution['gm_private_notes']}\n")
    for key in ("player_a", "player_b"):
        state.append_text(state.MEMORY / key / "memory.md", f"[turn {pub['turn_number']}] What happened: {resolution['outcome_narration']}\n")

    # 5. Persist and commit
    state.write_json(state.WORLD / "public_state.json", pub)
    state.write_json(state.WORLD / "hidden_state.json", hidden)
    state.git_commit(f"session {session_no}, turn {pub['turn_number']}")


if __name__ == "__main__":
    run_turn()
