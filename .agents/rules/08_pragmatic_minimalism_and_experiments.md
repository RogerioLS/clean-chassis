# 08 — Pragmatic Minimalism (*Ponytail*) & Experiment Protocol

## 1. Pragmatic Minimalism (*Ponytail* Standard)
Aim for the smallest **correct** implementation that preserves architecture, leakage protection, tests, and documentation.

### Pre-Code Checklist:
1. Does this helper or behavior already exist in `src/` or `scripts/`? Reuse before writing new code.
2. Can Python stdlib or already-installed libraries solve it cleanly?
3. Prefer: pure function ➔ small module ➔ simple dataclass/config ➔ class/abstraction (only when repeated patterns justify it).
4. Keep diffs strictly scoped to the current task — never refactor unrelated files opportunistically.

### Non-Negotiable Boundaries (Minimalism ≠ Laziness):
Never omit tests, type hints, docstrings, CV group isolation, input/schema validation, or doc updates to "save lines".

---

## 2. Reproducible Experiment Protocol
Every meaningful modeling, feature, or pipeline experiment must record:
- **Hypothesis**: What is expected to improve and why.
- **Validation Split**: Exact CV scheme (e.g., `StratifiedGroupKFold(5)` with grouping key) and random seed.
- **Baseline vs Candidate**: Exact local CV metric delta, runtime, and peak VRAM/RAM.
- **Decision**: `promote` | `reject` | `revisit`.

### Preserve Negative Results:
Never delete or hide failed experiments. Record `reject` decisions in `docs/research/BENCHMARK_ANALYSIS.md` (and key traps in `docs/notes/MASTER_MEMORY_COMPILATION.md`) so future sessions do not repeat dead ends.
