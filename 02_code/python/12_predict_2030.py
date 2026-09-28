"""
2030 Prediction:
- Load trained Gradient Boosting model
- Prepare 2030 features from 2025 baseline
- Predict 2030 LST for each grid cell
- Generate uncertainty estimates
- Create prediction maps
"""
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingRegressor
import os

print("=" * 60)
print("2030 PREDICTION")
print("=" * 60)

# ============================================================
# 1. LOAD DATA AND MODEL
# ============================================================
df = pd.read_csv("01_data/master/dhaka_green_space_master.csv")
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])

print(f"Loaded {len(df)} rows")

model = joblib.load("03_results/models/best_model_lst.pkl")
print("Model loaded: Gradient Boosting")

# ============================================================
# 2. CALCULATE ANNUAL TRENDS (from 2000-2025)
# ============================================================
print()
print("=" * 60)
print("CALCULATING TRENDS (2000-2025)")
print("=" * 60)

# Annual rate of change per grid cell
df_sorted = df.sort_values(['grid_id', 'Year'])

# NDVI change rate
df_2000 = df[df['Year'] == 2000].set_index('grid_id')
df_2025 = df[df['Year'] == 2025].set_index('grid_id')

common = df_2000.index.intersection(df_2025.index)

ndvi_rate = (df_2025.loc[common, 'NDVI'] - df_2000.loc[common, 'NDVI']) / 25
ndbi_rate = (df_2025.loc[common, 'NDBI'] - df_2000.loc[common, 'NDBI']) / 25
lst_night_rate = (df_2025.loc[common, 'LST_Night'] - df_2000.loc[common, 'LST_Night']) / 25

print(f"NDVI change rate: {ndvi_rate.mean():.6f}/year")
print(f"NDBI change rate: {ndbi_rate.mean():.6f}/year")
print(f"LST_Night change rate: {lst_night_rate.mean():.6f}/year")

# ============================================================
# 3. BUILD 2030 FEATURES
# ============================================================
print()
print("=" * 60)
print("BUILDING 2030 FEATURES")
print("=" * 60)

# Start from 2025 data
baseline_2025 = df[df['Year'] == 2025].copy()
baseline_2025 = baseline_2025.set_index('grid_id')

# Population for 2030 (from national trend +5%)
# 2025 population: 23M, 2030 estimate: ~25M
pop_2030_factor = 25_000_000 / 23_000_000

df_2030 = pd.DataFrame(index=baseline_2025.index)
df_2030['NDVI'] = baseline_2025['NDVI'] + ndvi_rate * 5  # +5 years
df_2030['NDBI'] = baseline_2025['NDBI'] + ndbi_rate * 5
df_2030['LST_Night'] = baseline_2025['LST_Night'] + lst_night_rate * 5
df_2030['Population'] = baseline_2025['Population'] * pop_2030_factor
df_2030['Year'] = 2030

# Reset index to use grid_id as column
df_2030 = df_2030.reset_index()

print(f"Built 2030 features for {len(df_2030)} grid cells")
print()
print("Sample 2030 features:")
print(df_2030.head().to_string())

# ============================================================
# 4. PREDICT 2030 LST
# ============================================================
print()
print("=" * 60)
print("PREDICTING 2030 LST")
print("=" * 60)

feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year']
X_2030 = df_2030[feature_cols].values

df_2030['LST_2030_pred'] = model.predict(X_2030)

print(f"Predicted 2030 LST:")
print(f"  Mean:   {df_2030['LST_2030_pred'].mean():.2f}°C")
print(f"  Min:    {df_2030['LST_2030_pred'].min():.2f}°C")
print(f"  Max:    {df_2030['LST_2030_pred'].max():.2f}°C")
print(f"  Std:    {df_2030['LST_2030_pred'].std():.2f}°C")

