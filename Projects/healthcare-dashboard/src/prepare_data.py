"""Clean a healthcare CSV and export a tidy file for Power BI.

Steps (all reported in a cleaning log, nothing is changed silently):
1. Standardise column names to snake_case.
2. Trim whitespace in text columns.
3. Parse columns whose names contain "date" as dates.
4. Drop exact duplicate rows.
5. Write the cleaned data and a summary of what changed.

The script does not impute or remove missing values; decisions about missing
data should be made deliberately and documented in the README.

Example:
    python src/prepare_data.py --input data/raw/healthcare.csv --output data/processed
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


def to_snake_case(name: str) -> str:
    name = re.sub(r"[^0-9a-zA-Z]+", "_", str(name).strip())
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return re.sub(r"_+", "_", name).strip("_").lower()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--input", required=True, help="Path to the source CSV file.")
    parser.add_argument("--output", default="data/processed", help="Output directory.")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {input_path}. Download it from its source, check the "
            "license, and place it at the path supplied with --input."
        )

    df = pd.read_csv(input_path)
    log: list[tuple[str, object]] = [
        ("rows_in", len(df)),
        ("columns_in", len(df.columns)),
    ]

    renamed = {c: to_snake_case(c) for c in df.columns}
    df = df.rename(columns=renamed)
    log.append(("columns_renamed", sum(1 for a, b in renamed.items() if a != b)))

    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip()
    log.append(("text_columns_trimmed", len(text_cols)))

    parsed = []
    for col in df.columns:
        if "date" in col:
            converted = pd.to_datetime(df[col], errors="coerce")
            newly_missing = int(converted.isna().sum() - df[col].isna().sum())
            df[col] = converted
            parsed.append(f"{col} (unparseable values set to missing: {newly_missing})")
    log.append(("date_columns_parsed", "; ".join(parsed) if parsed else "none"))

    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates()
    log.append(("exact_duplicates_removed", duplicates))
    log.append(("rows_out", len(df)))
    log.append(("missing_cells_remaining", int(df.isna().sum().sum())))

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "healthcare_clean.csv", index=False)
    pd.DataFrame(log, columns=["step", "result"]).to_csv(
        output_dir / "cleaning_log.csv", index=False
    )

    for step, result in log:
        print(f"{step}: {result}")
    print(f"Cleaned file saved to: {(output_dir / 'healthcare_clean.csv').resolve()}")


if __name__ == "__main__":
    main()
