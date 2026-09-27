"""
Core statistical analysis:
- Descriptive statistics by year
- Correlation: NDVI vs LST, NDBI vs LST
- Linear regression
- Time trend analysis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import os

# Load master
df = pd.read_csv("01_data/master/dhaka_green_space_master.csv")
print(f"Loaded {len(df)} rows")

# Create output dirs
os.makedirs("03_results/tables", exist_ok=True)
os.makedirs("03_results/figures", exist_ok=True)

# ============================================================
# 1. DESCRIPTIVE STATISTICS BY YEAR
# ============================================================
print()
print("=" * 60)
print("1. DESCRIPTIVE STATISTICS BY YEAR")
print("=" * 60)

yearly = df.groupby('Year').agg({
    'NDVI': ['mean', 'std'],
    'NDBI': ['mean', 'std'],
    'LST': ['mean', 'std'],
    'LST_Night': ['mean', 'std'],
}).round(4)

print(yearly)
yearly.to_csv("03_results/tables/descriptive_by_year.csv")

# ============================================================
# 2. CORRELATION ANALYSIS
# ============================================================
print()
print("=" * 60)
print("2. CORRELATION ANALYSIS")
print("=" * 60)

# Remove rows with missing values
df_clean = df.dropna(subset=['NDVI', 'NDBI', 'LST', 'LST_Night'])
print(f"Clean rows: {len(df_clean)}")

# Pearson correlations
r_ndvi_lst, p_ndvi_lst = stats.pearsonr(df_clean['NDVI'], df_clean['LST'])
r_ndbi_lst, p_ndbi_lst = stats.pearsonr(df_clean['NDBI'], df_clean['LST'])
r_ndvi_night, p_ndvi_night = stats.pearsonr(df_clean['NDVI'], df_clean['LST_Night'])
r_ndbi_night, p_ndbi_night = stats.pearsonr(df_clean['NDBI'], df_clean['LST_Night'])

corr_results = pd.DataFrame({
    'Relationship': ['NDVI vs LST', 'NDBI vs LST', 
                     'NDVI vs LST_Night', 'NDBI vs LST_Night'],
    'Pearson_r': [r_ndvi_lst, r_ndbi_lst, r_ndvi_night, r_ndbi_night],
    'P_value': [p_ndvi_lst, p_ndbi_lst, p_ndvi_night, p_ndbi_night],
    'Significant': ['YES' if p < 0.05 else 'NO' 
                    for p in [p_ndvi_lst, p_ndbi_lst, p_ndvi_night, p_ndbi_night]]
})
print(corr_results.round(4).to_string(index=False))
corr_results.to_csv("03_results/tables/correlation_results.csv", index=False)

# Correlation matrix
fig, ax = plt.subplots(figsize=(8, 6))
corr_matrix = df_clean[['NDVI', 'NDBI', 'LST', 'LST_Night']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0,
            fmt='.3f', square=True, ax=ax)
plt.title('Correlation Matrix: Environmental Variables')
plt.tight_layout()
plt.savefig("03_results/figures/correlation_matrix.png", dpi=150)
plt.close()

# ============================================================
# 3. REGRESSION: LST ~ NDVI + NDBI
# ============================================================
print()
print("=" * 60)
print("3. REGRESSION: LST ~ NDVI + NDBI")
print("=" * 60)

X = sm.add_constant(df_clean[['NDVI', 'NDBI']])
y = df_clean['LST']
model = sm.OLS(y, X).fit()
print(model.summary())

with open("03_results/tables/regression_lst.txt", 'w') as f:
    f.write(model.summary().as_text())

# ============================================================
# 4. TIME TREND ANALYSIS
# ============================================================
print()
print("=" * 60)
print("4. TIME TREND ANALYSIS")
print("=" * 60)

yearly_means = df.groupby('Year')[['NDVI', 'NDBI', 'LST', 'LST_Night']].mean().reset_index()

# LST trend
slope_lst, intercept_lst, r_lst, p_lst, se_lst = stats.linregress(
    yearly_means['Year'], yearly_means['LST'])
print(f"LST trend: {slope_lst:+.4f} °C/year (R² = {r_lst**2:.3f}, p = {p_lst:.4f})")

# LST_Night trend
slope_night, intercept_night, r_night, p_night, se_night = stats.linregress(
    yearly_means['Year'], yearly_means['LST_Night'])
print(f"LST_Night trend: {slope_night:+.4f} °C/year (R² = {r_night**2:.3f}, p = {p_night:.4f})")

# NDVI trend
slope_ndvi, intercept_ndvi, r_ndvi, p_ndvi, se_ndvi = stats.linregress(
    yearly_means['Year'], yearly_means['NDVI'])
print(f"NDVI trend: {slope_ndvi:+.5f}/year (R² = {r_ndvi**2:.3f}, p = {p_ndvi:.4f})")

# NDBI trend
slope_ndbi, intercept_ndbi, r_ndbi, p_ndbi, se_ndbi = stats.linregress(
    yearly_means['Year'], yearly_means['NDBI'])
print(f"NDBI trend: {slope_ndbi:+.5f}/year (R² = {r_ndbi**2:.3f}, p = {p_ndbi:.4f})")

# Save trends
trends = pd.DataFrame({
    'Variable': ['LST', 'LST_Night', 'NDVI', 'NDBI'],
    'Slope_per_year': [slope_lst, slope_night, slope_ndvi, slope_ndbi],
    'R_squared': [r_lst**2, r_night**2, r_ndvi**2, r_ndbi**2],
    'P_value': [p_lst, p_night, p_ndvi, p_ndbi]
})
trends.to_csv("03_results/tables/time_trends.csv", index=False)

# ============================================================
# 5. SCATTER PLOTS
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# NDVI vs LST
axes[0].scatter(df_clean['NDVI'], df_clean['LST'],
                alpha=0.15, s=2, c='green')
axes[0].set_xlabel('NDVI', fontsize=12)
axes[0].set_ylabel('Daytime LST (°C)', fontsize=12)
axes[0].set_title(f'NDVI vs LST (r = {r_ndvi_lst:.3f})', fontsize=14)
axes[0].grid(True, alpha=0.3)

# NDBI vs LST
axes[1].scatter(df_clean['NDBI'], df_clean['LST'],
                alpha=0.15, s=2, c='red')
axes[1].set_xlabel('NDBI', fontsize=12)
axes[1].set_ylabel('Daytime LST (°C)', fontsize=12)
axes[1].set_title(f'NDBI vs LST (r = {r_ndbi_lst:.3f})', fontsize=14)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("03_results/figures/scatter_ndvi_ndbi_vs_lst.png", dpi=150)
plt.close()

# ============================================================
# 6. TIME SERIES PLOTS
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# LST
axes[0, 0].plot(yearly_means['Year'], yearly_means['LST'],
                'o-', color='#d62728', linewidth=2, markersize=10)
axes[0, 0].set_title('Mean Daytime LST (2000–2025)', fontsize=14)
axes[0, 0].set_xlabel('Year')
axes[0, 0].set_ylabel('LST (°C)')
axes[0, 0].grid(True, alpha=0.3)

# LST_Night
axes[0, 1].plot(yearly_means['Year'], yearly_means['LST_Night'],
                'o-', color='#9467bd', linewidth=2, markersize=10)
axes[0, 1].set_title('Mean Nighttime LST (2000–2025)', fontsize=14)
axes[0, 1].set_xlabel('Year')
axes[0, 1].set_ylabel('LST_Night (°C)')
axes[0, 1].grid(True, alpha=0.3)

# NDVI
axes[1, 0].plot(yearly_means['Year'], yearly_means['NDVI'],
                'o-', color='green', linewidth=2, markersize=10)
axes[1, 0].set_title('Mean NDVI (2000–2025)', fontsize=14)
axes[1, 0].set_xlabel('Year')
axes[1, 0].set_ylabel('NDVI')
axes[1, 0].grid(True, alpha=0.3)

# NDBI
axes[1, 1].plot(yearly_means['Year'], yearly_means['NDBI'],
                'o-', color='brown', linewidth=2, markersize=10)
axes[1, 1].set_title('Mean NDBI (2000–2025)', fontsize=14)
axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('NDBI')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("03_results/figures/temporal_trends.png", dpi=150)
plt.close()

print()
print("=" * 60)
print("✅ Analysis complete. Files saved to 03_results/")
print("=" * 60)