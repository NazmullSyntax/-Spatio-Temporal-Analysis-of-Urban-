"""
2030 Prediction — Fixed version
- Uses all available grid cells
- Applies empirical LST trend
- Preserves spatial patterns from ML model
"""
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

print("=" * 60)
print("2030 PREDICTION (FIXED)")
print("=" * 60)

# Load data
df = pd.read_csv("01_data/master/dhaka_green_space_master.csv")
df = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night', 'Population'])
print(f"Loaded {len(df)} rows")

# Load model
model = joblib.load("03_results/models/best_model_lst.pkl")

# ============================================================
# 1. GET BASELINE 2025 (ALL CELLS WITH DATA)
# ============================================================
baseline = df[df['Year'] == 2025].copy().set_index('grid_id')
print(f"\n2025 baseline cells: {len(baseline)}")

# If some cells missing in 2025, use 2020 data
if len(baseline) < 6000:
    print("⚠️ Some cells missing in 2025 — filling from 2020")
    baseline_2020 = df[df['Year'] == 2020].copy().set_index('grid_id')
    # For missing 2025 cells, use 2020 data
    missing = baseline_2020.index.difference(baseline.index)
    print(f"   Filling {len(missing)} cells from 2020")
    for gid in missing:
        baseline.loc[gid] = baseline_2020.loc[gid]
        baseline.loc[gid, 'Year'] = 2025

print(f"Total baseline cells: {len(baseline)}")

# ============================================================
# 2. CALCULATE TRENDS (from 2000 to 2025, averaged)
# ============================================================
print()
print("=" * 60)
print("TRENDS 2000–2025")
print("=" * 60)

df_2000 = df[df['Year'] == 2000].set_index('grid_id')
df_2025_orig = df[df['Year'] == 2025].set_index('grid_id')
common = df_2000.index.intersection(df_2025_orig.index)
print(f"Common cells for trend: {len(common)}")

ndvi_change = (df_2025_orig.loc[common, 'NDVI'] - df_2000.loc[common, 'NDVI']).mean()
ndbi_change = (df_2025_orig.loc[common, 'NDBI'] - df_2000.loc[common, 'NDBI']).mean()
lst_change = (df_2025_orig.loc[common, 'LST'] - df_2000.loc[common, 'LST']).mean()
lst_night_change = (df_2025_orig.loc[common, 'LST_Night'] - df_2000.loc[common, 'LST_Night']).mean()

print(f"NDVI change (2000-2025): {ndvi_change:+.4f} → {ndvi_change/25:+.6f}/year")
print(f"NDBI change (2000-2025): {ndbi_change:+.4f} → {ndbi_change/25:+.6f}/year")
print(f"LST change (2000-2025): {lst_change:+.4f}°C → {lst_change/25:+.4f}°C/year")
print(f"LST_Night change: {lst_night_change:+.4f}°C")

# ============================================================
# 3. BUILD 2030 FEATURES
# ============================================================
print()
print("=" * 60)
print("BUILDING 2030 FEATURES")
print("=" * 60)

df_2030 = baseline.copy()

# Apply 5-year change based on empirical rates
df_2030['NDVI'] = baseline['NDVI'] + (ndvi_change / 25) * 5
df_2030['NDBI'] = baseline['NDBI'] + (ndbi_change / 25) * 5
df_2030['LST_Night'] = baseline['LST_Night'] + (lst_night_change / 25) * 5
df_2030['Population'] = baseline['Population'] * 1.087  # ~8.7% over 5 years
df_2030['Year'] = 2030

print(f"Built 2030 features for {len(df_2030)} grid cells")

# ============================================================
# 4. PREDICT LST FOR 2030
# ============================================================
feature_cols = ['NDVI', 'NDBI', 'LST_Night', 'Population', 'Year']
X_2030 = df_2030[feature_cols].values

df_2030['LST_2030_pred'] = model.predict(X_2030)

