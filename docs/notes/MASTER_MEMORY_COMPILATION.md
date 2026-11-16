# 🧠 Master Memory Compilation

> **Project:** `<Competition Name>`  
> **Repository:** `<Owner>/<repository-name>`  
> **Status:** Active  
> **Canonical Role:** Single-source permanent engineering memory for rapid onboarding and post-reboot context recovery.

---

## 1. Competition Objective & Evaluation Metric

- **Problem Statement:** Describe the task, inputs, and expected prediction format.
- **Official Metric:** Specify the exact Kaggle evaluation formula and edge-case penalties.
- **Target Baseline / Medal Threshold:** Record CV and Leaderboard (LB) targets.

---

## 2. Validation Strategy & Leakage Guardrails

- **Cross-Validation Split:** e.g., `StratifiedGroupKFold(n_splits=5)` grouped by entity/prompt/patient ID.
- **Zero-Leakage Rules:** Document forbidden features, target leakage risks, and preprocessing fit boundaries (fit strictly inside training folds).

---

## 3. Hardware Rules & Environment Traps

- **GPU / VRAM Budget:** Record device limits (e.g., Kaggle T4 16GB / P100 16GB / L4 24GB), batch sizes, and precision (`fp16` / `bf16`).
- **Offline Constraints:** Kaggle evaluation notebooks run without internet; all code and wheels must come from synced Kaggle Datasets (`make sync-dataset`).
- **Known Gotchas:** Document dependency ABI traps, timeout budgets, and deterministic seed requirements.

---

## 4. Experiment & Submission Ledger

| Version | Strategy / Change | Local CV | Public LB | Submission Ref | Notes |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `v1.0` | Baseline pipeline | - | - | - | Initial end-to-end verification |
