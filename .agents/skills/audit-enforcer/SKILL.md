---
name: audit-enforcer
description: Validates repository health by running black, isort, flake8, ruff, bandit, pytest, and verifying generated audit artifacts.
---

# Audit Enforcer Skill

Use this skill before every commit, PR creation, or Kaggle dataset sync to ensure 100% Clean Chassis compliance.

## Tier 1 — Pre-Commit Sanity Check
Run fast formatting and lint checks:
```bash
make check
```
If formatting fails on modified Python files, apply formatters and re-verify:
```bash
black --line-length 100 src scripts tests
isort --profile black --line-length 100 src scripts tests
```

## Tier 2 — Full Quality Gate & Audit Certificate
Run the complete local audit suite:
```bash
make audit
```
Verify all of the following succeed with exit code `0`:
1. `python3 -m py_compile` across `src`, `tests`, `scripts`
2. `flake8 . --max-line-length=100` (excluding `.git,artifacts,.venv,venv,__pycache__,build,dist`)
3. `ruff check .`
4. `pytest` (100% passing, zero skipped/failing assertions)
5. `scripts/generate_summary.py` generates `summary.md` and `artifacts/audit_summary.json` with `"overall_passed": true`.

## Security Scan Check
When adding scripts, HTTP clients, or credential handling, verify Bandit reports zero High-severity findings:
```bash
python3 -m bandit -r src scripts -q
```
