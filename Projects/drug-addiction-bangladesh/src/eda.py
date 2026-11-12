"""Basic, reproducible EDA for a permitted CSV survey dataset.

This script intentionally does not assume the meaning of coded columns.
Use the original dataset codebook before interpreting any variable.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Create basic EDA outputs for a CSV file.")
    parser.add_argument("--input", required=True, help="Path to the source CSV file.")
    parser.add_argument("--output", default="outputs", help="Directory for generated outputs.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {input_path}. Obtain the dataset from its source "
            "and place it at the path supplied with --input."
        )

    df = pd.read_csv(input_path)

    # Basic structure and quality checks
    overview = pd.DataFrame({
        "metric": ["rows", "columns", "duplicate_rows"],
        "value": [len(df), len(df.columns), int(df.duplicated().sum())],
    })
    overview.to_csv(output_dir / "data_overview.csv", index=False)

    missing = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_percent": (df.isna().mean().values * 100).round(2),
        "data_type": df.dtypes.astype(str).values,
    })
    missing.to_csv(output_dir / "missing_values.csv", index=False)

    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        numeric.describe().T.to_csv(output_dir / "numeric_descriptive_statistics.csv")
        if numeric.shape[1] >= 2:
            numeric.corr().to_csv(output_dir / "numeric_correlation_matrix.csv")

    # Frequency tables are generated for non-numeric columns.
    categorical = df.select_dtypes(exclude="number")
    for column in categorical.columns:
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in str(column))
        df[column].value_counts(dropna=False).rename_axis("value").reset_index(
            name="count"
        ).to_csv(output_dir / f"frequency_{safe_name}.csv", index=False)

    # Missingness chart
    missing_counts = df.isna().sum().sort_values(ascending=False)
    if (missing_counts > 0).any():
        ax = missing_counts[missing_counts > 0].plot(kind="bar", figsize=(10, 5))
        ax.set_title("Missing Values by Column")
        ax.set_xlabel("Column")
        ax.set_ylabel("Missing count")
        plt.tight_layout()
        plt.savefig(output_dir / "missing_values.png", dpi=150)
        plt.close()

    print(f"EDA completed for {len(df):,} rows and {len(df.columns):,} columns.")
    print(f"Outputs saved to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
