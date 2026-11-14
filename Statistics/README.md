# Statistics

Statistical methods used in this portfolio, with where each one is applied. All results so far come from synthetic data and are for practice only.

## Methods applied
| Method | Used for | Where |
|---|---|---|
| Chi-square test of independence | Association between categorical variables and an outcome | [Drug Addiction project](../Projects/drug-addiction-bangladesh/outputs/statistical_analysis/statistical_analysis_report.md), [Healthcare findings](../Projects/healthcare-dashboard/outputs/findings.md) |
| Cramér's V | Effect size for chi-square tests | Same reports |
| Holm correction | Controlling error across many tests | [Drug Addiction report](../Projects/drug-addiction-bangladesh/outputs/statistical_analysis/statistical_analysis_report.md) |
| Welch t-test and Mann-Whitney U | Comparing age between two groups | Drug Addiction report |
| Kruskal-Wallis test | Comparing skewed costs across departments | [Healthcare findings](../Projects/healthcare-dashboard/outputs/findings.md) |
| Spearman correlation | Monotonic association (stay vs cost, stay vs satisfaction) | Healthcare findings |
| Logistic regression | Predicting a binary outcome, with holdout accuracy and ROC-AUC | Drug Addiction report |

## Practice notes
- Report effect sizes with p-values; a small p-value alone does not mean an important effect.
- Check expected counts before trusting a chi-square test.
- Association is not causation.

## Not yet covered
ANOVA, OLS regression, and factor analysis appear in the original thesis notes but have not been reproduced here.
