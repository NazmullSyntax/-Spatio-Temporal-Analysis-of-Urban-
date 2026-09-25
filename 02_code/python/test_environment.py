"""Test that the project dependencies import and Matplotlib can save a plot."""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import scipy
import sklearn
import statsmodels
import xgboost

print("=" * 50)
print("Environment Check")
print("=" * 50)
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"GeoPandas: {gpd.__version__}")
print(f"Rasterio: {rasterio.__version__}")
print(f"Scikit-learn: {sklearn.__version__}")
print(f"XGBoost: {xgboost.__version__}")
print(f"SciPy: {scipy.__version__}")
print(f"Statsmodels: {statsmodels.__version__}")
print("=" * 50)
print("All libraries working!")
print("=" * 50)

years = [2000, 2005, 2010, 2015, 2020, 2025]
green_placeholder = [100, 92, 80, 68, 55, 45]

plt.figure(figsize=(10, 6))
plt.plot(years, green_placeholder, "o-", color="green", linewidth=2, markersize=10)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Green Space (km²)", fontsize=12)
plt.title("Test Plot: Green Space Trend", fontsize=14)
plt.grid(True, alpha=0.3)

project_root = Path(__file__).resolve().parents[2]
output_path = project_root / "03_results/figures/test_plot.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"\nTest plot saved to {output_path}")