# Compare to 2025
print()
print(f"2025 mean LST: {baseline_2025['LST'].mean():.2f}°C")
print(f"2030 predicted: {df_2030['LST_2030_pred'].mean():.2f}°C")
print(f"Change: {df_2030['LST_2030_pred'].mean() - baseline_2025['LST'].mean():+.2f}°C")

# ============================================================
# 5. UNCERTAINTY ESTIMATION (Bootstrap)
# ============================================================
print()
print("=" * 60)
print("UNCERTAINTY ESTIMATION (Bootstrap)")
print("=" * 60)

n_bootstrap = 50
predictions = []

for i in range(n_bootstrap):
    # Resample rows for prediction uncertainty
    sample_idx = np.random.choice(len(X_2030), len(X_2030), replace=True)
    X_sample = X_2030[sample_idx]
    pred = model.predict(X_sample)
    predictions.append(pred.mean())

predictions = np.array(predictions)
ci_lower = np.percentile(predictions, 2.5)
ci_upper = np.percentile(predictions, 97.5)

print(f"2030 LST (95% CI):")
print(f"  Point estimate: {predictions.mean():.2f}°C")
print(f"  Lower bound:    {ci_lower:.2f}°C")
print(f"  Upper bound:    {ci_upper:.2f}°C")

# ============================================================
# 6. SAVE PREDICTIONS
# ============================================================
output = df_2030[['grid_id', 'NDVI', 'NDBI', 'LST_Night',
                   'Population', 'LST_2030_pred']].copy()

# Merge coordinates from 2025
coords = df[df['Year'] == 2025][['grid_id', 'lon', 'lat']]
output = output.merge(coords, on='grid_id', how='left')

output.to_csv("03_results/prediction_2030.csv", index=False)
print()
print(f"✅ Prediction saved: 03_results/prediction_2030.csv")
print(f"   Rows: {len(output)}")

# ============================================================
# 7. VISUALIZATION: 2025 vs 2030 MAP
# ============================================================
print()
print("=" * 60)
print("CREATING MAPS")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# 2025 actual
scatter1 = axes[0].scatter(baseline_2025['lon'], baseline_2025['lat'],
                            c=baseline_2025['LST'], cmap='hot_r',
                            s=3, vmin=20, vmax=32)
axes[0].set_title('2025 LST (Actual)', fontsize=16)
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
plt.colorbar(scatter1, ax=axes[0], label='LST (°C)')

# 2030 predicted
scatter2 = axes[1].scatter(output['lon'], output['lat'],
                            c=output['LST_2030_pred'], cmap='hot_r',
                            s=3, vmin=20, vmax=32)
axes[1].set_title('2030 LST (Predicted)', fontsize=16)
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('Latitude')
plt.colorbar(scatter2, ax=axes[1], label='LST (°C)')

plt.tight_layout()
plt.savefig("03_results/maps/prediction_2030_vs_2025.png", dpi=150)
plt.close()

# Distribution comparison
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(baseline_2025['LST'], bins=50, alpha=0.6, color='blue',
        label=f'2025 (mean={baseline_2025["LST"].mean():.2f}°C)', density=True)
ax.hist(output['LST_2030_pred'], bins=50, alpha=0.6, color='red',
        label=f'2030 (mean={output["LST_2030_pred"].mean():.2f}°C)', density=True)
ax.set_xlabel('Land Surface Temperature (°C)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('LST Distribution: 2025 vs 2030 Predicted', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("03_results/figures/lst_2025_vs_2030_distribution.png", dpi=150)
plt.close()

# ============================================================
# 8. ZONE-LEVEL SUMMARY
# ============================================================
print()
print("=" * 60)
print("TOP 10 HOTTEST GRID CELLS IN 2030")
print("=" * 60)

top_hot = output.nlargest(10, 'LST_2030_pred')
print(top_hot[['grid_id', 'lon', 'lat', 'LST_2030_pred']].to_string(index=False))

print()
print("=" * 60)
print("✅ 2030 prediction complete")
print("=" * 60)