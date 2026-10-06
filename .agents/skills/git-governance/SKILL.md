---
name: git-governance
description: Enforces branch naming, conventional commit messages, and automated PR generation.
---

# Git Governance Skill

Use this skill to adhere to Clean Chassis git workflows:
1. Validate branch name matches `feat/`, `fix/`, or `chore/` conventions.
2. Ensure commit messages contain valid Conventional Commit tags and task numbers.
3. Generate pull requests with `python3 scripts/create_pr.py` ensuring linked issue references (`Closes #X`).
4. Remind that merging into `main` is strictly reserved for the repository owner.
