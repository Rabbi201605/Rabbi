# Synthetic Healthcare Admissions Dataset

**IMPORTANT: This dataset is simulated. It contains no real patients, hospitals, or records.** The relationships between variables (for example, cost by department) are invented for practice. Do not present any result from this file as evidence about real healthcare.

- File: `synthetic_healthcare_patients.csv`
- Generator: `generate_synthetic_healthcare.py` (seeded; the same command always gives the same file)
- Rows: 2,010 (2,000 unique records plus 10 deliberately duplicated rows)
- Columns: 13
- Seed: 42
- Used in: [Healthcare Dashboard project](../../Projects/healthcare-dashboard/)

Regenerate with:
```bash
python generate_synthetic_healthcare.py --rows 2000 --seed 42 --output synthetic_healthcare_patients.csv
```

## Deliberate imperfections (for cleaning practice)
- 10 exact duplicate rows
- 60 missing values in `satisfaction_score`
- 20 missing values in `insurance_type`

## Data dictionary
| Column | Type | Description |
|---|---|---|
| patient_id | text | Synthetic identifier (P100000 onward) |
| admission_date | date | Simulated admission date, 2023-01-01 to 2024-12-30 |
| discharge_date | date | Admission date plus length of stay |
| age | integer | Age in years (0-95); Pediatrics is under 15, Obstetrics is 18-41 |
| gender | category | Male / Female (Obstetrics is all Female) |
| division | category | One of Bangladesh's eight divisions (simulated share per division) |
| department | category | General Medicine, Cardiology, Orthopedics, Pediatrics, Obstetrics, Surgery |
| diagnosis_category | category | Broad diagnosis group, depends on department |
| insurance_type | category | Uninsured, Private, Government scheme, Employer |
| length_of_stay_days | integer | Days admitted (1-19 in this file) |
| total_cost_bdt | integer | Simulated total cost in BDT, rounded to the nearest 50 |
| readmitted_30d | category | Yes / No, readmitted within 30 days |
| satisfaction_score | integer | Simulated patient rating, 1 (low) to 5 (high) |

## Appropriate use
Practising data cleaning, Python and Power BI dashboards, descriptive statistics, and group comparisons.

## Not appropriate
Reporting any figure as a real healthcare finding, or mixing this file with real data.
