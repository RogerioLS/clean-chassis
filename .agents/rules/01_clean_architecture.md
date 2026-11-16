# 01 — Clean Architecture & Python Standards

1. **Separation of Concerns**:
   - `src/core/`: Pure domain entities, metrics, and calculations with zero dependencies on CLI, ML frameworks (PyTorch/LightGBM/HF), or external IO.
   - `src/application/`: Use-case orchestration, cross-validation runners, and pipelines.
   - `src/adapters/`: External data loaders, model backbones, feature extractors, and submission exporters.
2. **100-Column Limit**: Strictly enforce 100-character line lengths across all Python files (`black`, `isort`, `flake8 --max-line-length=100`, `ruff`).
3. **Type Annotations**: All public functions, methods, and classes must include complete type hints.
4. **Google-Style Docstrings**: Provide clear, descriptive docstrings with `Args` and `Returns` for all modules, classes, and public methods.
