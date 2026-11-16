# 03 — Git Workflow, Task Creation & Commit Governance

Never ask the user to remind you of the task/commit workflow. Follow this sequence automatically:

## 1. Task & GitHub Issue Creation (Before Coding or Committing)
1. **Inspect Existing Tasks**: Check `.github/issues/` and run `gh issue list --state all --limit 50` (if `gh` is available) to see the next sequential `TASK-XX` ID and whether a GitHub Issue already exists.
2. **Create Local Task Spec**: If no file exists in `.github/issues/` for the task, create `.github/issues/task-XX-<short-slug>.md` with YAML frontmatter (`id: TASK-XX`, `title`, `area`, `type`, `milestone`, and `github_issue: <NUM>` once created), `## 🎯 Task Objective`, and `## 📋 Definition of Done` checkboxes (`- [ ] ...`).
3. **Create / Recover GitHub Issue `#NUM`**:
   - Create the issue via `gh issue create --title "[TASK-XX] <Title>" --body-file .github/issues/task-XX-<short-slug>.md` (or `python3 .github/scripts/setup_kanban.py`), **or** query `gh issue list --search "TASK-XX" --json number,title` to retrieve the exact `#ISSUE_NUM`.
   - Record `github_issue: <ISSUE_NUM>` in the `.github/issues/task-XX-<short-slug>.md` frontmatter so `scripts/create_pr.py` binds them automatically.
   - If working offline without GitHub API access, still create `.github/issues/task-XX-<short-slug>.md` so `.githooks/commit-msg` passes, and bind `#ISSUE_NUM` before opening the PR.

## 2. Branch Naming
- Standard task branches: `<type>/<task-id>-<kebab-description>` (e.g., `feat/task-02-cv-harness`, `fix/task-03-parquet-schema`, `docs/task-04-eda-report`).
- General branches without task ID: `<type>/<kebab-description>` (e.g., `chore/infra-kaggle-sync`).
- Allowed `<type>`: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

## 3. Commit Message Format
- **With Task & Issue (Mandatory for task work)**:
  `<type>(<scope>): [<TASK-ID>:#<ISSUE_NUM>] <lowercase concise description>`
  - Example: `feat(cv): [TASK-02:#7] implement stratified group k-fold split`
- **With Local Task Only (offline fallback)**:
  `<type>(<scope>): [<TASK-ID>] <lowercase concise description>`
- **With Reserved Tag (non-task infra/docs/maintenance)**:
  `<type>(<scope>): [<RESERVED_TAG>] <lowercase concise description>`
  - Allowed Reserved Tags: `[INFRA]`, `[CHORE]`, `[DOCS]`, `[FIX]`, `[HOTFIX]`, `[GLOBAL]`, `[CONFIG]`, `[SECURITY]`, `[COMMUNITY]`, `[DEPS]`, `[RELEASE]`.
- Note: `.githooks/prepare-commit-msg` automatically prepends the semantic emoji (`✨`, `🐛`, `📝`, `🔧`, etc.); do not duplicate emojis manually unless intentional.

## 4. Pull Requests
- Always create/update PRs with `make pr` (`python3 scripts/create_pr.py`).
- Verify `Resolves #<ISSUE_NUM>` is present in the PR body before requesting owner review.