# Add trend-based adjustment (since model has low Year importance)
# Use empirical LST warming rate
lst_warming_rate = lst_change / 25  # °C per year
df_2030['LST_2030_pred'] += lst_warming_rate * 5

print()
print("Predicted 2030 LST (after trend adjustment):")
print(f"  Mean:   {df_2030['LST_2030_pred'].mean():.2f}°C")
print(f"  Min:    {df_2030['LST_2030_pred'].min():.2f}°C")
print(f"  Max:    {df_2030['LST_2030_pred'].max():.2f}°C")

print(f"\n2025 mean LST: {baseline['LST'].mean():.2f}°C")
print(f"2030 predicted: {df_2030['LST_2030_pred'].mean():.2f}°C")
print(f"Change: {df_2030['LST_2030_pred'].mean() - baseline['LST'].mean():+.2f}°C")

# ============================================================
# 5. UNCERTAINTY
# ============================================================
# Simple uncertainty: ± RMSE from model
rmse = 0.91  # from model comparison
ci_lower = df_2030['LST_2030_pred'].mean() - 1.96 * rmse / np.sqrt(len(df_2030))
ci_upper = df_2030['LST_2030_pred'].mean() + 1.96 * rmse / np.sqrt(len(df_2030))

print()
print(f"2030 LST (95% CI):")
print(f"  Point estimate: {df_2030['LST_2030_pred'].mean():.2f}°C")
print(f"  Range:          [{ci_lower:.2f}, {ci_upper:.2f}]")

# ============================================================
# 6. SAVE
# ============================================================
output = df_2030.reset_index()[['grid_id', 'lon', 'lat', 'NDVI', 'NDBI',
                                 'LST_Night', 'Population', 'LST_2030_pred']].copy()
output.to_csv("03_results/prediction_2030.csv", index=False)
print(f"\n✅ Saved: 03_results/prediction_2030.csv ({len(output)} rows)")

# ============================================================
# 7. MAPS
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

s1 = axes[0].scatter(baseline['lon'], baseline['lat'],
                     c=baseline['LST'], cmap='hot_r',
                     s=3, vmin=22, vmax=30)
axes[0].set_title(f'2025 LST (Actual) — Mean {baseline["LST"].mean():.2f}°C',
                  fontsize=14)
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
plt.colorbar(s1, ax=axes[0], label='LST (°C)')

s2 = axes[1].scatter(output['lon'], output['lat'],
                     c=output['LST_2030_pred'], cmap='hot_r',
                     s=3, vmin=22, vmax=30)
axes[1].set_title(f'2030 LST (Predicted) — Mean {output["LST_2030_pred"].mean():.2f}°C',
                  fontsize=14)
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('Latitude')
plt.colorbar(s2, ax=axes[1], label='LST (°C)')

plt.tight_layout()
plt.savefig("03_results/maps/prediction_2030_vs_2025.png", dpi=150)
plt.close()

# Distribution
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(baseline['LST'], bins=50, alpha=0.6, color='blue',
        label=f'2025: mean={baseline["LST"].mean():.2f}°C', density=True)
ax.hist(output['LST_2030_pred'], bins=50, alpha=0.6, color='red',
        label=f'2030: mean={output["LST_2030_pred"].mean():.2f}°C', density=True)
ax.set_xlabel('LST (°C)', fontsize=12)
ax.set_ylabel('Density')
ax.set_title('LST Distribution: 2025 vs 2030 Predicted', fontsize=14)
ax.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("03_results/figures/lst_2025_vs_2030_distribution.png", dpi=150)
plt.close()

# ============================================================
# 8. TOP HOTTEST CELLS
# ============================================================
print()
print("=" * 60)
print("TOP 10 HOTTEST CELLS IN 2030")
print("=" * 60)
top = output.nlargest(10, 'LST_2030_pred')
print(top[['grid_id', 'lon', 'lat', 'LST_2030_pred']].to_string(index=False))

print()
print("=" * 60)
print("✅ 2030 prediction complete (FIXED)")
print("=" * 60)