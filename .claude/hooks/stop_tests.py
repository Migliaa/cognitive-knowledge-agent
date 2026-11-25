import json
import os
import subprocess
import sys
from pathlib import Path

TAIL_LINES = 60


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}

    if payload.get("stop_hook_active"):
        return 0

    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or Path.cwd())

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if not status.stdout.strip():
        return 0

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-x", "-q"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return 0

    tail = "\n".join((result.stdout + result.stderr).strip().splitlines()[-TAIL_LINES:])
    print(f"pytest -x -q failed; fix before stopping:\n{tail}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
