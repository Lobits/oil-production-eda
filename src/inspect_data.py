# inspectData.py — start fresh

# 0. Ensure required modules are installed
import sys
import subprocess

def install_if_missing(package):
    try:
        __import__(package)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check/install required packages
for pkg in ["pandas", "matplotlib", "numpy"]:
    install_if_missing(pkg)

# 1. Imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 2. Make sure output folder exists
os.makedirs("outputs", exist_ok=True)

# 3. Load data
data_path = "data/production.csv"
df = pd.read_csv(data_path, parse_dates=["date"])
print(f"Loaded {len(df)} rows from {data_path}")

# 4. Quick look
print("\n--- First 5 rows ---")
print(df.head())

# 5. Missing values
print("\n--- Missing values per column ---")
print(df.isna().sum())

# 6. Descriptive statistics for numeric columns
desc = df.describe()
print("\n--- Descriptive statistics ---")
print(desc)

# Save numeric descriptive stats to CSV
desc.to_csv("outputs/descriptive_stats.csv")
print("Saved outputs/descriptive_stats.csv")

# 7. Total monthly production plot
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')

monthly = df.groupby('month')['oil_production_bbl'].sum().reset_index()


plt.figure(figsize=(10,4))
monthly.plot(marker='o')
plt.title("Total monthly oil production (all wells)")
plt.xlabel("Date")
plt.ylabel("Oil production (bbl)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/total_monthly_production.png")
plt.show()
plt.close()
print("Saved outputs/total_monthly_production.png")

# 8. Histogram of production values
plt.figure(figsize=(8,4))
df['oil_production_bbl'].dropna().hist(bins=30)
plt.title("Distribution of oil production values")
plt.xlabel("Oil production (bbl)")
plt.ylabel("Count")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/prod_histogram.png")
plt.show()
plt.close()
print("Saved outputs/prod_histogram.png")

# 9. Per-well summary
per_well = df.groupby('well_id')['oil_production_bbl'].describe()
per_well.to_csv("outputs/per_well_summary.csv")
print("Saved outputs/per_well_summary.csv")
print("\n--- Top lines of per-well summary ---")
print(per_well.head())

# 10 Production Summary
monthly.mean()
monthly.min()
monthly.max()
monthly.median()

print(monthly.mean())
print(monthly.min())
print(monthly.max())
print(monthly.median())



