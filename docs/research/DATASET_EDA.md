# 📊 Dataset Exploratory Data Analysis (EDA)

> **Project:** `<Competition Name>`  
> **Purpose:** Empirical characterization of train/test distributions, class balance, missingness, group structure, and potential train/test shift.

---

## 1. Dataset Inventory & Schema

| Split | File | Rows | Columns | Target / Group Columns | Notes |
| :--- | :--- | :---: | :---: | :---: | :--- |
| Train | `train.*` | - | - | - | - |
| Test | `test.*` | - | - | - | - |

---

## 2. Target & Group Distribution

- **Class / Target Balance:** Document target skew, outliers, or metric sensitivity.
- **Grouping Keys:** Identify duplicate entities or shared IDs requiring `GroupKFold` / `StratifiedGroupKFold`.

---

## 3. Data Quality & Shift Risks

- Missing values, corrupted samples, sequence length distributions, and train-vs-test domain differences.
