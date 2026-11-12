# Healthcare Data Analysis and Power BI Dashboard

## Project Overview
A portfolio project that cleans and explores a public healthcare dataset with Python and presents the results in a Power BI dashboard.

## Status
**In progress.** The data-preparation script is ready. The dataset, analysis, and dashboard have not been added yet, so no findings are reported here.

## Dataset
- Source: _to be added (public Kaggle healthcare dataset)_
- License / terms of use: _to be verified before the data is shared_
- Rows / columns: _to be filled after loading_

The raw file is not committed. Download it from the original source and place it at `data/raw/healthcare.csv`.

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
python src/prepare_data.py --input data/raw/healthcare.csv --output data/processed
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
