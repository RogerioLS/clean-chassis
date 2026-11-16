# 06 — Documentation Routing & Audit Summary

Documentation is part of every deliverable. **Never create `README.md` inside `docs/`.** Route each type of knowledge strictly to its canonical file:

| Trigger / What Changed | Target File | Required Content |
| :--- | :--- | :--- |
| Task started, progressed, PR opened, or completed | `docs/status/PROJECT_STATUS.md` | Task board row (`TASK-XX`, Issue `#N`, PR `#M`, status), updated date & active branch |
| Session ending, reboot prep, or critical state change | `docs/status/HANDOFF_RESUME.md` | Current CV/LB/audit state, non-negotiable guardrails, exact next commands |
| Hardware limit, VRAM budget, env trap, leakage rule, or Kaggle submission ref | `docs/notes/MASTER_MEMORY_COMPILATION.md` | Constraint details, root cause, workaround, or row in Experiment & Submission Ledger |
| Dataset schema, target balance, group keys, or train/test shift | `docs/research/DATASET_EDA.md` | Row/column counts, target & group distributions, quality/shift findings |
| CV experiment, ablation study, latency/VRAM benchmark | `docs/research/BENCHMARK_ANALYSIS.md` | Experiment ID, CV score, runtime/VRAM, comparison against baseline & decision |
| Layer boundary, new module/adapter, or ADR | `docs/architecture/SYSTEM_DESIGN.md` | Updated directory layout and numbered ADR entry (Context, Decision, Consequences) |
| Release or milestone cut | `CHANGELOG.md` | Keep-a-Changelog semantic entry (`Added`, `Changed`, `Fixed`) |
| Root commands, env vars, or workflow changes | `README.md` / `.env.example` | Updated CLI command table, setup steps, and variable placeholders |
| Any run of `make audit` | `summary.md` & `artifacts/audit_summary.json` | **Auto-generated** by `scripts/generate_summary.py` — never hand-edit `summary.md` |

### Code Documentation Standards:
- Every new Python module, public class, and public function must have a Google-style docstring (`Args`, `Returns`, `Raises` where relevant).
- Comments explain *why* (invariants, hardware constraints, non-obvious edge cases), not *what*.
