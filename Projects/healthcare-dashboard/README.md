# Healthcare Data Analysis and Power BI Dashboard

## Project Overview
A portfolio project that cleans and explores a public healthcare dataset with Python and presents the results in a Power BI dashboard.

## Status
**In progress.** The data-preparation script and a synthetic practice dataset are ready. The analysis and Power BI dashboard have not been built yet, so no findings are reported here.

## Dataset
This project currently uses a **synthetic (simulated) dataset**, not real patient data. See [Datasets/synthetic-healthcare](../../Datasets/synthetic-healthcare/) for the data dictionary and generator.
- Rows / columns: 2,010 x 13 (includes 10 deliberate duplicates and some missing values)
- Any result from it describes the simulation only and must not be presented as a real healthcare finding.

To use a real public dataset instead (for example from Kaggle), record its source and license, then place the file at `data/raw/healthcare.csv`.

## Planned Workflow
1. Download the dataset and record its source and license.
2. Run `src/prepare_data.py` to standardise column names, trim text, parse dates, and remove exact duplicates.
3. Review missing values and decide how to handle them; document each decision here.
4. Explore the data in Python (distributions, group comparisons, trends over time).
5. Load `data/processed/healthcare_clean.csv` into Power BI and build the dashboard.
6. Export dashboard screenshots to `outputs/` and add the key findings and limitations below.

## Run the Data Preparation
```bash
python -m pip install -r requirements.txt
python src/prepare_data.py --input ../../Datasets/synthetic-healthcare/synthetic_healthcare_patients.csv --output data/processed
```

This writes `data/processed/healthcare_clean.csv` and `data/processed/cleaning_log.csv`, which records every change made.

## Repository Structure
```
healthcare-dashboard/
├── data/
│   ├── raw/          # Place the downloaded dataset here (not committed)
│   └── processed/    # Cleaned data and cleaning log (not committed)
├── outputs/          # Dashboard screenshots and figures
├── src/
│   └── prepare_data.py
├── requirements.txt
└── README.md
```

## Dashboard Plan
| Page | Purpose |
|---|---|
| Overview | Headline counts and key totals |
| Patient demographics | Age and gender distributions |
| Clinical / cost view | Comparisons across the dataset's main measures |
| Trends | Changes over time, if the data includes dates |

Final page contents depend on the columns available in the dataset.

## Findings
_To be added after the analysis is run and verified._

## Limitations
_To be added. Consider data source quality, missing values, and whether the data is synthetic._
