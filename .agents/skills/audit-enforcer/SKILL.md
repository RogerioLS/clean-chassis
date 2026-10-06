---
name: audit-enforcer
description: Validates repository health, runs linter suite and executes full test audit.
---

# Audit Enforcer Skill

Use this skill to run and enforce Clean Chassis quality gates:
1. Run `make check` for fast sanity pre-commit linting.
2. Run `make audit` for syntax compilation, flake8 (100 columns), ruff, and pytest.
3. Verify that `summary.md` and `artifacts/audit_summary.json` reflect 100% compliance.
