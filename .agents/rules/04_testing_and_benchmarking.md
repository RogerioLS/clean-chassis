# 04 — Testing, Benchmarking & ML Evaluation Gates

1. **Two-Tier Quality Gates**:
   - **Tier 1 (`make check`)**: Fast pre-commit linting (`py_compile`, `black --check`, `isort --check-only`, `flake8 --max-line-length=100`, `ruff check .`).
   - **Tier 2 (`make audit`)**: Complete verification (`py_compile`, `flake8`, `ruff`, `pytest`, `bandit` via `scripts/generate_summary.py`, producing `summary.md` and `artifacts/audit_summary.json`).
2. **Zero Regression**: Never leave failing or skipped tests. All new scripts, features, and bugfixes require corresponding unit or integration tests.
3. **Zero-Leakage Cross-Validation (Kaggle ML)**:
   - Never evaluate models on random splits when samples share groups (`prompt_id`, `patient_id`, `session_id`, `user_id`); enforce `GroupKFold` / `StratifiedGroupKFold`.
   - Fit encoders, scalers, vectorizers, and target encodings strictly inside each training fold.
   - Pin random seeds (`42` default) across Python, NumPy, and ML frameworks.
4. **Offline Parity**: Any Kaggle inference pipeline or submission artifact must work with `--network none` using only synced dataset assets (`make sync-dataset`) and local weights.
