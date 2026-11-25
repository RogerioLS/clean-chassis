# 09 — Quota Preservation & Model Routing Governance

1. **Tiered Model Routing Hierarchy**:
   - **Gemini 4 Hydrogen (`flash_lite`)**: Default model for lightweight, high-volume operations: repository scans, directory listings, grep, file discovery, reading short files, status checks, and routine terminal execution. Consumes negligible weekly quota.
   - **Gemini 4 Argon (`flash`)**: Standard workhorse model for software engineering: writing code, refactoring, unit and integration tests, bug fixes, EDA scripts, and local verification suites. Balances high reasoning quality with minimal quota consumption.
   - **Gemini 4 Neon (`pro`)**: Reserved exclusively for high-complexity architectural design, difficult mathematical and algorithmic derivations (e.g. Givens rotations, SDP/homotopy formulations, discrete-continuous approximations), and anti-leakage audits. Autonomous agents must never employ Neon for routine file reading or repetitive bash commands.

2. **Subagent Delegation Policy**:
   - For broad codebase exploration or extensive file reading, delegate to subagents configured with lighter models (`flash` or `flash_lite`), keeping the primary reasoning context pristine and token-compact.

3. **Context Length & Token Hygiene**:
   - **Proactive Context Compaction (`/compact`)**: Whenever a major development milestone is reached (e.g., closing a task, passing test suites, completing an EDA phase, or preparing a PR), recommend or trigger `/compact` to shed obsolete historical tokens.
   - **Log & Output Discipline**: Never dump raw training logs, large dataframes, or multi-megabyte files directly into context. Filter all outputs using concise utilities (`head`, `tail`, `grep`, `jq`, summary metrics).
   - **Strict Ban on Polling Loops**: Never run polling sleep loops (`while sleep ...`) in the terminal. Always rely on asynchronous execution, background task completion notifications, or timers.

4. **Zero-GPU Local Execution & Remote Offloading**:
   - Heavy compute tasks (e.g. neural network training, large-scale matrix factorizations, homotopy runs) must be offloaded to Kaggle GPU kernels or remote runners. Local developer environments must remain 100% lightweight and zero-GPU.

5. **Harness Verification**:
   - Compliance with this rule is verified automatically via `make harness-check` and `test_template_integrity.py`.
