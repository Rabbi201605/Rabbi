# Original Dataset Recovery Checklist

Source recorded in the thesis notes:
- Creator: Mostafa Mohiuddin Jalal Protik
- Dataset: Drug Addiction in Bangladesh – Reasons
- Kaggle URL: https://www.kaggle.com/protikmostafa/drug-addiction-in-bangladesh-reasons

## Current status
The Kaggle page could not be independently accessed during this session. The original CSV is therefore not recovered or validated. The synthetic CSV in this repository is a separate practice dataset and is not a replacement.

## Recovery steps
1. Open the Kaggle dataset page while signed in.
2. Download the original archive if it is still available.
3. Check the license and terms before sharing or committing any copy.
4. Keep the original file unchanged in the local data/raw folder.
5. Record download date, original filename, dimensions, column names, and SHA-256.
6. Compare the authentic codebook with the thesis variable coding before analysis.
7. Run the original-data EDA script only after the schema and coding are verified.

Kaggle CLI command (requires the user's own Kaggle API credentials):
```bash
kaggle datasets download -d protikmostafa/drug-addiction-in-bangladesh-reasons -p data/raw
```
