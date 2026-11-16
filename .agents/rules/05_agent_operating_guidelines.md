# 05 — Agent Operating Guidelines (Pragmatic Harness Loop)

Execute this loop autonomously on every engineering task so governance, validation, and documentation happen by default:

## 1. Mandatory 6-Step Execution Loop
1. **Boot & Discover**:
   - Read `.agents/AGENTS.md`, `docs/status/PROJECT_STATUS.md`, `docs/status/HANDOFF_RESUME.md`, and `docs/notes/MASTER_MEMORY_COMPILATION.md`.
   - Check `git status`, active branch, and existing tests.
2. **Task & Issue Binding (Before Coding)**:
   - Resolve the active `TASK-XX` and GitHub Issue `#NUM` (or create `.github/issues/task-XX-<slug>.md` + GitHub Issue via `gh` and record `github_issue: <NUM>` in frontmatter).
   - Work on a valid branch (`<type>/<task-id>-<desc>`), never committing feature work directly on `main`.
3. **Pragmatic Gatekeeper & Soft Green Light**:
   - **Routine / Scoped Tasks** (clear feature, bugfix, test, or doc request): Proceed directly to implementation after verifying the **Gatekeeper Check** internally (Target files, Active skill, Exclusive scope, Minimal diff).
   - **High-Impact / Ambiguous Changes** (changing CV split strategy, `SYSTEM_DESIGN.md` architecture, GPU/VRAM budgets, submission format, or multi-module refactors): Present a concise `[GATEKEEPER CHECK]` + plan and obtain user alignment before editing files.
4. **Implement & Validate**:
   - Apply `08_pragmatic_minimalism_and_experiments.md` (reuse helpers, smallest clean diff, typed, 100-col, Google docstrings, hermetic tests).
   - Run `make check`, `make audit`, and `make harness-check` after edits.
5. **Document Automatically**:
   - Route updates via `06_documentation_and_summary.md` (`documentation-steward` skill) as part of the task.
6. **Governed Commit & Completion Report**:
   - Commit with `[TASK-XX:#NUM]` (or valid `[RESERVED_TAG]` for pure infra/docs).
   - Open/update PR via `make pr` with `Resolves #<NUM>`; never merge into `main`.

## 2. False-State Prevention & Completion Summary
- **Never claim** a test passed, CV improved, submission succeeded, or file exists unless directly observed in tool output.
- Conclude every substantial task with exact file links, validations run, documentation updated, and the next recommended step.
