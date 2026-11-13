# Statistical Analysis Report — SYNTHETIC DATA ONLY

> WARNING: These are simulated practice records, not observations from Bangladesh.
> Do not report these results as real prevalence, risk factors, or thesis findings.

## Data validation
- Shape: 1426 rows x 26 columns
- Duplicate rows: 0
- Unique IDs: 1426
- Simulated positive outcome: 39.20%

## Analyses
- Descriptive statistics and missing-data profile
- Categorical cross-tabs, chi-square tests, Cramér's V and Holm correction
- Welch t-test and Mann–Whitney U test for age
- Holdout logistic regression using pre-outcome predictors only

## Strongest categorical associations by unadjusted p-value

| Variable | Chi-square | df | p-value | Cramér's V | Holm p |
|---|---:|---:|---:|---:|---:|
| smoking_status | 47.825 | 1 | 4.66e-12 | 0.185 | 8.39e-11 |
| gender | 26.121 | 2 | 2.13e-06 | 0.135 | 3.62e-05 |
| living_with_drug_user | 15.106 | 1 | 0.000102 | 0.105 | 0.00163 |
| peer_pressure | 14.800 | 2 | 0.000611 | 0.102 | 0.00917 |
| family_support | 11.238 | 2 | 0.00363 | 0.089 | 0.0508 |
| parental_supervision | 10.695 | 2 | 0.00476 | 0.087 | 0.0619 |
| access_to_drugs | 7.085 | 2 | 0.0289 | 0.070 | 0.347 |
| stress_level | 5.831 | 2 | 0.0542 | 0.064 | 0.596 |
| employment_status | 5.390 | 3 | 0.145 | 0.061 | 1 |
| depression_symptoms | 2.760 | 2 | 0.252 | 0.044 | 1 |

Variables with Holm-adjusted p < 0.05 in this synthetic dataset: smoking_status, gender, living_with_drug_user, peer_pressure.

This is a description of the simulation only, not a claim about real people.

## Logistic model holdout metrics
- Complete records: 1,426
- Training records: 1,069
- Test records: 357
- Accuracy: 0.591
- Precision: 0.473
- Recall: 0.371
- ROC-AUC: 0.612
- Confusion matrix (TN, FP, FN, TP): 159, 58, 88, 52

## Age comparison
- No group: n=867, mean age=24.14, median=24
- Yes group: n=559, mean age=24.06, median=24
- Welch t-test p=0.733
- Mann–Whitney U p=0.935

## Limitations
- Simulated data cannot establish facts about Bangladesh or its population.
- Association is not causation; p-values do not measure practical importance.
- Chi-square expected counts were adequate for the tested tables.
- A random holdout is not external validation.
- Logistic coefficients are predictive associations, not causal effects.
- Recover the original dataset and its codebook before reproducing thesis findings.

## Reproducibility
Run from this project folder: python src/statistical_analysis.py
