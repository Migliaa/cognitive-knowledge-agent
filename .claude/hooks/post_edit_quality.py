import ast
import io
import json
import os
import re
import subprocess
import sys
import tokenize
from pathlib import Path

MAX_COMMENT_DENSITY = 0.05
FORBIDDEN_COMMENT = re.compile(
    r"noqa|type:\s*ignore|pyright:\s*ignore|\bhack\b|\bworkaround\b|\btemporary\b",
    re.IGNORECASE,
)


def run_module(module_args: list[str], cwd: Path) -> str | None:
    result = subprocess.run(
        [sys.executable, "-m", *module_args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return None
    return (result.stdout + result.stderr).strip()


def comment_problems(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    try:
        comments = [
            token
            for token in tokenize.generate_tokens(io.StringIO(source).readline)
            if token.type == tokenize.COMMENT
        ]
        tree = ast.parse(source)
    except (tokenize.TokenError, SyntaxError):
        return []

    problems = [
        f"{path.name}:{token.start[0]}: forbidden comment {token.string!r}"
        for token in comments
        if FORBIDDEN_COMMENT.search(token.string)
    ]

    code_lines = sum(1 for line in source.splitlines() if line.strip())
    if comments and code_lines and len(comments) / code_lines > MAX_COMMENT_DENSITY:
        density = len(comments) / code_lines
        problems.append(
            f"{path.name}: comment density {density:.1%} exceeds {MAX_COMMENT_DENSITY:.0%}; "
            "delete comments and express intent with names and types"
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
            if name == "sleep":
                problems.append(
                    f"{path.name}:{node.lineno}: sleep() is forbidden; wait on a condition"
                )
    return problems


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    raw_path = (payload.get("tool_input") or {}).get("file_path")
    if not raw_path or not str(raw_path).endswith(".py"):
        return 0
    path = Path(raw_path)
    if not path.is_file():
        return 0

    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or Path.cwd())
    failures: list[str] = []

    ruff_output = run_module(["ruff", "check", str(path)], root)
    if ruff_output:
        failures.append(f"ruff check failed:\n{ruff_output}")

    mypy_output = run_module(["mypy", str(path)], root)
    if mypy_output:
        failures.append(f"mypy failed:\n{mypy_output}")

    failures.extend(comment_problems(path))

    if failures:
        print("\n\n".join(failures), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
