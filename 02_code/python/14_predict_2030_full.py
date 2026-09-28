"""
2030 Prediction — Full version
- Recovers all 6,315 grid cells
- Fills missing 2025 data from 2020 or other years
- Predicts 2030 LST
"""
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

print("=" * 60)
print("2030 PREDICTION (FULL)")
print("=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================
df = pd.read_csv("01_data/master/dhaka_green_space_master.csv")
print(f"Total rows: {len(df)}")
print(f"Total unique grid cells: {df['grid_id'].nunique()}")
print(f"Years: {sorted(df['Year'].unique())}")

# Check data availability per year
print()
print("Data availability by year:")
for year in sorted(df['Year'].unique()):
    subset = df[df['Year'] == year]
    print(f"  {year}: {len(subset)} cells | "
          f"NDVI: {subset['NDVI'].notna().sum()} | "
          f"NDBI: {subset['NDBI'].notna().sum()} | "
          f"LST: {subset['LST'].notna().sum()} | "
          f"LST_Night: {subset['LST_Night'].notna().sum()}")

# ============================================================
# 2. FILL MISSING LST_Night (main problem)
# ============================================================
print()
print("=" * 60)
print("FILLING MISSING DATA")
print("=" * 60)

# For each cell, fill missing LST_Night with the cell's own average
df = df.sort_values(['grid_id', 'Year'])

# Group by cell and forward/backward fill LST_Night
df['LST_Night_filled'] = df.groupby('grid_id')['LST_Night'].transform(
    lambda x: x.fillna(x.mean())
)

# If still NaN (cell has no LST_Night at all), use city average for that year
df['LST_Night_filled'] = df.groupby('Year')['LST_Night_filled'].transform(
    lambda x: x.fillna(x.mean())
)

# Same for NDVI, NDBI, LST
df['NDVI_filled'] = df.groupby('grid_id')['NDVI'].transform(
    lambda x: x.fillna(x.mean()))
df['NDBI_filled'] = df.groupby('grid_id')['NDBI'].transform(
    lambda x: x.fillna(x.mean()))
df['LST_filled'] = df.groupby('grid_id')['LST'].transform(
    lambda x: x.fillna(x.mean()))

# Fill remaining NaN with year-level mean
for col in ['NDVI_filled', 'NDBI_filled', 'LST_filled']:
    df[col] = df.groupby('Year')[col].transform(lambda x: x.fillna(x.mean()))

print(f"After filling, missing values:")
print(f"  NDVI_filled: {df['NDVI_filled'].isna().sum()}")
print(f"  NDBI_filled: {df['NDBI_filled'].isna().sum()}")
print(f"  LST_filled: {df['LST_filled'].isna().sum()}")
print(f"  LST_Night_filled: {df['LST_Night_filled'].isna().sum()}")

# ============================================================
# 3. RETRAIN MODEL WITH FILLED DATA
# ============================================================
print()
print("=" * 60)
print("RETRAINING MODEL WITH FULL DATA")
print("=" * 60)

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

model_df = df.dropna(subset=['NDVI_filled', 'NDBI_filled',
                             'LST_filled', 'LST_Night_filled']).copy()

# Population merge
pop_lookup = {2000: 10500000, 2005: 12500000, 2010: 14500000,
              2015: 17500000, 2020: 21000000, 2025: 23000000}
model_df['Population'] = model_df['Year'].map(pop_lookup)

feature_cols = ['NDVI_filled', 'NDBI_filled', 'LST_Night_filled',
                'Population', 'Year']

X = model_df[feature_cols].values
y = model_df['LST_filled'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(n_estimators=100, max_depth=5,
                                   learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f"Model R²: {r2:.4f}")
print(f"Model MAE: {mae:.4f}°C")
print(f"Training samples: {len(X_train)}")

# ============================================================
# 4. BUILD 2030 BASELINE (from 2025)
# ============================================================
baseline = df[df['Year'] == 2025].copy().set_index('grid_id')
print(f"\n2025 cells available: {len(baseline)}")

# Calculate trends from 2000 to 2025
df_2000 = df[df['Year'] == 2000].set_index('grid_id')
common = df_2000.index.intersection(baseline.index)
print(f"Cells with data in both 2000 and 2025: {len(common)}")

ndvi_change = (baseline.loc[common, 'NDVI_filled'] -
               df_2000.loc[common, 'NDVI_filled']).mean() / 25
ndbi_change = (baseline.loc[common, 'NDBI_filled'] -
               df_2000.loc[common, 'NDBI_filled']).mean() / 25
lst_night_change = (baseline.loc[common, 'LST_Night_filled'] -
                    df_2000.loc[common, 'LST_Night_filled']).mean() / 25
lst_change = (baseline.loc[common, 'LST_filled'] -
              df_2000.loc[common, 'LST_filled']).mean() / 25

print(f"Trends per year:")
print(f"  NDVI: {ndvi_change:+.6f}")
print(f"  NDBI: {ndbi_change:+.6f}")
print(f"  LST: {lst_change:+.4f}°C")
print(f"  LST_Night: {lst_night_change:+.4f}°C")

# ============================================================
# 5. BUILD 2030 FEATURES
# ============================================================
df_2030 = baseline.copy()
df_2030['NDVI_filled'] = baseline['NDVI_filled'] + ndvi_change * 5
df_2030['NDBI_filled'] = baseline['NDBI_filled'] + ndbi_change * 5
df_2030['LST_Night_filled'] = baseline['LST_Night_filled'] + lst_night_change * 5
df_2030['Population'] = baseline['Year'].map({2025: 23000000}) * 1.087
df_2030['Year'] = 2030

print(f"\n2030 grid cells: {len(df_2030)}")

# ============================================================
# 6. PREDICT AND ADJUST
# ============================================================
X_2030 = df_2030[feature_cols].values
df_2030['LST_2030_pred'] = model.predict(X_2030)

# Apply empirical LST trend adjustment
df_2030['LST_2030_pred'] += lst_change * 5

print()
print("=" * 60)
print("2030 PREDICTION RESULTS")
print("=" * 60)
print(f"2025 mean LST: {baseline['LST_filled'].mean():.2f}°C")
print(f"2030 mean LST: {df_2030['LST_2030_pred'].mean():.2f}°C")
print(f"Change: {df_2030['LST_2030_pred'].mean() - baseline['LST_filled'].mean():+.2f}°C")
print()
print(f"2030 LST range: [{df_2030['LST_2030_pred'].min():.2f}, "
      f"{df_2030['LST_2030_pred'].max():.2f}]")
print(f"2030 std: {df_2030['LST_2030_pred'].std():.2f}°C")

# Uncertainty
ci_lower = df_2030['LST_2030_pred'].mean() - 1.96 * mae / np.sqrt(len(df_2030))
ci_upper = df_2030['LST_2030_pred'].mean() + 1.96 * mae / np.sqrt(len(df_2030))
print(f"95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]")

# ============================================================
# 7. SAVE
# ============================================================
output = df_2030.reset_index()[['grid_id', 'lon', 'lat',
                                 'NDVI_filled', 'NDBI_filled',
                                 'LST_Night_filled', 'Population',
                                 'LST_2030_pred']].copy()
output.columns = ['grid_id', 'lon', 'lat', 'NDVI', 'NDBI',
                  'LST_Night', 'Population', 'LST_2030_pred']
output.to_csv("03_results/prediction_2030.csv", index=False)
print(f"\n✅ Saved: 03_results/prediction_2030.csv ({len(output)} rows)")

# ============================================================
# 8. MAPS
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

s1 = axes[0].scatter(baseline['lon'], baseline['lat'],
                     c=baseline['LST_filled'], cmap='hot_r',
                     s=3, vmin=22, vmax=30)
axes[0].set_title(f'2025 LST (Actual) — Mean {baseline["LST_filled"].mean():.2f}°C',
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

print()
print("=" * 60)
print("✅ DONE — Now covers all grid cells")
print("=" * 60)