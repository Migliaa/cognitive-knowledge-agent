import json
import os
import subprocess
import sys
from pathlib import Path

PROTECTED_BRANCHES = {"main", "master"}
CONSTITUTION = ("mission.md", "tech-stack.md", "roadmap.md")
FEATURE_FILES = ("plan.md", "requirements.md", "validation.md")


def current_branch(root: Path) -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def has_complete_feature(features_dir: Path) -> bool:
    if not features_dir.is_dir():
        return False
    return any(
        folder.is_dir() and all((folder / name).is_file() for name in FEATURE_FILES)
        for folder in features_dir.iterdir()
    )


def is_inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    raw_path = (payload.get("tool_input") or {}).get("file_path")
    if not raw_path:
        return 0

    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or Path.cwd())
    target = Path(raw_path)
    if not target.is_absolute():
        target = root / target
    if not is_inside(target, root / "src"):
        return 0

    problems: list[str] = []

    branch = current_branch(root)
    if branch in PROTECTED_BRANCHES:
        problems.append(
            f"You are on '{branch}'. Create a feature branch first: git switch -c feature/<name>"
        )

    missing = [name for name in CONSTITUTION if not (root / "specs" / name).is_file()]
    if missing:
        listing = ", ".join(f"specs/{name}" for name in missing)
        problems.append(f"Missing constitution files: {listing}. Write them before any code.")

    if not has_complete_feature(root / "specs" / "features"):
        problems.append(
            "No complete feature spec. Run the sdd-feature skill so that "
            "specs/features/<name>/ contains plan.md, requirements.md and validation.md."
        )

    if problems:
        message = "\n- ".join(problems)
        print(
            f"SDD guardrail: editing src/ is blocked.\n- {message}\n"
            "Disable this guardrail by removing the enforce-sdd.py entry from "
            ".claude/settings.json.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
