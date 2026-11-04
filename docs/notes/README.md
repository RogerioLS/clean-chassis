# 🧠 Engineering Notes & Permanent Memory

> **Purpose:** Permanent repository for hardware constraints, edge-case traps, operating system quirks, and institutional knowledge preservation across sessions.

---

## 🧭 Directory Purpose & Guidelines

Software engineering teams and autonomous AI agents frequently encounter subtle environment bugs, hardware incompatibilities, or architectural traps that cost hours to diagnose.

Documenting them here ensures **zero loss of context** across sprints, developer rotations, or session resets.

### Recommended Content:
1. **Hardware Rules & Memory Profiles**:
   - VRAM partitioning, GPU allocation limits, and CUDA driver compatibilities.
   - CPU offloading warnings and throughput benchmarks.
2. **Environment & Dependency Traps**:
   - ABI mismatches (e.g. PyTorch C++ symbols vs custom wheels).
   - Python packaging nuances (e.g. `pip install` vs direct `sys.path` wheel injection).
3. **Master Memory Briefing (`MASTER_MEMORY.md`)**:
   - Single-file executive summary enabling an engineer or AI agent to ramp up on the project in under 60 seconds.
