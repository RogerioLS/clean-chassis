# 01 — Clean Architecture & Python Standards

1. **Separation of Concerns**: Pure core domain (`src/core/`) must have zero dependencies on CLI or external presentation frameworks.
2. **100-Column Limit**: Strictly enforce 100-character line lengths across all files (`flake8 --max-line-length=100`, `ruff`, `black`).
3. **Type Annotations**: All public functions and classes must include complete type hints.
4. **Google-Style Docstrings**: Provide clear, descriptive docstrings with Args and Returns for all modules, classes, and public methods.
