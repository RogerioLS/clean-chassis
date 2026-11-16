---
name: kanban-task-tracker
description: Creates local task specs in .github/issues/, resolves or creates GitHub Issues to capture #NUM for commit binding, and syncs kanban boards.
---

# Kanban Task Tracker Skill

Use this skill **before starting implementation** on any new feature, fix, or experiment so every commit and PR automatically binds to a valid Task ID and GitHub Issue `#NUM`.

## Step 1: Discover Existing Tasks & Issues
1. List local task specs:
   ```bash
   ls -1 .github/issues/
   ```
2. Query GitHub Issues (when `gh` CLI is authenticated):
   ```bash
   gh issue list --state all --limit 50 --json number,title,state
   ```
3. Determine the next sequential `TASK-XX` ID (e.g., `TASK-02`) or locate the existing issue for the requested work.

## Step 2: Create Local Task File (If New)
Create `.github/issues/task-XX-<short-kebab-slug>.md`:
```markdown
---
id: TASK-XX
title: "Concise Task Title"
area: core
type: feature
milestone: 1
---

## 🎯 Task Objective
Clear, verifiable goal of the task.

## 📋 Definition of Done
- [ ] First deliverable
- [ ] Automated tests passing (`make audit`)
- [ ] Documentation updated (`docs/status/PROJECT_STATUS.md`, etc.)
```

## Step 3: Create or Recover GitHub Issue `#NUM`
- **If the issue already exists on GitHub**: extract its integer `number` from `gh issue list --search "TASK-XX" --json number,title`.
- **If the issue does not exist yet**: create it from the local spec and capture the returned URL/number:
  ```bash
  gh issue create \
    --title "[TASK-XX] Concise Task Title" \
    --body-file .github/issues/task-XX-<short-kebab-slug>.md
  ```
- **Or** synchronize all defined milestones/tasks idempotently:
  ```bash
  python3 .github/scripts/setup_kanban.py
  ```
- **Bind the Issue Number Locally**: Add `github_issue: <ISSUE_NUM>` to the YAML frontmatter of `.github/issues/task-XX-<short-kebab-slug>.md`. This guarantees `scripts/create_pr.py` and `scripts/update_issue_checklist.py` resolve `Resolves #<ISSUE_NUM>` automatically.

## Step 4: Sync & Lifecycle Closure
- Pull issues created via GitHub Web UI into `.github/issues/` with:
  ```bash
  python3 scripts/sync_tasks.py
  ```
- Use `[TASK-XX:#<ISSUE_NUM>]` in every commit message and `Resolves #<ISSUE_NUM>` in the PR body. Upon CI `audit.yml` pass, `scripts/update_issue_checklist.py` automatically checks off `- [ ]` boxes and closes `#<ISSUE_NUM>`.
