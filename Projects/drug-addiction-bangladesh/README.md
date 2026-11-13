# Drug Addiction in Bangladesh: A Statistical Analysis

## Project Overview
This research project examines social, family, and behavioral factors associated with drug addiction in Bangladesh. The original academic work was based on a secondary survey dataset attributed to Mostafa Mohiuddin Jalal Protik and titled **"Drug addiction in Bangladesh – Reasons"**.

The reported original dataset contained **1,426 respondents and 26 coded variables**. Verify the original source, current availability, and license or permission before reuse.

## Research Questions
1. How are demographic and educational characteristics distributed?
2. Which social, family, and behavioral factors are associated with reported drug-taking status?
3. What patterns appear among coded variables?
4. What can statistical tests and regression models tell us, and what are their limitations?

## Tools and Methods
- Python for data inspection, cleaning, and exploratory analysis
- SPSS / Excel for statistical analysis and cross-checking
- Descriptive statistics, chi-square tests, t-tests, ANOVA, correlation, and regression

## Repository Contents
- `data/raw/`: location for a permitted copy of the original dataset (not committed)
- `data/synthetic_drug_addiction_bangladesh.csv`: separate synthetic practice dataset
- `data/data_dictionary.csv`: descriptions of the synthetic dataset variables
- `src/eda.py`: general-purpose EDA script for the original source data
- `src/eda_synthetic.py`: EDA script for the synthetic practice dataset
- `outputs/`: analysis notes and generated outputs

## Original Dataset Workflow
1. Obtain the original dataset from its source and record its license / terms.
2. Place a permitted copy at `data/raw/drug_addiction_bangladesh.csv`.
3. Inspect column names, data types, missing values, duplicates, and coding.
4. Complete the original codebook before interpreting coded variables.
5. Run:
   ```bash
   python src/eda.py --input data/raw/drug_addiction_bangladesh.csv --output outputs
   ```
6. Conduct inferential analyses after checking assumptions and report effect sizes, uncertainty, and limitations.

## Synthetic Practice Dataset
**IMPORTANT: The synthetic CSV is simulated data, not observations from real Bangladesh respondents.** It is provided only for practising Python, Excel, SPSS, descriptive statistics, cross-tabulations, and introductory modelling. Its frequencies and statistical outputs are not estimates of real-world prevalence and must not be presented as empirical thesis findings.

To run its dedicated script:
```bash
python -m pip install -r requirements.txt
python src/eda_synthetic.py
```
Random seed used for the synthetic generator: `20261112`.

## Previously Reported Analysis Notes
The original academic analysis included chi-square tests, ANOVA, t-tests, correlation analysis, OLS, binary logistic regression, multicollinearity checks, and factor-analysis diagnostics. Previously recorded chi-square notes include:
- Smoking status: chi-square = 456.520, p approximately 7.38 × 10⁻¹⁰⁰, Cramér's V = 0.566
- Family relationship: chi-square = 247.952
- Withdrawal symptoms: chi-square = 92.594
- Education: chi-square = 59.400
- Living with a drug user: chi-square = 32.001
- Gender: chi-square = 22.719

These figures are historical notes from the earlier analysis and have **not** been independently reproduced here. Do not cite them as verified results until the original dataset, coding, test tables, and analysis script have been checked and rerun.

## Academic Integrity and Ethics
- Synthetic records must never be represented as real survey responses.
- Do not mix synthetic results with original thesis findings.
- Association does not establish causation.
- Do not upload identifiable, confidential, or restricted respondent-level data.
- Interpret coded variables using the authentic original codebook.
- Report sample limitations, missingness, and model assumptions.
