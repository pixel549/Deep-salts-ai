"""
CLI entrypoint.

Usage:
  python -m orchestrator.main turn          # run one turn
  python -m orchestrator.main end-session    # run the God/DM memory audit
"""

import sys

from orchestrator.turn_loop import run_turn
from orchestrator.session_end import run_session_end


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("turn", "end-session"):
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "turn":
        run_turn()
    elif sys.argv[1] == "end-session":
        run_session_end()


if __name__ == "__main__":
    main()
