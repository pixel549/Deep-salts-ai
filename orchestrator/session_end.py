"""
End-of-session pipeline:
  each agent writes a private recap
    -> God checks each recap against the PUBLIC session log only
       (confabulation = contradicts canon, leak = knows something it
       shouldn't -- never flags a belief just for differing from truth
       or from another agent's recap)
    -> DM (full-context GM) rules on each flag
    -> code strips DM's internal_reasoning immediately -- God, and the
       fix logs, never see it
    -> assertion-only corrections are appended directly to each agent's
       memory.md

Run directly: `python -m orchestrator.session_end`

Design note: we append corrections to memory.md as a plain text block
rather than asking the model to "rewrite its memory to incorporate this."
Letting a model freely rewrite its own memory in response to a correction
reopens the exact confabulation risk this pipeline exists to catch --
so the fix itself is deterministic, not generated.
"""

import json

from orchestrator import state
from orchestrator.api_client import call_structured

ROLES = ["gm", "player_a", "player_b"]


def write_recap(role: str, session_no: int) -> dict:
    if role == "gm":
        sheet_context = f"Your private memory:\n{state.gm_memory()}"
        prompt_name = "gm_system"
    else:
        char_key = "character_a" if role == "player_a" else "character_b"
        sheet_context = (
            f"Your character sheet:\n{json.dumps(state.character(char_key), indent=2)}\n\n"
            f"Your private memory:\n{state.player_memory(role)}"
        )
        prompt_name = "player_system"

    log_path = state.session_log_path(session_no)
    session_log_text = state.read_text(log_path) if log_path.exists() else "(no log entries)"

    system = state.prompt(prompt_name)
    if role != "gm":
        char_key = "character_a" if role == "player_a" else "character_b"
        system = system.format(character_name=state.character(char_key)["name"])

    user_content = (
        f"{sheet_context}\n\n"
        f"Full session log for reference:\n{session_log_text}\n\n"
        f"Write your end-of-session recap now."
    )

    recap = call_structured(role if role != "gm" else "gm", system, user_content, "session_recap")

    recap_dir = state.MEMORY / role / "recaps"
    recap_dir.mkdir(exist_ok=True)
    state.write_json(recap_dir / f"session_{session_no:03d}.json", recap)
    return recap


def get_god_flags(session_no: int, recaps: dict) -> dict:
    log_path = state.session_log_path(session_no)
    session_log_text = state.read_text(log_path) if log_path.exists() else "(no log entries)"

    user_content = (
        f"Public session log (ground truth for 'what happened'):\n{session_log_text}\n\n"
        f"Recaps to audit:\n{json.dumps(recaps, indent=2)}\n\n"
        f"Produce your flag report now."
    )
    flags = call_structured("god", state.prompt("god_system"), user_content, "god_flag_report")

    dm_review_dir = state.MEMORY / "dm_review"
    dm_review_dir.mkdir(exist_ok=True)
    state.write_json(dm_review_dir / f"session_{session_no:03d}_flags.json", flags)
    return flags


def get_dm_rulings(session_no: int, flags: dict, recaps: dict) -> dict:
    """DM sees everything -- full hidden state, all secrets, all recaps -- to make the call."""
    context = (
        f"Flags from God:\n{json.dumps(flags, indent=2)}\n\n"
        f"All three recaps (full context, you're omniscient):\n{json.dumps(recaps, indent=2)}\n\n"
        f"Hidden state:\n{json.dumps(state.hidden_state(), indent=2)}\n\n"
        f"Character A sheet: {json.dumps(state.character('character_a'), indent=2)}\n"
        f"Character B sheet: {json.dumps(state.character('character_b'), indent=2)}\n\n"
        f"Rule on each flag now."
    )
    rulings = call_structured(
        "dm_adjudication", state.prompt("dm_adjudication_system"), context, "dm_adjudication"
    )

    dm_review_dir = state.MEMORY / "dm_review"
    dm_review_dir.mkdir(exist_ok=True)
    # NOTE: this file contains internal_reasoning and is DM/God eyes only.
    # It must never be the source agents read from -- see build_fix_logs().
    state.write_json(dm_review_dir / f"session_{session_no:03d}_rulings.json", rulings)
    return rulings


def build_fix_logs(rulings: dict) -> dict:
    """
    Strip internal_reasoning in code, not in a prompt. This is the actual
    firewall -- it holds even if a model call skips its own instructions.
    """
    fix_logs = {role: [] for role in ROLES}
    for ruling in rulings.get("rulings", []):
        target = ruling["target_agent"]
        if target in fix_logs:
            fix_logs[target].append(ruling["instruction"])
    return fix_logs


def apply_fix_logs(session_no: int, fix_logs: dict) -> None:
    for role, instructions in fix_logs.items():
        if not instructions:
            continue

        fix_log_dir = state.MEMORY / role / "fix_logs"
        fix_log_dir.mkdir(exist_ok=True)
        state.write_json(
            fix_log_dir / f"session_{session_no:03d}.json",
            {"for_agent": role, "instructions": instructions},
        )

        mem_path = state.MEMORY / role / "memory.md"
        block = f"\n## Corrections (session {session_no:03d})\n"
        for instruction in instructions:
            block += f"- {instruction}\n"
        state.append_text(mem_path, block)


def run_session_end() -> None:
    pub = state.public_state()
    session_no = pub["session_number"]

    recaps = {role: write_recap(role, session_no) for role in ROLES}
    flags = get_god_flags(session_no, recaps)

    if flags.get("flags"):
        rulings = get_dm_rulings(session_no, flags, recaps)
        fix_logs = build_fix_logs(rulings)
        apply_fix_logs(session_no, fix_logs)
    else:
        print(f"No flags for session {session_no} -- nothing to adjudicate.")

    # Roll over to the next session
    pub["session_number"] += 1
    pub["turn_number"] = 0
    state.write_json(state.WORLD / "public_state.json", pub)
    state.git_commit(f"session {session_no} end-of-session review")


if __name__ == "__main__":
    run_session_end()
