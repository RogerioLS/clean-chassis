# 🚨 Session Handoff & Immediate Resumption Guide

> **Last Updated:** DD/MM/YYYY  
> **Repository:** `<Owner>/<repository-name>`  
> **Active Branch:** `main`  
> **Canonical Role:** Fast-recovery operational briefing after machine reboot, context compaction, or multi-machine switch.

---

## 1. Current Operational State

- **Test Suite & Quality Gate:** `make audit` passing (`100%`)
- **Current Best Local CV:** `-`
- **Current Best Public LB:** `-`
- **Active Objective:** Describe the immediate next milestone or experiment.

---

## 2. Non-Negotiable Guardrails

1. Never alter validated hardware/memory limits without an empirical benchmark.
2. Never submit without running `make check` and verifying offline package constraints.
3. Preserve CV group isolation to prevent train/validation leakage.

---

## 3. Immediate Next Actions

1. Sync environment and verify tests:
   ```bash
   make check
   make test
   ```
2. Continue work on the active task branch and update `docs/status/PROJECT_STATUS.md` upon completion.
