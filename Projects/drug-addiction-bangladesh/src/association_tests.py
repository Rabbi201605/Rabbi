"""Chi-square tests of association between one outcome column and other columns.

For each predictor column the script reports the chi-square statistic, degrees
of freedom, p-value, Cramer's V, and a warning when expected cell counts are
too small for the chi-square approximation to be reliable.

The script does not assume what any coded value means. Read the original
codebook before interpreting the results.

Example:
    python src/association_tests.py \
        --input data/raw/drug_addiction_bangladesh.csv \
        --outcome <outcome_column> \
        --output outputs
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


def cramers_v(table: pd.DataFrame) -> float:
    """Cramer's V (uncorrected) for a contingency table."""
    chi2 = chi2_contingency(table, correction=False)[0]
    n = table.to_numpy().sum()
    min_dim = min(table.shape) - 1
    if n == 0 or min_dim == 0:
        return float("nan")
    return float(np.sqrt(chi2 / (n * min_dim)))


def test_column(df: pd.DataFrame, outcome: str, column: str) -> dict:
    subset = df[[outcome, column]].dropna()
    table = pd.crosstab(subset[outcome], subset[column])
    if table.shape[0] < 2 or table.shape[1] < 2:
        return {
            "variable": column,
            "n": len(subset),
            "chi_square": np.nan,
            "dof": np.nan,
            "p_value": np.nan,
            "cramers_v": np.nan,
            "pct_cells_expected_below_5": np.nan,
            "note": "Fewer than two categories after removing missing values.",
        }
    chi2, p_value, dof, expected = chi2_contingency(table)
    pct_low = float((expected < 5).mean() * 100)
    note = ""
    if pct_low > 20:
        note = "More than 20% of expected counts are below 5; interpret with caution."
    return {
        "variable": column,
        "n": int(table.to_numpy().sum()),
        "chi_square": round(float(chi2), 3),
        "dof": int(dof),
        "p_value": float(p_value),
        "cramers_v": round(cramers_v(table), 3),
        "pct_cells_expected_below_5": round(pct_low, 1),
        "note": note,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--input", required=True, help="Path to the source CSV file.")
    parser.add_argument("--outcome", required=True, help="Name of the outcome column.")
    parser.add_argument(
        "--columns",
        nargs="*",
        help="Predictor columns to test. Defaults to all other columns.",
    )
    parser.add_argument("--output", default="outputs", help="Directory for results.")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {input_path}. Obtain the dataset from its source "
            "and place it at the path supplied with --input."
        )

    df = pd.read_csv(input_path)
    if args.outcome not in df.columns:
        raise ValueError(
            f"Outcome column '{args.outcome}' not found. Available columns: {list(df.columns)}"
        )

    predictors = args.columns or [c for c in df.columns if c != args.outcome]
    missing = [c for c in predictors if c not in df.columns]
    if missing:
        raise ValueError(f"Columns not found: {missing}")

    results = pd.DataFrame([test_column(df, args.outcome, c) for c in predictors])
    results = results.sort_values("cramers_v", ascending=False, na_position="last")

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "chi_square_results.csv"
    results.to_csv(out_path, index=False)

    print(results.to_string(index=False))
    print(f"\nResults saved to: {out_path.resolve()}")
    print(
        "Note: p-values from many tests are not adjusted for multiple comparisons. "
        "Association does not establish causation."
    )


if __name__ == "__main__":
    main()
