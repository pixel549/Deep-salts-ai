"""
Load/save for every JSON state file, plus the append-only session log and a
thin git-commit helper. Nothing in here calls the API -- this is pure file
plumbing so turn_loop.py and session_end.py stay readable.
"""

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


def read_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def write_json(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def read_text(path: Path) -> str:
    with open(path) as f:
        return f.read()


def append_text(path: Path, text: str) -> None:
    with open(path, "a") as f:
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
