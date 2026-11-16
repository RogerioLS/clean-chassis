---
name: competition-orchestrator
description: Coordinates end-to-end Kaggle competition iterations from discovery and Task/Issue binding through CV experiments, documentation routing, harness checks, and PR creation.
---

# Competition Orchestrator Skill

Use this skill to coordinate multi-step Kaggle feature, modeling, or pipeline iterations without skipping governance or documentation steps.

## End-to-End Iteration Workflow
1. **Context Boot**:
   - Load `docs/status/PROJECT_STATUS.md`, `docs/status/HANDOFF_RESUME.md`, and `docs/notes/MASTER_MEMORY_COMPILATION.md`.
   - Inspect `git status` and active branch.
2. **Task & Issue Binding**:
   - Invoke `kanban-task-tracker` to resolve or create `TASK-XX` in `.github/issues/` and bind `github_issue: <NUM>`.
   - Ensure you are on `<type>/task-XX-<slug>` (use `git-governance`).
3. **Soft Green Light & Gatekeeper Check**:
   - Confirm scope, active skill, target files, and minimal diff (*Ponytail*).
   - If the change alters CV splits, competition architecture, or GPU budgets, align briefly with the user before editing; otherwise proceed directly.
4. **Execute & Benchmark**:
   - Implement inside `src/` / `scripts/` (keep `notebooks/` as thin runners).
   - Validate CV strictly with group/time isolation (zero leakage) and record experiment metrics (including rejected hypotheses).
5. **Sync Documentation & Harness**:
   - Apply `documentation-steward` to update `PROJECT_STATUS.md`, `HANDOFF_RESUME.md`, `BENCHMARK_ANALYSIS.md` / `DATASET_EDA.md`, and `MASTER_MEMORY_COMPILATION.md`.
   - Run `audit-enforcer` (`make check`, `make audit`) and `make harness-check`.
6. **Package, Submit & PR**:
   - If deploying to Kaggle, invoke `kaggle-submission-guard` (`make sync-dataset`, `make submit-kaggle`).
   - Commit with `[TASK-XX:#NUM]` and open PR via `make pr`.
