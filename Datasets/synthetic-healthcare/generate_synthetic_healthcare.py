"""Generate a SYNTHETIC hospital-admissions dataset for practice and demos.

Every value is randomly generated. No real patients, hospitals, or records are
involved, and the relationships between variables are invented for practice.
Do not use results from this file as evidence about real healthcare.

The generator is seeded, so running it again produces the same file.
A few missing values and duplicate rows are added on purpose so that data
cleaning steps have something realistic to work on.

Usage:
    python generate_synthetic_healthcare.py --rows 2000 --seed 42 \
        --output synthetic_healthcare_patients.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

DEPARTMENTS = ["General Medicine", "Cardiology", "Orthopedics", "Pediatrics", "Obstetrics", "Surgery"]
DEPT_WEIGHTS = [0.30, 0.15, 0.12, 0.15, 0.13, 0.15]
DEPT_BASE_COST = {  # invented average daily cost in BDT
    "General Medicine": 4000,
    "Cardiology": 9000,
    "Orthopedics": 8000,
    "Pediatrics": 3500,
    "Obstetrics": 6000,
    "Surgery": 12000,
}
DEPT_BASE_STAY = {
    "General Medicine": 4,
    "Cardiology": 5,
    "Orthopedics": 6,
    "Pediatrics": 3,
    "Obstetrics": 3,
    "Surgery": 6,
}
DIAGNOSES = {
    "General Medicine": ["Infection", "Diabetes-related", "Respiratory", "Gastrointestinal"],
    "Cardiology": ["Hypertension-related", "Cardiac", "Diabetes-related"],
    "Orthopedics": ["Fracture", "Joint disorder"],
    "Pediatrics": ["Infection", "Respiratory", "Gastrointestinal"],
    "Obstetrics": ["Childbirth", "Pregnancy complication"],
    "Surgery": ["Appendicitis", "Hernia", "Injury", "Gastrointestinal"],
}
DIVISIONS = ["Dhaka", "Chattogram", "Rajshahi", "Khulna", "Barishal", "Sylhet", "Rangpur", "Mymensingh"]
DIVISION_WEIGHTS = [0.28, 0.16, 0.13, 0.10, 0.06, 0.07, 0.11, 0.09]
INSURANCE = ["Uninsured", "Private", "Government scheme", "Employer"]
INSURANCE_WEIGHTS = [0.55, 0.15, 0.15, 0.15]


def build(rows: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    department = rng.choice(DEPARTMENTS, rows, p=DEPT_WEIGHTS)
    gender = np.where(department == "Obstetrics", "Female", rng.choice(["Male", "Female"], rows))

    age = np.empty(rows, dtype=int)
    for i, dept in enumerate(department):
        if dept == "Pediatrics":
            age[i] = rng.integers(0, 15)
        elif dept == "Obstetrics":
            age[i] = rng.integers(18, 42)
        elif dept in ("Cardiology", "Orthopedics"):
            age[i] = int(np.clip(rng.normal(58, 14), 18, 95))
        else:
            age[i] = int(np.clip(rng.normal(42, 20), 1, 95))

    diagnosis = np.array([rng.choice(DIAGNOSES[d]) for d in department])

    base_stay = np.array([DEPT_BASE_STAY[d] for d in department], dtype=float)
    age_effect = np.where(age >= 60, 1.5, 0.0)
    stay = np.clip(rng.poisson(base_stay + age_effect) + 1, 1, 30)

    admission = pd.Timestamp("2023-01-01") + pd.to_timedelta(rng.integers(0, 730, rows), unit="D")
    discharge = admission + pd.to_timedelta(stay, unit="D")

    daily_cost = np.array([DEPT_BASE_COST[d] for d in department], dtype=float)
    cost = daily_cost * stay * rng.lognormal(mean=0.0, sigma=0.25, size=rows)
    cost = (np.round(cost / 50) * 50).astype(int)

    readmit_p = 0.06 + 0.004 * np.clip(age - 40, 0, None) / 5 + 0.01 * np.clip(stay - 5, 0, None)
    readmit_p = np.clip(readmit_p, 0.02, 0.35)
    readmitted = np.where(rng.random(rows) < readmit_p, "Yes", "No")

    satisfaction = np.clip(np.round(rng.normal(3.9 - 0.04 * np.clip(stay - 4, 0, None), 0.9)), 1, 5)

    df = pd.DataFrame(
        {
            "patient_id": [f"P{100000 + i}" for i in range(rows)],
            "admission_date": admission.strftime("%Y-%m-%d"),
            "discharge_date": discharge.strftime("%Y-%m-%d"),
            "age": age,
            "gender": gender,
            "division": rng.choice(DIVISIONS, rows, p=DIVISION_WEIGHTS),
            "department": department,
            "diagnosis_category": diagnosis,
            "insurance_type": rng.choice(INSURANCE, rows, p=INSURANCE_WEIGHTS),
            "length_of_stay_days": stay,
            "total_cost_bdt": cost,
            "readmitted_30d": readmitted,
            "satisfaction_score": satisfaction.astype(int),
        }
    )

    # Deliberate imperfections for cleaning practice.
    miss_sat = rng.choice(rows, size=int(rows * 0.03), replace=False)
    df.loc[miss_sat, "satisfaction_score"] = pd.NA
    df["satisfaction_score"] = df["satisfaction_score"].astype("Int64")
    miss_ins = rng.choice(rows, size=int(rows * 0.01), replace=False)
    df.loc[miss_ins, "insurance_type"] = pd.NA
    dupes = df.sample(10, random_state=seed)
    df = pd.concat([df, dupes], ignore_index=True)

    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--rows", type=int, default=2000, help="Number of unique records.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--output", default="synthetic_healthcare_patients.csv")
    args = parser.parse_args()

    df = build(args.rows, args.seed)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Wrote {len(df):,} rows ({args.rows:,} unique + 10 duplicates) to {out.resolve()}")


if __name__ == "__main__":
    main()
