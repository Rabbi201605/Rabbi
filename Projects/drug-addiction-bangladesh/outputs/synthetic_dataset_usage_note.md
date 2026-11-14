# Synthetic Dataset: Analysis and Usage Note

**This report concerns simulated records only. It is not a report of actual drug use in Bangladesh.**

- Number of records: 1,426
- Number of variables: 26
- Seed documented for the generator: 20261112
- Outcome field: `ever_taken_drug` (0 = No; 1 = Yes)
- `age_of_first_use` is intentionally blank for simulated never-users.
- Consistency repair: the original simulation contained impossible combinations (for example a 15-year-old postgraduate). `src/repair_synthetic_consistency.py` corrected 79 respondents using fixed rules; every change is listed in `docs/synthetic_data_repair_log.csv`. The outcome column was not changed.

Run `python src/eda_synthetic.py` to generate descriptive summaries, a smoking-by-outcome cross-tabulation, and an outcome distribution chart.

## Appropriate use
Use these files for practising data import, data cleaning, descriptive statistics, cross-tabulation, visualisation, and introductory modelling in Python, Excel, or SPSS.

## Not appropriate
Do not use synthetic frequencies, percentages, tests, charts, or model coefficients as empirical evidence, thesis findings, public-health estimates, or claims about Bangladesh. Do not merge them with the original thesis results. Recover the authentic source dataset and rerun the original analysis for academic reporting.
