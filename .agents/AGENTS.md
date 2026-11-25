# AGENTS.md — Clean Chassis (Kaggle Flavor) Master Operating Protocol

**Project:** Clean Chassis — Kaggle Flavor  
**Domain:** Competitive Machine Learning, Offline GPU Pipelines & Software Engineering  
**Purpose:** Canonical operating protocol and pragmatic agent harness for this repository  
**Version:** 2.2  

---

# 0. Core Philosophy

This file is the repository-level operating protocol and routing layer.

- **The repository is the source of truth.** Not chat history, not human memory, not agent memory.
- **Rigor over haste**: Disciplined, leak-free, tested pipelines passing all quality gates beat unverified hacks.
- **Pragmatic Autonomy (Zero Hand-Holding)**: Agents proactively resolve/create `TASK-XX` + GitHub Issue `#NUM`, obey commit/branch governance, run quality gates, and update canonical `docs/` files **without waiting to be asked**.
- **Ponytail Minimalism**: Write the smallest *correct* implementation; reuse existing helpers; never touch out-of-scope files.
- **False-State Prevention**: Never claim a test passed, metric improved, or file exists without inspected command/file evidence.
- **Strict Role Boundary**: Agents NEVER merge directly into `main`, and `template/*` flavor branches NEVER merge back into `main`.

---

# 1. Source-of-Truth Hierarchy

When resolving ambiguity or conflicting context, follow this strict precedence:
1. Explicit user instruction in the current request
2. `docs/status/PROJECT_STATUS.md` & `docs/status/HANDOFF_RESUME.md`
3. `docs/architecture/SYSTEM_DESIGN.md`
4. `docs/notes/MASTER_MEMORY_COMPILATION.md`
5. Active task spec in `.github/issues/task-XX-*.md`
6. `.agents/rules/` (non-negotiable operating laws)
7. `.agents/skills/` (domain playbooks)
8. Existing codebase & tests (`src/`, `scripts/`, `tests/`)
9. Inference (last resort — never infer when the repository contains the answer)

---

# 2. Task Router (Load Only What You Need)

| Task Type | Mandatory Reads / Skills | Forbidden Actions |
| :--- | :--- | :--- |
| **Start Any Session** | `PROJECT_STATUS.md`, `HANDOFF_RESUME.md`, `MASTER_MEMORY_COMPILATION.md`, `git status` | Editing code before inspecting state |
| **Feature / Bugfix / Task** | `kanban-task-tracker`, `git-governance`, `03_git_workflow_and_commits.md` | Committing without `TASK-XX` (or valid `[RESERVED_TAG]`), committing on `main` |
| **EDA & Data Quality** | `docs/research/DATASET_EDA.md`, `04_testing_and_benchmarking.md` | Fitting scalers/encoders on full data, ignoring group keys |
| **CV / Modeling Experiment** | `competition-orchestrator`, `BENCHMARK_ANALYSIS.md`, `08_pragmatic_minimalism_and_experiments.md` | Random K-Fold on grouped data, deleting failed experiment logs |
| **Submission & Dataset Sync** | `kaggle-submission-guard`, `scripts/submit_kaggle.py`, `scripts/sync_kaggle_dataset.py` | Network calls in Kaggle notebooks, staging `.env`/secrets |
| **Architecture / Refactor** | `docs/architecture/SYSTEM_DESIGN.md`, `01_clean_architecture.md` | Importing ML frameworks in `src/core/`, touching out-of-scope modules |
| **Wrap-up & PR** | `documentation-steward`, `audit-enforcer`, `make check`, `make audit`, `make harness-check` | Hand-editing `summary.md`, merging into `main`, skipping doc updates |

---

# 3. Mandatory Session Start & End Checklist

### On Session Start (Before Editing Code):
1. Read `docs/status/PROJECT_STATUS.md`, `docs/status/HANDOFF_RESUME.md`, and `docs/notes/MASTER_MEMORY_COMPILATION.md`.
2. Check active branch and working tree (`git status`, `git branch -vv`).
3. If starting feature/fix work, resolve or create `TASK-XX` and GitHub Issue `#NUM` via `kanban-task-tracker` before making the first commit.
4. Apply the **Soft Green Light & Gatekeeper Check** (`05_agent_operating_guidelines.md`): execute directly for scoped tasks; align with the user first on architectural, CV-split, or high-impact changes.

### Before Concluding Any Work (Never Skip):
1. **Update Documentation** via `06_documentation_and_summary.md` and `documentation-steward`.
2. **Run Quality & Harness Gates**: `make check`, `make audit`, and `make harness-check`.
3. **Verify Governance**: Confirm branch name, `[TASK-XX:#NUM]` (or valid `[RESERVED_TAG]`) commit format, and zero leaked secrets.

