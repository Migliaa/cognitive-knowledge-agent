---
name: sdd-changelog
description: Update CHANGELOG.md before merging a feature branch. Summarizes the branch's commits and the feature spec in Keep a Changelog format.
---

# sdd-changelog

Update `CHANGELOG.md` for the current branch before it is merged.

## Steps

1. Run `git branch --show-current`. Stop if it is `main` or `master`.
2. Run `git log main..HEAD --format=%s` and `git diff main...HEAD --stat`.
3. Read `specs/features/<feature-name>/requirements.md` for the feature this branch implements.
4. If `CHANGELOG.md` does not exist, create it with the header
   `# Changelog` and the line `All notable changes follow [Keep a Changelog](https://keepachangelog.com/).`
5. Add entries under `## [Unreleased]`, grouped as `### Added`, `### Changed`, `### Fixed`,
   `### Removed`, `### Security`. Omit empty groups.
6. Write each entry as one line describing user-visible behavior, derived from the requirements
   and commits. Skip `chore:`, `test:`, and `docs:` commits unless they change behavior or
   developer workflow.
7. Do not duplicate entries already present. Do not rewrite released sections.
8. Commit only `CHANGELOG.md` as `docs: update changelog for <feature-name>`.

## Rules

- No marketing language, no commit hashes, no file lists.
- If the branch has no user-visible change, add nothing and say so.
