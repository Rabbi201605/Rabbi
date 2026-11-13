"""Statistical analysis for the SYNTHETIC practice dataset only."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, mannwhitneyu, ttest_ind
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

N_ROWS, N_COLS = 1426, 26
Y = "ever_taken_drug"
ID = "respondent_id"
POST_OUTCOME = {"age_of_first_use", "drug_frequency", "withdrawal_symptoms", "treatment_history"}
NON_ANALYTIC = {"survey_response_quality"}
PREDICTORS = [
    "age", "gender", "education_level", "employment_status", "residence",
    "family_type", "family_relationship", "parental_supervision", "peer_pressure",
    "stress_level", "depression_symptoms", "smoking_status", "alcohol_use",
    "living_with_drug_user", "awareness_level", "access_to_drugs",
    "family_support", "social_media_influence", "monthly_income_group"
]

def cramers_v(tab):
    chi2 = chi2_contingency(tab, correction=False)[0]
    n = tab.to_numpy().sum()
    den = n * min(tab.shape[0] - 1, tab.shape[1] - 1)
    return float(np.sqrt(chi2 / den)) if den > 0 else np.nan

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="data/synthetic_drug_addiction_bangladesh.csv")
    p.add_argument("--output", default="outputs/statistical_analysis")
    a = p.parse_args()
    source, out = Path(a.input), Path(a.output)
    if not source.exists():
        raise FileNotFoundError(f"Missing dataset: {source}")
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(source)
    if df.shape != (N_ROWS, N_COLS):
        raise ValueError(f"Expected 1426 x 26; got {df.shape}")
    if Y not in df or not set(df[Y].dropna().unique()).issubset({0, 1}):
        raise ValueError("Outcome must be binary 0/1.")
    if df[ID].duplicated().any():
        raise ValueError("Respondent IDs must be unique.")

    quality = pd.DataFrame({
        "column": df.columns, "dtype": [str(x) for x in df.dtypes],
        "missing_n": df.isna().sum().values,
        "missing_pct": (df.isna().mean().values * 100).round(2),
        "unique_n": df.nunique().values
    })
    quality.to_csv(out / "data_quality.csv", index=False)
    df.describe(include="all").T.to_csv(out / "descriptive_summary.csv")
    counts = df[Y].value_counts().sort_index().rename_axis("outcome").reset_index(name="n")
    counts["percent"] = (counts["n"] / len(df) * 100).round(2)
    counts.to_csv(out / "outcome_distribution.csv", index=False)

    fig, ax = plt.subplots(figsize=(6, 4))
    vals = [(df[Y] == 0).sum(), (df[Y] == 1).sum()]
    ax.bar(["No (0)", "Yes (1)"], vals)
    ax.set(title="Synthetic outcome distribution", xlabel="Ever taken drugs", ylabel="Simulated records")
    for i, v in enumerate(vals):
        ax.text(i, v, str(v), ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(out / "outcome_distribution.png", dpi=160)
    plt.close(fig)

    # Bivariate categorical associations. Exclude IDs and post-outcome fields.
    cat_cols = [c for c in df.columns if c not in POST_OUTCOME | NON_ANALYTIC | {ID, Y}
                and is_string_dtype(df[c])]
    tests = []
    for col in cat_cols:
        tab = pd.crosstab(df[col], df[Y])
        if tab.shape[0] < 2 or tab.shape[1] < 2:
            continue
        chi2, pv, dof, exp = chi2_contingency(tab)
        tests.append({
            "variable": col, "n": int(tab.to_numpy().sum()), "chi2": chi2,
            "df": dof, "p_value": pv, "cramers_v": cramers_v(tab),
            "min_expected": float(exp.min()),
            "expected_cells_below_5_pct": float((exp < 5).mean() * 100)
        })
        tab.to_csv(out / f"crosstab_{col}.csv")
    tdf = pd.DataFrame(tests)
    if not tdf.empty:
        order = np.argsort(tdf.p_value.to_numpy())
        raw = tdf.p_value.to_numpy()[order]
        adj = np.maximum.accumulate(np.minimum(1, raw * (len(raw) - np.arange(len(raw)))))
        tdf["p_holm"] = np.nan
        tdf.loc[order, "p_holm"] = adj
        tdf = tdf.sort_values("p_value")
    tdf.to_csv(out / "categorical_association_tests.csv", index=False)
    # Effect-size chart for the strongest categorical associations.
    if not tdf.empty:
        plotdf = tdf.head(10).sort_values("cramers_v")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(plotdf["variable"], plotdf["cramers_v"])
        ax.set(title="Cramers V — synthetic categorical associations", xlabel="Cramers V", ylabel="Variable")
        fig.tight_layout()
        fig.savefig(out / "categorical_effect_sizes.png", dpi=160)
        plt.close(fig)

    # Age: Welch's t-test and Mann-Whitney U are both reported.
    age_result = {}
    if "age" in df:
        no = df.loc[df[Y] == 0, "age"].dropna()
        yes = df.loc[df[Y] == 1, "age"].dropna()
        if len(no) and len(yes):
            tr = ttest_ind(no, yes, equal_var=False)
            ur = mannwhitneyu(no, yes, alternative="two-sided")
            age_result = {
                "no_n": len(no), "yes_n": len(yes), "no_mean": no.mean(),
                "yes_mean": yes.mean(), "no_median": no.median(),
                "yes_median": yes.median(), "welch_t": tr.statistic,
                "welch_p": tr.pvalue, "mann_whitney_u": ur.statistic,
                "mann_whitney_p": ur.pvalue
            }
    pd.DataFrame([age_result]).to_csv(out / "age_group_comparison.csv", index=False)

    # Predictive model uses only plausible pre-outcome fields, never post-outcome fields.
    available = [c for c in PREDICTORS if c in df.columns]
    md = df[available + [Y]].dropna()
    X = pd.get_dummies(md[available], drop_first=True, dtype=float)
    y = md[Y].astype(int)
    metrics = {}
    if len(X) > 30 and y.nunique() == 2:
        Xtr, Xte, ytr, yte = train_test_split(
            X, y, test_size=0.25, random_state=2026, stratify=y
        )
        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, random_state=2026))
        model.fit(Xtr, ytr)
        pred, prob = model.predict(Xte), model.predict_proba(Xte)[:, 1]
        metrics = {
            "n_complete": len(X), "n_train": len(Xtr), "n_test": len(Xte),
            "accuracy": accuracy_score(yte, pred),
            "precision": precision_score(yte, pred, zero_division=0),
            "recall": recall_score(yte, pred, zero_division=0),
            "roc_auc": roc_auc_score(yte, prob),
            "confusion_matrix_tn_fp_fn_tp": confusion_matrix(yte, pred).ravel().tolist()
        }
        coef = model.named_steps["logisticregression"].coef_[0]
        cdf = pd.DataFrame({"feature": X.columns, "standardized_log_odds": coef})
        cdf["odds_ratio_per_sd"] = np.exp(cdf.standardized_log_odds)
        cdf.reindex(cdf.standardized_log_odds.abs().sort_values(ascending=False).index).to_csv(
            out / "logistic_coefficients.csv", index=False
        )
    pd.DataFrame([metrics]).to_csv(out / "logistic_model_metrics.csv", index=False)

    lines = [
        "# Statistical Analysis Report — SYNTHETIC DATA ONLY", "",
        "> WARNING: These are simulated practice records, not observations from Bangladesh.",
        "> Do not report these results as real prevalence, risk factors, or thesis findings.", "",
        "## Data validation",
        f"- Shape: {df.shape[0]} rows x {df.shape[1]} columns",
        f"- Duplicate rows: {int(df.duplicated().sum())}",
        f"- Unique IDs: {df[ID].nunique()}",
        f"- Simulated positive outcome: {df[Y].mean()*100:.2f}%", "",
        "## Analyses",
        "- Descriptive statistics and missing-data profile",
        "- Categorical cross-tabs, chi-square tests, Cramér's V and Holm correction",
        "- Welch t-test and Mann–Whitney U test for age",
        "- Holdout logistic regression using pre-outcome predictors only", "",
        "## Strongest categorical associations by unadjusted p-value", "",
        "| Variable | Chi-square | df | p-value | Cramér's V | Holm p |",
        "|---|---:|---:|---:|---:|---:|"
    ]
    for _, r in tdf.head(10).iterrows():
        lines.append(f"| {r['variable']} | {r['chi2']:.3f} | {int(r['df'])} | {r['p_value']:.3g} | {r['cramers_v']:.3f} | {r['p_holm']:.3g} |")
    significant = tdf[tdf["p_holm"] < 0.05]["variable"].tolist() if not tdf.empty else []
    lines += ["", "Variables with Holm-adjusted p < 0.05 in this synthetic dataset: " +
              (", ".join(significant) if significant else "none") + ".",
              "This is a description of the simulation only, not a claim about real people.",
              "", "## Logistic model holdout metrics", ""]
    lines += [f"- {k}: {v}" for k, v in metrics.items()] if metrics else ["Model not fitted: insufficient complete data."]
    lines += [
        "", "## Limitations",
        "- Simulated data cannot establish facts about Bangladesh or its population.",
        "- Association is not causation; p-values do not measure practical importance.",
        "- Check expected cell counts before relying on chi-square approximations.",
        "- A random holdout is not external validation.",
        "- Logistic coefficients are predictive associations, not causal effects.",
        "- Recover the original dataset and its codebook before reproducing thesis findings.",
        "", "## Reproducibility",
        "Run from this project folder: python src/statistical_analysis.py"
    ]
    (out / "statistical_analysis_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Completed. Results saved to {out}. SYNTHETIC DATA ONLY.")

if __name__ == "__main__":
    main()
