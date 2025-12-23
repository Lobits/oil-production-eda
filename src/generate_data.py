# src/generate_data.py
import numpy as np
import pandas as pd
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)
np.random.seed(42)

n_wells = 5
months = 48
start_date = datetime(2019, 1, 1)

rows = []
for well_id in range(1, n_wells + 1):
    base = 5000 - well_id * 200
    for m in range(months):
        date = start_date + pd.DateOffset(months=m)
        well_age_months = m + np.random.randint(-2, 3)
        seasonal = 1 + 0.1 * np.sin(2 * np.pi * (date.month - 1) / 12)
        pressure = 3000 - 2 * m + np.random.normal(0, 25)
        decline = np.exp(-0.01 * m)
        prod = base * decline * seasonal + 0.02 * pressure + np.random.normal(0, 80)
        rows.append({
            "well_id": f"W{well_id:02d}",
            "date": date.strftime("%Y-%m-%d"),
            "well_age_months": max(0, well_age_months),
            "pressure": max(0, pressure),
            "oil_production_bbl": max(0, prod)
        })

df = pd.DataFrame(rows)
for col in ["pressure", "oil_production_bbl"]:
    df.loc[df.sample(frac=0.02, random_state=1).index, col] = np.nan

df.to_csv("data/production.csv", index=False)
print("Saved data/production.csv — rows:", len(df))
