---
name: kanban-task-tracker
description: Manages project tasks, milestones, and automatic issue checklist synchronization.
---

# Kanban Task Tracker Skill

Use this skill to synchronize issues and track progress:
1. Use `scripts/sync_tasks.py` to pull issues from GitHub into local Markdown files.
2. Link issues in PRs to ensure `scripts/update_issue_checklist.py` automatically marks checklists and closes tasks upon audit success.
