# 00 — Clean Chassis Governance & Boundaries

1. **Owner Authority**: All PR merges into `main` are exclusively performed by the repository owner (`RogerioLS`).
2. **Never Merge into `main`**: Autonomous agents must NEVER run `git merge` into `main` or push directly to `main`.
3. **PR-Driven Flow**: Work in dedicated feature branches (`feat/<task-id>-<desc>`). Once `make audit` passes 100%, push branch and open a PR via `scripts/create_pr.py`.
4. **Issue Linkage**: Every PR must include `Resolves #<ID>` or `Closes #<ID>` to trigger automatic issue checklist closure upon merge.
