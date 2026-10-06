# AGENTS.md — Clean Chassis Master Operating Protocol

**Project:** Clean Chassis  
**Domain:** Foundational Software Engineering & Production Blueprint  
**Purpose:** Canonical operating protocol for AI coding agents and human developers  
**Version:** 2.0  

---

# 0. Core Philosophy

This file is the repository-level operating protocol.

- **The repository is the source of truth.** Not chat history, not temporary memory.
- **Rigor over haste**: High-integrity code passing all quality gates beats an unverified hack.
- **Two-Tier Quality Gates**: Every change must pass local validation (`make check`, `make audit`) and CI/CD pipelines.
- **Zero Terminal Spam**: Installations and builds follow the 42 standard (silent execution, real-time single-line progress).
- **Strict Role Boundary**: Agents NEVER merge directly into `main`. The Owner (`RogerioLS`) reviews and merges PRs on GitHub.

---

# 1. Monorepo Organization

```text
clean-chassis/
├── .agents/                 # Operating protocols, rules, and specialized skills
│   ├── rules/               # Modular engineering rules
│   └── skills/              # Executable and instructional agent skills
├── .github/                 # Workflows (audit, branch lint, labeler, pages)
├── .githooks/               # Local pre-commit & commit-msg hooks
├── artifacts/               # Audit reports and generated metrics
├── docs/                    # Architecture and documentation
├── scripts/                 # Automation scripts (clean install, PR creation, task sync)
├── src/                     # Core domain and application source code
└── tests/                   # Automated unit, integration, and security tests
```

---

# 2. Rule Registry

Before implementing any feature or modifying code, agents must load and follow:
1. `rules/00_clean_chassis_governance.md` — PR lifecycle, role boundaries, merge policies.
2. `rules/01_clean_architecture.md` — Domain design, separation of concerns, 100-column limit.
3. `rules/02_security_and_anti_cheating.md` — Secret prevention, proxy resilience, credential protection.
4. `rules/03_git_workflow_and_commits.md` — Branch formatting and Conventional Task Commits.
5. `rules/04_testing_and_benchmarking.md` — Pytest, fixtures, coverage gates, hermetic mocks.
6. `rules/05_agent_operating_guidelines.md` — Pre-flight discovery, non-interactive execution.
7. `rules/06_documentation_and_summary.md` — Auto-generated audit certificates, docstrings.
8. `rules/07_terminal_and_minimalism.md` — 42-style silent progress, terminal cleanliness.

---

# 3. Quick Reference Commands

- `make help` — Interactive command center.
- `make install` — 42-style silent installation of dependencies and git hooks.
- `make check` — Pre-commit sanity check (formatters, linters).
- `make audit` — Full audit: syntax compile + flake8 (100 cols) + ruff + pytest + summary.md.
- `make clean` — Clean temporary caches and build artifacts.
