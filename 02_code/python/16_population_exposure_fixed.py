"""
Population Exposure Analysis — Fixed
Uses 2025 actual LST + warming shift (not raw ML predictions)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("POPULATION EXPOSURE ANALYSIS (FIXED)")
print("=" * 60)

# Load data
df_2030 = pd.read_csv("03_results/prediction_2030.csv")
master = pd.read_csv("01_data/master/dhaka_green_space_master.csv")
baseline_2025 = master[master['Year'] == 2025].copy()

# Merge 2025 actual LST
df_2030 = df_2030.merge(
    baseline_2025[['grid_id', 'LST']].rename(columns={'LST': 'LST_2025'}),
    on='grid_id', how='left'
)

# Fill missing
df_2030['LST_2025'] = df_2030['LST_2025'].fillna(baseline_2025['LST'].mean())

# ============================================================
# KEY FIX: Use 2025 LST + warming shift
# ============================================================
WARMING_SHIFT = 0.25  # °C from our prediction

df_2030['LST_2030_fixed'] = df_2030['LST_2025'] + WARMING_SHIFT

print(f"Using 2025 actual LST + {WARMING_SHIFT}°C warming shift")
print(f"2025 mean LST: {df_2030['LST_2025'].mean():.2f}°C")
print(f"2030 mean LST: {df_2030['LST_2030_fixed'].mean():.2f}°C")

# ============================================================
# POPULATION
# ============================================================
pop_2030_total = 25_000_000
pop_per_cell = pop_2030_total / len(df_2030)
df_2030['Population_per_cell'] = pop_per_cell

print(f"Population total: {pop_2030_total:,}")
print(f"Population per cell: {pop_per_cell:,.0f}")

# ============================================================
# HEAT EXPOSURE THRESHOLDS
# ============================================================
print()
print("=" * 60)
print("POPULATION EXPOSED ABOVE THRESHOLDS")
print("=" * 60)

thresholds = [25, 26, 27, 28, 29, 30, 31, 32]
results = []

for thr in thresholds:
    pop_2025 = df_2030.loc[df_2030['LST_2025'] > thr, 'Population_per_cell'].sum()
    pop_2030 = df_2030.loc[df_2030['LST_2030_fixed'] > thr, 'Population_per_cell'].sum()
    
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
# HEAT CLASSES
# ============================================================
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
df_2030['Heat_Class_2030'] = df_2030['LST_2030_fixed'].apply(classify_heat)

print()
print("=" * 60)
print("2030 HEAT CLASSES (FIXED)")
print("=" * 60)

count_2030 = df_2030.groupby('Heat_Class_2030').agg({
    'grid_id': 'count',
    'Population_per_cell': 'sum'
}).rename(columns={'grid_id': 'Cells', 'Population_per_cell': 'Population'})
count_2030['% Cells'] = (count_2030['Cells'] / len(df_2030) * 100).round(2)
count_2030['% Population'] = (count_2030['Population'] / pop_2030_total * 100).round(2)
print(count_2030.to_string())
count_2030.to_csv("03_results/tables/heat_exposure_2030.csv")

# ============================================================
# SUMMARY
# ============================================================
print()
print("=" * 60)
print("SUMMARY FOR THESIS")
print("=" * 60)

pop_above_28_2025 = df_2030.loc[df_2030['LST_2025'] > 28, 'Population_per_cell'].sum()
pop_above_28_2030 = df_2030.loc[df_2030['LST_2030_fixed'] > 28, 'Population_per_cell'].sum()
pop_above_30_2025 = df_2030.loc[df_2030['LST_2025'] > 30, 'Population_per_cell'].sum()
pop_above_30_2030 = df_2030.loc[df_2030['LST_2030_fixed'] > 30, 'Population_per_cell'].sum()

print(f"Population > 28°C:")
print(f"  2025: {pop_above_28_2025:,.0f} ({pop_above_28_2025/pop_2030_total*100:.1f}%)")
print(f"  2030: {pop_above_28_2030:,.0f} ({pop_above_28_2030/pop_2030_total*100:.1f}%)")
print(f"  Change: {pop_above_28_2030 - pop_above_28_2025:+,.0f}")

print()
print(f"Population > 30°C:")
print(f"  2025: {pop_above_30_2025:,.0f} ({pop_above_30_2025/pop_2030_total*100:.1f}%)")
print(f"  2030: {pop_above_30_2030:,.0f} ({pop_above_30_2030/pop_2030_total*100:.1f}%)")
print(f"  Change: {pop_above_30_2030 - pop_above_30_2025:+,.0f}")

# ============================================================
# MAP
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

s1 = axes[0].scatter(df_2030['lon'], df_2030['lat'],
                     c=df_2030['LST_2025'], cmap='hot_r',
                     s=5, vmin=22, vmax=32)
axes[0].set_title(f'2025 LST (Actual) — Mean {df_2030["LST_2025"].mean():.2f}°C',
                  fontsize=14)
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
plt.colorbar(s1, ax=axes[0], label='LST (°C)')

s2 = axes[1].scatter(df_2030['lon'], df_2030['lat'],
                     c=df_2030['LST_2030_fixed'], cmap='hot_r',
                     s=5, vmin=22, vmax=32)
axes[1].set_title(f'2030 LST (2025+{WARMING_SHIFT}°C) — Mean {df_2030["LST_2030_fixed"].mean():.2f}°C',
                  fontsize=14)
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('Latitude')
plt.colorbar(s2, ax=axes[1], label='LST (°C)')

plt.tight_layout()
plt.savefig("03_results/maps/heat_exposure_2025_vs_2030.png", dpi=150)
plt.close()
print()
print("✅ Map saved: heat_exposure_2025_vs_2030.png")
print()
print("=" * 60)
print("✅ Population exposure analysis complete (FIXED)")
print("=" * 60)