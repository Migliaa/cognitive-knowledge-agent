---
name: sdd-feature
description: Start a new feature the Spec-Driven way. Interviews the user on tradeoffs, then writes plan.md, requirements.md and validation.md under specs/features/<feature-name>/ and stops for human approval. Use before writing any code under src/.
---

# sdd-feature

Produce a three-file feature spec. Write no application code.

## Steps

1. **Check the branch.** Run `git branch --show-current`. If it is `main` or `master`, ask for a
   feature name and run `git switch -c feature/<feature-name>` (kebab-case). Stop if the working
   tree has unrelated uncommitted changes.
2. **Read the constitution.** Read `specs/mission.md`, `specs/tech-stack.md`, `specs/roadmap.md`.
   If any is missing, stop and tell the user to create the constitution first.
3. **Interview the user.** Ask about one decision at a time, with a recommendation for each:
   goal and non-goals, inputs and outputs, failure behavior, data and privacy limits,
   dependencies, and the tradeoff between at least two viable approaches. Do not proceed on
   assumptions; unanswered questions go in the plan as open questions.
4. **Write the spec** in `specs/features/<feature-name>/`:
   - `plan.md`: approach chosen, alternatives rejected and why, module and interface sketch,
     ordered implementation steps, risks, open questions.
   - `requirements.md`: numbered, testable requirements (`R1`, `R2`, ...) and an explicit
     out-of-scope list. Each requirement states observable behavior, not implementation.
   - `validation.md`: one row per requirement with the exact check that proves it (test name,
     command, or artifact) and the expected result.
5. **Stop.** Show the three file paths and a summary of the decisions. Ask for approval. Do not
   commit, do not implement. After approval: commit only the spec
   (`docs(spec): add <feature-name> feature spec`), then tell the user to run `/clear` before
   implementation.

## Rules

- Prose stays minimal; every line must change what gets built or tested.
- Requirements and validation must map one-to-one.
- Never create files under `src/` or `tests/` in this skill.
