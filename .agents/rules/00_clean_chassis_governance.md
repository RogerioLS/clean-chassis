# 00 — Clean Chassis Governance & Boundaries

1. **Owner Authority**: All PR merges into `main` are exclusively performed by the repository owner (`RogerioLS`).
2. **Never Merge into `main`**: Autonomous agents must NEVER run `git merge` into `main` or push directly to `main`.
3. **Standing Flavor Protection**: Branches prefixed with `template/*` (such as `template/kaggle`) are specialized downstream flavors. Merges are strictly one-way (`main` ➔ `template/*`). Never open a PR or merge from `template/*` into `main`, `master`, or `develop`.
4. **PR-Driven Flow**: Work in dedicated task branches (`<type>/<task-id>-<desc>`). Once `make audit` passes 100%, push the branch and open a PR via `make pr` (`python3 scripts/create_pr.py`).
5. **Mandatory Issue Linkage**: Every feature/fix PR must resolve a real GitHub Issue (`Resolves #<ISSUE_NUM>` or `Closes #<ISSUE_NUM>`) so CI automatically checks off checklists and closes the issue upon audit pass.
