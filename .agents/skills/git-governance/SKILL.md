---
name: git-governance
description: Enforces branch naming, [TASK-XX:#NUM] conventional commits, standing flavor protection, and automated PR generation via scripts/create_pr.py.
---

# Git Governance Skill

Use this skill whenever creating a branch, committing changes, or opening a Pull Request.

## 1. Branch Creation Rules
- Check current branch (`git branch --show-current`) and verify it is NOT `main` before committing feature work.
- Create a task-bound branch matching `.githooks` and `scripts/lint_branch_and_commits.py`:
  - `feat/<task-id>-<kebab-desc>` (e.g., `feat/task-02-cv-pipeline`)
  - `fix/<task-id>-<kebab-desc>` (e.g., `fix/task-03-parquet-nulls`)
  - `docs/<task-id>-<kebab-desc>` or `chore/<desc>` for general maintenance.
- **Standing Flavor Protection**: Never open a PR or merge from `template/*` (e.g., `template/kaggle`) into `main`, `master`, or `develop`. Flavor sync is strictly one-way (`main` ➔ `template/*`).

## 2. Commit Message Protocol
- **Task-linked commit (Standard)**:
  `<type>(<scope>): [<TASK-ID>:#<ISSUE_NUM>] <lowercase description>`
  - Example: `feat(features): [TASK-02:#7] extract stylometric punctuation ratios`
- **Offline task commit (no `#NUM` yet)**:
  `<type>(<scope>): [<TASK-ID>] <lowercase description>`
- **Non-task maintenance commit (Reserved Tags)**:
  `<type>(<scope>): [<RESERVED_TAG>] <lowercase description>`
  - Valid Reserved Tags: `INFRA`, `CHORE`, `DOCS`, `FIX`, `HOTFIX`, `GLOBAL`, `CONFIG`, `SECURITY`, `COMMUNITY`, `DEPS`, `RELEASE`.
- Allowed `<type>`: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Note: `.githooks/prepare-commit-msg` prepends semantic emojis automatically; `.githooks/commit-msg` rejects commits whose `[TASK-ID]` lacks a matching `.github/issues/*<task-id>*` file.

## 3. Pull Request Creation & Role Boundary
1. Ensure `make audit` passes 100% locally.
2. Push branch to origin (`git push -u origin <branch>`).
3. Create or preview PR:
   ```bash
   python3 scripts/create_pr.py --dry-run
   make pr
   ```
4. Confirm `Resolves #<ISSUE_NUM>` is in the PR description.
5. **NEVER** run `git merge` into `main` or push directly to `main`. The repository owner (`RogerioLS`) reviews and merges PRs on GitHub.
