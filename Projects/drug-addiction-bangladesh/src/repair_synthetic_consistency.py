"""Repair age-related impossibilities in the SYNTHETIC practice dataset.

The simulated records contained combinations that cannot occur in real life,
such as a 15-year-old postgraduate or a 14-year-old in full-time employment.
This script applies simple, documented rules and writes a log of every change.

Rules (applied in this order):
1. Education must be plausible for age:
   - under 16: at most Secondary
   - 16-17: at most Higher secondary
   - 18-21: at most Undergraduate
2. Under 16: Employed / Self-employed becomes Student.
3. Income must be plausible: under 16 students have "No income"; anyone under
   18 with "High" income becomes "Low".

The script is idempotent: running it again changes nothing. Changes are drawn
with a fixed seed so the result is reproducible.

Usage (from the project folder):
    python src/repair_synthetic_consistency.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261113
LEVELS = ["No formal education", "Primary", "Secondary", "Higher secondary", "Undergraduate", "Postgraduate"]
MAX_LEVEL_BY_AGE = [(16, "Secondary"), (18, "Higher secondary"), (22, "Undergraduate")]


def max_level(age: int) -> str | None:
    for limit, level in MAX_LEVEL_BY_AGE:
        if age < limit:
            return level
    return None


def repair(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    df = df.copy()
    log: list[dict] = []

    def change(idx: int, column: str, new: str, rule: str) -> None:
        old = df.at[idx, column]
        if old != new:
            log.append({"respondent_id": df.at[idx, "respondent_id"], "column": column,
                        "old_value": old, "new_value": new, "rule": rule})
            df.at[idx, column] = new

    for idx in df.index:
        age = int(df.at[idx, "age"])

        cap = max_level(age)
        if cap is not None and LEVELS.index(df.at[idx, "education_level"]) > LEVELS.index(cap):
            lower = LEVELS.index(cap)
            choices = LEVELS[max(lower - 1, 0): lower + 1]
            change(idx, "education_level", str(rng.choice(choices)), "education too high for age")

        if age < 16 and df.at[idx, "employment_status"] in ("Employed", "Self-employed"):
            change(idx, "employment_status", "Student", "employment not plausible under 16")

        if age < 16 and df.at[idx, "employment_status"] == "Student":
            change(idx, "monthly_income_group", "No income", "student under 16 has no income")
        if age < 18 and df.at[idx, "monthly_income_group"] == "High":
            change(idx, "monthly_income_group", "Low", "high income not plausible under 18")

    return df, pd.DataFrame(log, columns=["respondent_id", "column", "old_value", "new_value", "rule"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--input", default="data/synthetic_drug_addiction_bangladesh.csv")
    parser.add_argument("--log", default="docs/synthetic_data_repair_log.csv")
    args = parser.parse_args()

    path = Path(args.input)
    df = pd.read_csv(path)
    fixed, log = repair(df)

    if log.empty:
        print("No inconsistencies found; nothing changed.")
        return

    fixed.to_csv(path, index=False)
    Path(args.log).parent.mkdir(parents=True, exist_ok=True)
    log.to_csv(args.log, index=False)
    print(f"Changed {log.respondent_id.nunique()} respondents ({len(log)} values). Log: {args.log}")
    print(log.groupby("rule").size().to_string())


if __name__ == "__main__":
    main()
