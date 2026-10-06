# 03 — Git Workflow & Conventional Task Commits

1. **Branch Naming**:
   - `feat/<task-id>-<description>`
   - `fix/<task-id>-<description>`
   - `chore/<task-id>-<description>`
2. **Commit Message Format**:
   - `<type>(<scope>): [<TASK-ID>:#<ISSUE_NUM>] <short description>`
   - Example: `feat(core): [TASK-01:#6] implement computation engine`
   - Infra/Chore: `ci(labeler): [INFRA] switch trigger to pull_request`
3. **Enforced Hooks**: Clean Chassis git hooks validate branch names and commit formats before allowing commits.
