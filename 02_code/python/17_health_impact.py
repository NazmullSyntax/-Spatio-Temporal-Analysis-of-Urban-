"""
Health Impact Estimation
Uses published exposure-response coefficients to estimate
heat-related health burden in Dhaka (2025 and 2030)

References for coefficients:
- Gasparrini et al. (2015) Lancet: heat-mortality relationship
- Burkart et al. (2011): heat-hospitalization relationship
- WHO (2021): Heat and health in South Asia
- Rahman et al. (2019): Bangladesh-specific estimates

IMPORTANT: These are ESTIMATES based on literature coefficients,
not measured health outcomes.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("HEALTH IMPACT ESTIMATION (Literature-based)")
print("=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================
df = pd.read_csv("03_results/prediction_2030.csv")
master = pd.read_csv("01_data/master/dhaka_green_space_master.csv")
baseline_2025 = master[master['Year'] == 2025].copy()

# Merge 2025 LST
df = df.merge(
    baseline_2025[['grid_id', 'LST']].rename(columns={'LST': 'LST_2025'}),
    on='grid_id', how='left'
)
df['LST_2025'] = df['LST_2025'].fillna(baseline_2025['LST'].mean())

# Fix 2030: 2025 + warming shift
WARMING_SHIFT = 0.25
df['LST_2030'] = df['LST_2025'] + WARMING_SHIFT

# Population per cell
pop_total = 25_000_000
df['Population_per_cell'] = pop_total / len(df)

print(f"Grid cells: {len(df)}")
print(f"Total population (2030): {pop_total:,}")
print(f"2025 mean LST: {df['LST_2025'].mean():.2f}°C")
print(f"2030 mean LST: {df['LST_2030'].mean():.2f}°C")

# ============================================================
# 2. EXPOSURE-RESPONSE COEFFICIENTS (from literature)
# ============================================================
print()
print("=" * 60)
print("EXPOSURE-RESPONSE COEFFICIENTS (Literature)")
print("=" * 60)

# From published studies:
# - Gasparrini et al. 2015: ~1-3% increase in mortality per 1°C above threshold
# - Burkart et al. 2011: ~0.5-2% increase in hospital admissions per 1°C
# - WHO 2021: ~5-10% increase in heat-related ED visits per 1°C

# Conservative estimates for South Asia:
heat_threshold = 30.0  # °C — where health effects begin
mortality_increase_per_C = 0.02  # 2% per °C above threshold
hospitalization_increase_per_C = 0.01  # 1% per °C
ed_visit_increase_per_C = 0.05  # 5% per °C

# Baseline rates (per 100,000 population per year) for Bangladesh
# Source: WHO, BBS Health Statistics
baseline_heat_mortality_rate = 5  # deaths per 100,000/year
baseline_heat_hospital_rate = 50  # hospitalizations per 100,000/year
baseline_heat_ed_rate = 200  # ED visits per 100,000/year

print(f"Heat threshold: {heat_threshold}°C")
print(f"Mortality increase: {mortality_increase_per_C*100}% per °C")
print(f"Hospitalization increase: {hospitalization_increase_per_C*100}% per °C")
print(f"ED visit increase: {ed_visit_increase_per_C*100}% per °C")
print()
print(f"Baseline rates (per 100,000/year):")
print(f"  Mortality: {baseline_heat_mortality_rate}")
print(f"  Hospitalization: {baseline_heat_hospital_rate}")
print(f"  ED visits: {baseline_heat_ed_rate}")

# ============================================================
# 3. CALCULATE HEALTH BURDEN
# ============================================================
print()
print("=" * 60)
print("ESTIMATED HEALTH BURDEN")
print("=" * 60)

def calc_health_burden(lst_values, population, year_label):
    """Calculate estimated health outcomes based on LST"""
    results = {
        'Year': year_label,
        'Exposed_Pop': 0,
        'Heat_Deaths': 0,
        'Heat_Hospitalizations': 0,
        'Heat_ED_Visits': 0
    }
    
    for lst, pop in zip(lst_values, population):
        if lst <= heat_threshold:
            continue
        
        degrees_above = lst - heat_threshold
        exposed_pop = pop
        results['Exposed_Pop'] += exposed_pop
        
        # Apply coefficients
        mortality_rate = baseline_heat_mortality_rate * (1 + mortality_increase_per_C * degrees_above)
        hospital_rate = baseline_heat_hospital_rate * (1 + hospitalization_increase_per_C * degrees_above)
        ed_rate = baseline_heat_ed_rate * (1 + ed_visit_increase_per_C * degrees_above)
        
        results['Heat_Deaths'] += (mortality_rate / 100_000) * exposed_pop
        results['Heat_Hospitalizations'] += (hospital_rate / 100_000) * exposed_pop
        results['Heat_ED_Visits'] += (ed_rate / 100_000) * exposed_pop
    
    return results

# 2025
burden_2025 = calc_health_burden(
    df['LST_2025'].values,
    df['Population_per_cell'].values,
    '2025'
)

# 2030
burden_2030 = calc_health_burden(
    df['LST_2030'].values,
    df['Population_per_cell'].values,
    '2030'
)

burden_df = pd.DataFrame([burden_2025, burden_2030])
print(burden_df.to_string(index=False))
burden_df.to_csv("03_results/tables/health_burden.csv", index=False)

# ============================================================
# 4. ADDITIONAL HEALTH ATTRIBUTION
# ============================================================
print()
print("=" * 60)
print("HEAT-ATTRIBUTABLE BURDEN (Excess above threshold)")
print("=" * 60)

# Calculate what would happen at threshold temperature (no excess heat)
df_no_excess = df.copy()
df_no_excess['LST_2025'] = np.minimum(df['LST_2025'], heat_threshold)
df_no_excess['LST_2030'] = np.minimum(df['LST_2030'], heat_threshold)

baseline_burden = calc_health_burden(
    df_no_excess['LST_2030'].values,
    df_no_excess['Population_per_cell'].values,
    'Baseline (no excess heat)'
)

attributable_deaths_2030 = burden_2030['Heat_Deaths'] - baseline_burden['Heat_Deaths']
attributable_hosp_2030 = burden_2030['Heat_Hospitalizations'] - baseline_burden['Heat_Hospitalizations']
attributable_ed_2030 = burden_2030['Heat_ED_Visits'] - baseline_burden['Heat_ED_Visits']

print(f"Attributable to heat above {heat_threshold}°C (2030):")
print(f"  Heat-related deaths: {attributable_deaths_2030:,.0f}")
print(f"  Heat-related hospitalizations: {attributable_hosp_2030:,.0f}")
print(f"  Heat-related ED visits: {attributable_ed_2030:,.0f}")

# ============================================================
# 5. ZONE-LEVEL MAP
# ============================================================
# Heat exposure × population (weighted)
df['Heat_Index_2025'] = np.maximum(df['LST_2025'] - 28, 0) * df['Population_per_cell']
df['Heat_Index_2030'] = np.maximum(df['LST_2030'] - 28, 0) * df['Population_per_cell']

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

s1 = axes[0].scatter(df['lon'], df['lat'],
                     c=df['LST_2025'], cmap='hot_r',
                     s=5, vmin=22, vmax=32)
axes[0].set_title(f'2025 Heat Exposure', fontsize=14)
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
plt.colorbar(s1, ax=axes[0], label='LST (°C)')

s2 = axes[1].scatter(df['lon'], df['lat'],
                     c=df['LST_2030'], cmap='hot_r',
                     s=5, vmin=22, vmax=32)
axes[1].set_title(f'2030 Heat Exposure (Predicted)', fontsize=14)
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('Latitude')
plt.colorbar(s2, ax=axes[1], label='LST (°C)')

plt.tight_layout()
plt.savefig("03_results/maps/health_exposure_maps.png", dpi=150)
plt.close()
print()
print("✅ Health exposure maps saved")

print()
print("=" * 60)
print("✅ Health impact estimation complete")
print("=" * 60)