# Drug Addiction in Bangladesh: A Statistical Analysis

## Project Overview
This research project examines social, family, and behavioral factors associated with drug addiction in Bangladesh. The analysis is based on a secondary survey dataset attributed to Mostafa Mohiuddin Jalal Protik and titled **"Drug addiction in Bangladesh – Reasons"**.

The reported dataset contains **1,426 respondents and 26 coded variables**. Before publishing any dataset or reproducing results, verify the original source, its current availability, and its license or permission for reuse.

## Research Questions
1. How are demographic and educational characteristics distributed in the dataset?
2. Which social, family, and behavioral factors are associated with reported drug-taking status?
3. What patterns appear in the relationships among the coded variables?
4. What can statistical tests and regression models tell us, and what are their limitations?

## Tools
- Python for data inspection, cleaning, and exploratory analysis
- SPSS / Excel for statistical analysis and cross-checking
- Statistical methods: descriptive statistics, chi-square tests, t-tests, ANOVA, correlation, and regression

## Analysis Workflow
1. Obtain the dataset from its original source and record its license / terms.
2. Place a permitted copy at `data/raw/drug_addiction_bangladesh.csv`.
3. Inspect column names, data types, missing values, duplicates, and coding.
4. Document the codebook before interpreting coded variables.
5. Run exploratory analysis using the Python script in `src/eda.py`.
6. Conduct appropriate inferential analyses after checking assumptions.
7. Report effect sizes, uncertainty, limitations, and reproducible findings.

## Previously Reported Analysis Notes
The original academic analysis included chi-square tests, ANOVA, t-tests, correlation analysis, OLS, binary logistic regression, multicollinearity checks, and factor-analysis diagnostics. Examples of previously recorded chi-square results include:
- Smoking status: chi-square = 456.520, p approximately 7.38 × 10⁻¹⁰⁰, Cramér's V = 0.566
- Family relationship: chi-square = 247.952
- Withdrawal symptoms: chi-square = 92.594
- Education: chi-square = 59.400
- Living with a drug user: chi-square = 32.001
- Gender: chi-square = 22.719

These are notes from the earlier analysis, not independently reproduced in this repository yet. They should not be treated as verified outputs until the dataset, coding, test tables, and analysis script are checked and rerun.

## Repository Structure
```
drug-addiction-bangladesh/
├── data/
│   ├── raw/          # Place permitted source data here (not committed)
│   └── processed/    # Generated files (not committed)
├── outputs/          # Generated summaries and figures (not committed)
├── src/
│   └── eda.py
├── requirements.txt
└── README.md
```

## Run the Exploratory Analysis
From this project directory:

```bash
python -m pip install -r requirements.txt
python src/eda.py --input data/raw/drug_addiction_bangladesh.csv --output outputs
```

The script produces a data overview, missing-value summary, descriptive statistics, categorical frequency tables, and numeric correlation output when applicable. It does not assume the meaning of coded columns.

## Important Ethical and Methodological Notes
- This is observational survey data; association does not establish causation.
- Do not infer sensitive personal characteristics from coded values.
- Do not upload identifiable, confidential, or restricted respondent-level data.
- Interpret every coded variable using the original codebook.
- Report sample limitations, missingness, and model assumptions.
