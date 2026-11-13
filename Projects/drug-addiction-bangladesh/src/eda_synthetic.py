"""EDA for the synthetic practice dataset only; not real survey evidence."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_drug_addiction_bangladesh.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
if df.shape != (1426, 26):
    raise ValueError(f"Expected 1,426 rows x 26 columns; found {df.shape}")

overview = pd.DataFrame({
    "metric": ["rows", "columns", "duplicate_rows", "simulated_ever_use_percent"],
    "value": [len(df), len(df.columns), int(df.duplicated().sum()),
              round(df["ever_taken_drug"].mean() * 100, 2)]
})
overview.to_csv(OUT / "synthetic_data_overview.csv", index=False)
df.describe(include="all").T.to_csv(OUT / "synthetic_descriptive_summary.csv")
pd.crosstab(df["smoking_status"], df["ever_taken_drug"]).to_csv(
    OUT / "synthetic_smoking_by_outcome.csv"
)
counts = df["ever_taken_drug"].value_counts().reindex([0, 1], fill_value=0)
ax = counts.plot(kind="bar")
ax.set_xticklabels(["No", "Yes"], rotation=0)
ax.set_title("Synthetic outcome distribution")
ax.set_xlabel("Ever taken drugs")
ax.set_ylabel("Simulated records")
plt.tight_layout()
plt.savefig(OUT / "synthetic_outcome_distribution.png", dpi=160)
plt.close()
print("Synthetic EDA complete. Do not interpret these results as real-world evidence.")
