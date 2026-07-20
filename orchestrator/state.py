"""
Load/save for every JSON state file, plus the append-only session log and a
thin git-commit helper. Nothing in here calls the API -- this is pure file
plumbing so turn_loop.py and session_end.py stay readable.
"""

# Every open() below pins encoding="utf-8" explicitly. Without it, Python
# falls back to the OS locale encoding -- cp1252 on most Windows setups --
# and this project writes/reads a LOT of LLM-generated prose full of em
# dashes and curly quotes. Those get written in one encoding and can get
# misread as another downstream (e.g. by whatever ingests the session log
# next), which is exactly what produces mangled "�" replacement characters
# in session_NNN.md. Pinning utf-8 here makes the files correct regardless
# of what OS or locale this runs under -- Windows laptop, GitHub Actions
# ubuntu-latest runner, whatever.

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORLD = ROOT / "world"
CHARACTERS = ROOT / "characters"
MEMORY = ROOT / "memory"
SESSIONS = ROOT / "sessions"
PROMPTS = ROOT / "prompts"
RULES = ROOT / "rules"
ENCOUNTER_PATH = WORLD / "encounter_state.json"

_DEFAULT_ENCOUNTER_STATE = {
    "active": False,
    "monster": None,
    # Insanity/Influence saves the GM flagged last turn (saves_triggered),
    # already rolled by the orchestrator using the pre-turn track value.
    # Surfaced into the next GM scene context, then cleared.
    "pending_save_results": [],
}


def read_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def read_text(path: Path) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def append_text(path: Path, text: str) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


# --- convenience accessors -------------------------------------------------

def public_state() -> dict:
    return read_json(WORLD / "public_state.json")


def hidden_state() -> dict:
    return read_json(WORLD / "hidden_state.json")


def character(name: str) -> dict:
    return read_json(CHARACTERS / f"{name}.json")


def player_memory(player_key: str) -> str:
    return read_text(MEMORY / player_key / "memory.md")


def gm_memory() -> str:
    return read_text(MEMORY / "gm" / "gm_memory.md")


def prompt(name: str) -> str:
    return read_text(PROMPTS / f"{name}.md")


def ruleset_text() -> str:
    """The actual Deep Salts ruleset (rules/deep-salts-v8.1.md), loaded
    verbatim into the GM's context. See gm_system.md for how it's used."""
    return read_text(RULES / "deep-salts-v8.1.md")


def encounter_state() -> dict:
    """No active encounter is the default/normal state -- return that
    rather than erroring if the file hasn't been created yet."""
    if not ENCOUNTER_PATH.exists():
        return dict(_DEFAULT_ENCOUNTER_STATE)
    return read_json(ENCOUNTER_PATH)


def write_encounter_state(data: dict) -> None:
    write_json(ENCOUNTER_PATH, data)


def clear_encounter_state() -> None:
    write_encounter_state(dict(_DEFAULT_ENCOUNTER_STATE))


def session_log_path(session_number: int) -> Path:
    return SESSIONS / f"session_{session_number:03d}.md"


def append_session_log(session_number: int, entry: str) -> None:
    SESSIONS.mkdir(exist_ok=True)
    path = session_log_path(session_number)
    ts = datetime.now(timezone.utc).isoformat()
    append_text(path, f"\n---\n[{ts}]\n{entry}\n")


def git_commit(message: str) -> None:
    """
    Commit whatever's currently changed in the repo. No-ops quietly if
    there's nothing to commit or this isn't a git repo yet -- intended to
    run inside CI or a local repo you've already `git init`'d.
    """
    try:
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 and "nothing to commit" not in result.stdout:
            print(f"git commit warning: {result.stdout} {result.stderr}")
    except FileNotFoundError:
        print("git not available -- skipping commit")
    except subprocess.CalledProcessError as e:
        print(f"git add failed: {e}")
