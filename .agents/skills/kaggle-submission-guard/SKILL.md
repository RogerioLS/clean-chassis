---
name: kaggle-submission-guard
description: Enforces CV zero-leakage, offline Kaggle parity, codebase dataset syncing, and validated submission dispatch (.parquet, .csv, .zip).
---

# Kaggle Submission Guard Skill

Use this skill when packaging competition code for Kaggle Notebooks, validating submission outputs, or dispatching submissions to Kaggle.

## 1. Pre-Sync & Leakage Guardrails
1. Verify local CV uses proper group/time isolation (`GroupKFold` or `StratifiedGroupKFold`) with zero train-to-validation preprocessing leakage.
2. Confirm no secrets (`.env`, `kaggle.json`, `*token*`, `*.key`) or large local caches will be staged.
3. Ensure `make audit` passes 100% locally.

## 2. Synchronize Codebase to Kaggle Dataset
Dry-run first to inspect staged file count and target slug (`KAGGLE_DATASET_SLUG` in `.env`):
```bash
make sync-dataset ARGS="--dry-run"
```
Live sync (packages `competitions/`, `src/`, `scripts/`, `notebooks/`, `pyproject.toml`, `README.md`, `LICENSE`):
```bash
make sync-dataset ARGS="-m 'Describe pipeline update'"
```

## 3. Validate & Dispatch Submission
`scripts/submit_kaggle.py` auto-discovers `submission.parquet`, `submission.csv`, or `submission.zip` in `artifacts/` or `submission/` (or use `--file <path>`).
1. Run dry-run validation first:
   ```bash
   make submit-kaggle ARGS="--dry-run"
   ```
2. Dispatch live submission:
   ```bash
   make submit-kaggle ARGS="--competition <slug> -m 'v1.0 baseline'"
   ```
3. Query leaderboard submission status:
   ```bash
   make submit-kaggle ARGS="--status --competition <slug>"
   ```

## 4. Mandatory Post-Submission Memory Update
Immediately record the version, local CV score, submission message/ref, and runtime notes in `docs/notes/MASTER_MEMORY_COMPILATION.md` and `docs/status/HANDOFF_RESUME.md`.
