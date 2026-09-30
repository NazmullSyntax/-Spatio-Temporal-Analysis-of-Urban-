"""
Population Exposure Analysis:
- Combine 2030 LST predictions with population
- Calculate people exposed to heat > 28°C, 30°C, 32°C
- Identify priority intervention zones
- Create heat exposure maps
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

print("=" * 60)
print("POPULATION EXPOSURE ANALYSIS")
print("=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================
df_2030 = pd.read_csv("03_results/prediction_2030.csv")
print(f"Loaded {len(df_2030)} grid cells")

master = pd.read_csv("01_data/master/dhaka_green_space_master.csv")
baseline_2025 = master[master['Year'] == 2025].copy()

# Merge baseline 2025 LST into 2030 predictions
df_2030 = df_2030.merge(
    baseline_2025[['grid_id', 'LST']].rename(columns={'LST': 'LST_2025'}),
    on='grid_id', how='left'
)

# If LST_2025 is missing, use city mean
df_2030['LST_2025'] = df_2030['LST_2025'].fillna(baseline_2025['LST'].mean())

print(f"Merged 2025 baseline")

# ============================================================
# 2. POPULATION PER GRID CELL
# ============================================================
# Total population for Dhaka District ~23 million in 2025
# Assume 8.7% growth to 2030 → 25 million
pop_2030_total = 25_000_000
pop_per_cell = pop_2030_total / len(df_2030)
df_2030['Population_per_cell'] = pop_per_cell

print()
print("=" * 60)
print("POPULATION DISTRIBUTION")
print("=" * 60)
print(f"Total 2030 population (est.): {pop_2030_total:,}")
print(f"Grid cells: {len(df_2030):,}")
print(f"Population per cell: {pop_per_cell:,.0f}")

# ============================================================
# 3. HEAT EXPOSURE CATEGORIES
# ============================================================
print()
print("=" * 60)
print("HEAT EXPOSURE CLASSIFICATION")
print("=" * 60)

def classify_heat(lst):
    if lst < 25:
        return 'Low (<25°C)'
    elif lst < 28:
        return 'Moderate (25-28°C)'
    elif lst < 30:
        return 'High (28-30°C)'
    else:
        return 'Extreme (>30°C)'

df_2030['Heat_Class_2025'] = df_2030['LST_2025'].apply(classify_heat)
df_2030['Heat_Class_2030'] = df_2030['LST_2030_pred'].apply(classify_heat)

print("2025 Heat Classes:")
count_2025 = df_2030.groupby('Heat_Class_2025').agg({
    'grid_id': 'count',
    'Population_per_cell': 'sum'
}).rename(columns={'grid_id': 'Cells', 'Population_per_cell': 'Population'})
count_2025['% Cells'] = (count_2025['Cells'] / len(df_2030) * 100).round(2)
count_2025['% Population'] = (count_2025['Population'] / pop_2030_total * 100).round(2)
print(count_2025.to_string())

print()
print("2030 Heat Classes:")
count_2030 = df_2030.groupby('Heat_Class_2030').agg({
    'grid_id': 'count',
    'Population_per_cell': 'sum'
}).rename(columns={'grid_id': 'Cells', 'Population_per_cell': 'Population'})
count_2030['% Cells'] = (count_2030['Cells'] / len(df_2030) * 100).round(2)
count_2030['% Population'] = (count_2030['Population'] / pop_2030_total * 100).round(2)
print(count_2030.to_string())

count_2025.to_csv("03_results/tables/heat_exposure_2025.csv")
count_2030.to_csv("03_results/tables/heat_exposure_2030.csv")

# ============================================================
# 4. HEAT EXPOSURE BY THRESHOLD
# ============================================================
print()
print("=" * 60)
print("POPULATION EXPOSED ABOVE THRESHOLDS")
print("=" * 60)

thresholds = [25, 26, 27, 28, 29, 30, 31, 32]
results = []

for thr in thresholds:
    pop_2025 = df_2030.loc[df_2030['LST_2025'] > thr, 'Population_per_cell'].sum()
    pop_2030 = df_2030.loc[df_2030['LST_2030_pred'] > thr, 'Population_per_cell'].sum()
    
    results.append({
        'Threshold_C': thr,
        'Population_2025': int(pop_2025),
        'Population_2030': int(pop_2030),
        'Change': int(pop_2030 - pop_2025),
        'Change_pct': round((pop_2030 - pop_2025) / pop_2025 * 100, 2) if pop_2025 > 0 else 0
    })

exposure_df = pd.DataFrame(results)
print(exposure_df.to_string(index=False))
exposure_df.to_csv("03_results/tables/population_exposure.csv", index=False)

# ============================================================
# 5. HOTSPOT IDENTIFICATION
# ============================================================
print()
print("=" * 60)
print("TOP 20 HOTTEST CELLS IN 2030")
print("=" * 60)

top_hot = df_2030.nlargest(20, 'LST_2030_pred')
top_hot_clean = top_hot[['grid_id', 'lon', 'lat',
                          'LST_2025', 'LST_2030_pred',
                          'Population_per_cell']].copy()
top_hot_clean['Temp_Increase'] = top_hot_clean['LST_2030_pred'] - top_hot_clean['LST_2025']
print(top_hot_clean.to_string(index=False))
top_hot_clean.to_csv("03_results/tables/top_hotspot_cells_2030.csv", index=False)

# ============================================================
# 6. MAPS
# ============================================================
print()
print("=" * 60)
print("CREATING MAPS")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

scatter1 = axes[0].scatter(
    df_2030['lon'], df_2030['lat'],
    c=df_2030['LST_2025'], cmap='hot_r',
    s=5, vmin=22, vmax=32
)
axes[0].set_title('2025 LST Exposure', fontsize=15, fontweight='bold')
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
plt.colorbar(scatter1, ax=axes[0], label='LST (°C)')

scatter2 = axes[1].scatter(
    df_2030['lon'], df_2030['lat'],
    c=df_2030['LST_2030_pred'], cmap='hot_r',
    s=5, vmin=22, vmax=32
)
axes[1].set_title('2030 LST Exposure (Predicted)', fontsize=15, fontweight='bold')
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('Latitude')
plt.colorbar(scatter2, ax=axes[1], label='LST (°C)')

plt.tight_layout()
plt.savefig("03_results/maps/heat_exposure_2025_vs_2030.png", dpi=150)
plt.close()
print("✅ Map saved: heat_exposure_2025_vs_2030.png")

# Heat zone classification map
fig, ax = plt.subplots(figsize=(12, 10))

categories = df_2030['Heat_Class_2030'].unique()
colors_dict = {
    'Low (<25°C)': 'green',
    'Moderate (25-28°C)': 'yellow',
    'High (28-30°C)': 'orange',
    'Extreme (>30°C)': 'red'
}

for cat in categories:
    subset = df_2030[df_2030['Heat_Class_2030'] == cat]
    ax.scatter(subset['lon'], subset['lat'],
               c=colors_dict.get(cat, 'gray'),
               s=5, label=cat, alpha=0.7)

ax.set_title('2030 Heat Exposure Zones', fontsize=15, fontweight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend(loc='upper left', markerscale=3)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("03_results/maps/heat_zones_2030.png", dpi=150)
plt.close()
print("✅ Map saved: heat_zones_2030.png")

# ============================================================
# 7. SUMMARY FOR THESIS
# ============================================================
print()
print("=" * 60)
print("SUMMARY FOR THESIS")
print("=" * 60)

pop_above_28_2025 = df_2030.loc[df_2030['LST_2025'] > 28, 'Population_per_cell'].sum()
pop_above_28_2030 = df_2030.loc[df_2030['LST_2030_pred'] > 28, 'Population_per_cell'].sum()

print(f"Population exposed to LST > 28°C:")
print(f"  2025: {pop_above_28_2025:,.0f} ({pop_above_28_2025/pop_2030_total*100:.1f}%)")
print(f"  2030: {pop_above_28_2030:,.0f} ({pop_above_28_2030/pop_2030_total*100:.1f}%)")
print(f"  Change: {pop_above_28_2030 - pop_above_28_2025:+,.0f}")

pop_above_30_2025 = df_2030.loc[df_2030['LST_2025'] > 30, 'Population_per_cell'].sum()
pop_above_30_2030 = df_2030.loc[df_2030['LST_2030_pred'] > 30, 'Population_per_cell'].sum()

print()
print(f"Population exposed to LST > 30°C:")
print(f"  2025: {pop_above_30_2025:,.0f} ({pop_above_30_2025/pop_2030_total*100:.1f}%)")
print(f"  2030: {pop_above_30_2030:,.0f} ({pop_above_30_2030/pop_2030_total*100:.1f}%)")

print()
print("=" * 60)
print("✅ Population exposure analysis complete")
print("=" * 60)