---

# 4. Monorepo Organization

```text
clean-chassis/
├── .agents/                          # Operating protocols, rules, and specialized skills
│   ├── rules/                        # Modular engineering & governance rules (00..09)
│   └── skills/                       # Step-by-step operational playbooks
├── .github/                          # CI/CD workflows, issue specs, and kanban scripts
│   ├── issues/                       # Task markdown specs (task-XX-slug.md)
│   ├── scripts/                      # Kanban & issue setup automation (setup_kanban.py)
│   └── workflows/                    # Audit, branch lint, labeler, pages, sync_kaggle
├── .githooks/                        # Local pre-commit, prepare-commit-msg, commit-msg hooks
├── artifacts/                        # Audit reports, submissions, staging [GIT-IGNORED]
├── competitions/                     # Optional competition-specific modules & validators
├── docs/                             # Institutional documentation hub (NO README.md inside)
│   ├── architecture/                 # SYSTEM_DESIGN.md (ADRs & Clean Architecture)
│   ├── notes/                        # MASTER_MEMORY_COMPILATION.md (traps, hardware, ledger)
│   ├── research/                     # BENCHMARK_ANALYSIS.md & DATASET_EDA.md
│   └── status/                       # PROJECT_STATUS.md & HANDOFF_RESUME.md
├── notebooks/                        # Kaggle offline inference & experiment notebooks
├── scripts/                          # Automation (PR, audit, harness check, task sync, Kaggle CLI)
├── src/                              # Core domain, application use-cases, and adapters
└── tests/                            # Automated unit and integration tests
```

---

# 5. Rule & Skill Registry

### Rules (`.agents/rules/` — Always Active):
1. `00_clean_chassis_governance.md` — Owner merge authority, PR-driven flow, Standing Flavor Protection.
2. `01_clean_architecture.md` — Clean Architecture layers, 100-column limit, type hints, docstrings.
3. `02_security_and_anti_cheating.md` — Zero secrets, proxy/SSL resilience, hermetic mocks.
4. `03_git_workflow_and_commits.md` — Task-to-Issue `#NUM` binding, branch naming, commit format.
5. `04_testing_and_benchmarking.md` — Two-tier gates, CV zero-leakage, offline parity.
6. `05_agent_operating_guidelines.md` — Pragmatic 6-step loop, Soft Green Light & False-State Prevention.
7. `06_documentation_and_summary.md` — Exact doc-routing matrix (which doc to update and when).
8. `07_terminal_and_minimalism.md` — 42-style silent progress, concise actionable feedback.
9. `08_pragmatic_minimalism_and_experiments.md` — *Ponytail* minimalism & reproducible experiment ledger.
10. `09_quota_and_model_routing.md` — Tiered model routing (Hydrogen/Argon/Neon), context hygiene, /compact triggers, and zero-GPU local execution.

### Skills (`.agents/skills/` — Load When Relevant):
- `competition-orchestrator` — End-to-end Kaggle iteration coordinator.
- `kanban-task-tracker` — Creating `.github/issues/task-XX-*.md`, resolving/creating GitHub Issues (`#NUM`), syncing tasks.
- `git-governance` — Branch creation, `[TASK-XX:#NUM]` commits, `scripts/create_pr.py`, flavor protection.
- `documentation-steward` — Automatic routing and formatting for every file in `docs/` and `CHANGELOG.md`.
- `audit-enforcer` — Running `make check`, `make audit`, `bandit`, and verifying `summary.md`.
- `kaggle-submission-guard` — Dataset sync (`make sync-dataset`), `.parquet`/`.csv`/`.zip` validation, `make submit-kaggle`.

---

# 6. Quick Reference Commands

- `make help` — Interactive command center.
- `make install` — 42-style silent installation of dependencies and git hooks.
- `make check` — Pre-commit sanity check (black, isort, flake8, ruff).
- `make audit` — Full audit: `py_compile` + `flake8` (100 cols) + `ruff` + `pytest` + `summary.md`.
- `make harness-check` — Verify `.agents/` rules/skills, canonical `docs/` layout, and task linkage.
- `make pr` — Create or update GitHub PR with auto-linked `Resolves #<ISSUE_NUM>`.
- `make sync-dataset` — Package & sync `competitions/`, `src/`, `scripts/`, `notebooks/` to Kaggle Dataset.
- `make submit-kaggle` — Validate & submit `submission.{parquet,csv,zip}` (supports `--dry-run`, `--status`).
- `make clean` — Clean temporary caches and build artifacts.
