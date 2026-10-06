# 04 — Testing & Quality Gates

1. **Two-Tier Quality Gates**:
   - Tier 1: `make check` (fast local pre-commit linting).
   - Tier 2: `make audit` (complete audit: py_compile, flake8, ruff, pytest, summary.md).
2. **No Regression**: Code changes must never break existing unit or integration tests.
3. **Coverage Standard**: Target 100% test pass rate and high test coverage across new components.
