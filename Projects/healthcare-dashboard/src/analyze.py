"""Exploratory and statistical analysis of the cleaned healthcare data.

Run prepare_data.py first. Every number in the findings report is written by
this script from the data, nothing is typed in by hand.

If the input is the synthetic practice dataset, all results describe the
simulation only and say nothing about real healthcare.

Usage (from the project folder):
    python src/analyze.py --input data/processed/healthcare_clean.csv --output outputs
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, kruskal, spearmanr

AGE_BINS = [-1, 14, 29, 44, 59, 200]
AGE_LABELS = ["0-14", "15-29", "30-44", "45-59", "60+"]
REQUIRED = {
    "admission_date", "age", "department", "insurance_type", "length_of_stay_days",
    "total_cost_bdt", "readmitted_30d", "satisfaction_score",
}


def cramers_v(table: pd.DataFrame) -> float:
    chi2 = chi2_contingency(table, correction=False)[0]
    n = table.to_numpy().sum()
    k = min(table.shape) - 1
    return float(np.sqrt(chi2 / (n * k))) if n and k else float("nan")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--input", default="data/processed/healthcare_clean.csv")
    parser.add_argument("--output", default="outputs")
    parser.add_argument("--synthetic", action="store_true", default=True,
                        help="Label results as synthetic (default). Use --no-synthetic for real data.")
    parser.add_argument("--no-synthetic", dest="synthetic", action="store_false")
    args = parser.parse_args()

    path, out = Path(args.input), Path(args.output)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run src/prepare_data.py first.")
    df = pd.read_csv(path, parse_dates=["admission_date"])
    missing_cols = REQUIRED - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {sorted(missing_cols)}")
    out.mkdir(parents=True, exist_ok=True)

    df["age_group"] = pd.cut(df["age"], bins=AGE_BINS, labels=AGE_LABELS)
    df["readmit_flag"] = (df["readmitted_30d"] == "Yes").astype(int)

    # 1. Department summary
    dept = (
        df.groupby("department")
        .agg(patients=("age", "size"), mean_los_days=("length_of_stay_days", "mean"),
             mean_cost_bdt=("total_cost_bdt", "mean"), median_cost_bdt=("total_cost_bdt", "median"),
             readmission_rate_pct=("readmit_flag", lambda s: s.mean() * 100))
        .round(1).sort_values("mean_cost_bdt", ascending=False)
    )
    dept.to_csv(out / "department_summary.csv")
    groups = [g["total_cost_bdt"].to_numpy() for _, g in df.groupby("department")]
    kw_stat, kw_p = kruskal(*groups)

    # 2. Readmission by age group and by insurance
    age_tab = pd.crosstab(df["age_group"], df["readmitted_30d"])
    age_chi2, age_p, age_dof, age_exp = chi2_contingency(age_tab)
    age_rate = (df.groupby("age_group", observed=True)["readmit_flag"].mean() * 100).round(1)
    age_rate.rename("readmission_rate_pct").to_csv(out / "readmission_by_age_group.csv")

    ins = df.dropna(subset=["insurance_type"])
    ins_tab = pd.crosstab(ins["insurance_type"], ins["readmitted_30d"])
    ins_chi2, ins_p, ins_dof, _ = chi2_contingency(ins_tab)

    # 3. Correlations
    los_cost = spearmanr(df["length_of_stay_days"], df["total_cost_bdt"])
    sat = df.dropna(subset=["satisfaction_score"])
    los_sat = spearmanr(sat["length_of_stay_days"], sat["satisfaction_score"])

    # 4. Monthly admissions
    monthly = df.set_index("admission_date").resample("MS").size().rename("admissions")
    monthly.to_csv(out / "monthly_admissions.csv")

    # Charts
    fig, ax = plt.subplots(figsize=(8, 4.5))
    dept["mean_cost_bdt"].sort_values().plot.barh(ax=ax)
    ax.set(title="Mean total cost by department (synthetic data)" if args.synthetic
           else "Mean total cost by department", xlabel="BDT", ylabel="")
    fig.tight_layout(); fig.savefig(out / "cost_by_department.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    age_rate.plot.bar(ax=ax, rot=0)
    ax.set(title="30-day readmission rate by age group" + (" (synthetic)" if args.synthetic else ""),
           xlabel="Age group", ylabel="Readmission rate (%)")
    fig.tight_layout(); fig.savefig(out / "readmission_by_age_group.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4))
    monthly.plot(ax=ax)
    ax.set(title="Monthly admissions" + (" (synthetic)" if args.synthetic else ""),
           xlabel="Month", ylabel="Admissions")
    fig.tight_layout(); fig.savefig(out / "monthly_admissions.png", dpi=160); plt.close(fig)

    # Findings report: all values come from the results above.
    def p_fmt(p: float) -> str:
        return "< 0.001" if p < 0.001 else f"{p:.3f}"

    top, bottom = dept.index[0], dept.index[-1]
    warn = ([
        "> WARNING: SYNTHETIC DATA. These results describe a simulation and say nothing about real patients or hospitals.",
        "",
    ] if args.synthetic else [])
    low_cells = float((age_exp < 5).mean() * 100)
    lines = [
        "# Healthcare Analysis: Findings", "", *warn,
        "## Data",
        f"- Records analysed: {len(df):,}",
        f"- Admission dates: {df['admission_date'].min():%Y-%m-%d} to {df['admission_date'].max():%Y-%m-%d}",
        f"- Missing `insurance_type`: {int(df['insurance_type'].isna().sum())}; "
        f"missing `satisfaction_score`: {int(df['satisfaction_score'].isna().sum())} (excluded from the tests that use them)",
        f"- Overall 30-day readmission rate: {df['readmit_flag'].mean() * 100:.1f}%", "",
        "## Cost and length of stay by department",
        dept.to_markdown(), "",
        f"- Highest mean cost: {top} ({dept.loc[top, 'mean_cost_bdt']:,.0f} BDT); lowest: {bottom} ({dept.loc[bottom, 'mean_cost_bdt']:,.0f} BDT).",
        f"- Kruskal-Wallis test of cost across departments: H = {kw_stat:.1f}, p {p_fmt(kw_p)}.",
        f"- Spearman correlation, length of stay vs cost: rho = {los_cost.statistic:.2f}, p {p_fmt(los_cost.pvalue)}.", "",
        "## Readmission",
        age_rate.to_frame("readmission_rate_pct").to_markdown(), "",
        f"- Readmission vs age group: chi-square = {age_chi2:.2f}, df = {age_dof}, p {p_fmt(age_p)}, Cramér's V = {cramers_v(age_tab):.3f}.",
        f"- Readmission vs insurance type: chi-square = {ins_chi2:.2f}, df = {ins_dof}, p {p_fmt(ins_p)}, Cramér's V = {cramers_v(ins_tab):.3f}.", "",
        "## Patient satisfaction",
        f"- Spearman correlation, length of stay vs satisfaction: rho = {los_sat.statistic:.2f}, p {p_fmt(los_sat.pvalue)} (n = {len(sat):,}).", "",
        "## Charts",
        "![Cost by department](cost_by_department.png)",
        "![Readmission by age group](readmission_by_age_group.png)",
        "![Monthly admissions](monthly_admissions.png)", "",
        "## Limitations",
        "- Observational data: associations do not show cause and effect.",
        "- Several tests were run without a multiple-comparison correction; treat single p-values cautiously.",
        f"- {low_cells:.0f}% of expected counts in the age-group readmission table are below 5." +
        (" The chi-square approximation may be unreliable." if low_cells > 20 else ""),
        "- Costs are right-skewed, so medians are shown next to means.",
        ("- The data are simulated; the relationships found were built into the simulation." if args.synthetic
         else "- Check the dataset's source and sampling before generalising."),
        "", "## Reproducibility",
        "```bash",
        "python src/prepare_data.py --input ../../Datasets/synthetic-healthcare/synthetic_healthcare_patients.csv --output data/processed",
        "python src/analyze.py",
        "```",
    ]
    (out / "findings.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote findings and charts to {out.resolve()}")


if __name__ == "__main__":
    main()
