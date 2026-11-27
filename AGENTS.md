# AGENTS.md

Constraints are enforced by tooling, not prose. If a rule below is violated, a hook or linter
fails. Fix the cause; never route around the check.

## Commands

- Lint: `.venv/Scripts/ruff check .` and `.venv/Scripts/ruff format --check .`
- Types: `.venv/Scripts/mypy`
- Tests: `.venv/Scripts/pytest -x -q`
- All three must pass before a task is done.

## Layout

- `src/cognitive_agent/{ingestion,processing,agent}/` application code
- `tests/` pytest suite
- `specs/` constitution (`mission.md`, `tech-stack.md`, `roadmap.md`) and `specs/features/<name>/`
- `docs/adr/` architecture decision records
- `.claude/` hooks, skills, review agents

## Forbidden workarounds

- No `# noqa`, `# type: ignore`, `# pyright: ignore`, `# fmt: off`.
- No `sleep()` / `time.sleep()` / `asyncio.sleep()` to hide races or wait for state; wait on a
  condition or fix the ordering.
- No bare `except:` or `except Exception:` that swallows errors.
- No comments tagged `hack`, `workaround`, `temporary`.
- No weakening of lint, type, or test config to make a failure disappear.
- No deleting or skipping a failing test to get green.

## Comments

Target near-zero comments (hook limit: 5% of lines). Express intent with names, types, and small
functions. A comment is allowed only for a non-obvious *why* that code cannot carry.

## Gardening Rule

When the same mistake is made or corrected twice, do not add prose here. Encode it as a ruff
rule, a mypy setting, a test, or a hook in `.claude/hooks/`, then commit it with the fix.

## Spec-Driven Development

1. Work on a feature branch, never on `main` or `master`.
2. Interview the user about tradeoffs, then write `specs/features/<name>/{plan,requirements,validation}.md`.
3. Commit the spec alone and stop for human approval.
4. Run `/clear` so implementation starts from the spec, not from the conversation.
5. Implement against `validation.md`; every acceptance criterion maps to a test or an artifact.
6. Run `sdd-changelog` before merge.

`.claude/hooks/enforce-sdd.py` blocks `src/` edits via `Edit`/`Write` only (not shell writes). It
checks that spec files exist, not commit or approval; one complete spec unlocks all later features.

## Review

Before opening a PR, run the `security-reviewer` and `pattern-reviewer` agents. Fill every
section of `.github/pull_request_template.md`.

## Git

- Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`).
- One logical change per commit. PRs reference an issue with `Closes #<n>`.
- Never commit secrets, `.env`, or tokens. Read credentials from environment variables.
