"""
Economic Impact Estimation
Estimates economic burden of urban heat in Dhaka
- Cooling electricity demand
- Worker productivity loss
- Health-related economic cost
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("ECONOMIC IMPACT ESTIMATION")
print("=" * 60)

# Load data
df = pd.read_csv("03_results/prediction_2030.csv")
master = pd.read_csv("01_data/master/dhaka_green_space_master.csv")
baseline_2025 = master[master['Year'] == 2025].copy()

df = df.merge(
    baseline_2025[['grid_id', 'LST']].rename(columns={'LST': 'LST_2025'}),
    on='grid_id', how='left'
)
df['LST_2025'] = df['LST_2025'].fillna(baseline_2025['LST'].mean())
df['LST_2030'] = df['LST_2025'] + 0.25

pop_total = 25_000_000
df['Population_per_cell'] = pop_total / len(df)

# ============================================================
# ECONOMIC COEFFICIENTS (Literature-based)
# ============================================================
print()
print("=" * 60)
print("ECONOMIC COEFFICIENTS (Literature)")
print("=" * 60)

# From published studies:
# - IEA (2020): ~3-5% electricity demand increase per 1°C
# - ILO (2019): ~2% productivity loss per 1°C above 30°C
# - WHO (2021): health cost of heat-related illness

# Baseline values for Dhaka
baseline_electricity_per_capita_kwh_year = 500  # kWh/capita/year
electricity_cost_usd_per_kwh = 0.08  # USD per kWh (BD tariff ~8 taka)
electricity_increase_per_C = 0.04  # 4% per °C

# Productivity (for outdoor workers — ~30% of workforce)
outdoor_workforce_fraction = 0.30
baseline_productivity_loss_per_C = 0.02  # 2% per °C above threshold
avg_annual_wage_usd = 2400  # USD (approx GDP per capita)

# Health cost per case
cost_per_hospitalization_usd = 200  # USD
cost_per_ed_visit_usd = 50  # USD
cost_per_premature_death_usd = 100_000  # Value of Statistical Life (WHO)

# ============================================================
# ELECTRICITY DEMAND
# ============================================================
print()
print("=" * 60)
print("COOLING ELECTRICITY DEMAND")
print("=" * 60)

# Base electricity for cooling (assume ~40% of total)
baseline_electricity_total = pop_total * baseline_electricity_per_capita_kwh_year
baseline_cooling_kwh = baseline_electricity_total * 0.40

# Extra demand from 2025 vs 2030 temperature
# Use mean LST difference
mean_lst_2025 = df['LST_2025'].mean()
mean_lst_2030 = df['LST_2030'].mean()
temp_increase = mean_lst_2030 - mean_lst_2025

extra_electricity_pct = electricity_increase_per_C * temp_increase
extra_electricity_kwh = baseline_cooling_kwh * extra_electricity_pct
extra_electricity_cost_usd = extra_electricity_kwh * electricity_cost_usd_per_kwh

print(f"Baseline electricity (2025): {baseline_electricity_total:,.0f} kWh")
print(f"Cooling portion (40%): {baseline_cooling_kwh:,.0f} kWh")
print(f"Temperature increase: +{temp_increase:.2f}°C")
print(f"Extra electricity demand: {extra_electricity_pct*100:.2f}%")
print(f"Extra electricity: {extra_electricity_kwh:,.0f} kWh")
print(f"Extra cost: ${extra_electricity_cost_usd:,.0f} USD/year")

# ============================================================
# WORKER PRODUCTIVITY
# ============================================================
print()
print("=" * 60)
print("WORKER PRODUCTIVITY LOSS")
print("=" * 60)

# Only outdoor workers affected
outdoor_workers = int(pop_total * outdoor_workforce_fraction)
baseline_wage_bill = outdoor_workers * avg_annual_wage_usd

# Assume average 2°C increase in working-hour temperature
temp_increase_work = max(temp_increase, 0.5)  # at least 0.5°C
productivity_loss_pct = baseline_productivity_loss_per_C * temp_increase_work
productivity_loss_usd = baseline_wage_bill * productivity_loss_pct

print(f"Outdoor workers: {outdoor_workers:,} ({outdoor_workforce_fraction*100}%)")
print(f"Average annual wage: ${avg_annual_wage_usd:,}")
print(f"Total wage bill: ${baseline_wage_bill:,.0f}")
print(f"Productivity loss: {productivity_loss_pct*100:.2f}%")
print(f"Annual loss: ${productivity_loss_usd:,.0f} USD/year")

# ============================================================
# HEALTH ECONOMIC COST
# ============================================================
print()
print("=" * 60)
print("HEALTH-RELATED ECONOMIC COST")
print("=" * 60)

# Load health burden
health = pd.read_csv("03_results/tables/health_burden.csv")
health_2030 = health[health['Year'] == 2030].iloc[0]

# Calculate cost
health_cost_deaths = health_2030['Heat_Deaths'] * cost_per_premature_death_usd
health_cost_hosp = health_2030['Heat_Hospitalizations'] * cost_per_hospitalization_usd
health_cost_ed = health_2030['Heat_ED_Visits'] * cost_per_ed_visit_usd
total_health_cost = health_cost_deaths + health_cost_hosp + health_cost_ed

print(f"Premature deaths (2030): {health_2030['Heat_Deaths']:.0f}")
print(f"  Cost @ ${cost_per_premature_death_usd:,}/death: ${health_cost_deaths:,.0f}")
print(f"Hospitalizations: {health_2030['Heat_Hospitalizations']:.0f}")
print(f"  Cost @ ${cost_per_hospitalization_usd}/case: ${health_cost_hosp:,.0f}")
print(f"ED visits: {health_2030['Heat_ED_Visits']:.0f}")
print(f"  Cost @ ${cost_per_ed_visit_usd}/case: ${health_cost_ed:,.0f}")
print(f"Total health economic cost: ${total_health_cost:,.0f} USD/year")

# ============================================================
# TOTAL ECONOMIC BURDEN
# ============================================================
print()
print("=" * 60)
print("TOTAL ECONOMIC BURDEN (2030)")
print("=" * 60)

total_cost = extra_electricity_cost_usd + productivity_loss_usd + total_health_cost
print(f"Cooling electricity: ${extra_electricity_cost_usd:,.0f}")
print(f"Productivity loss:  ${productivity_loss_usd:,.0f}")
print(f"Health burden:      ${total_health_cost:,.0f}")
print(f"{'='*50}")
print(f"TOTAL (2030):       ${total_cost:,.0f} USD/year")
print(f"                    ≈ {total_cost * 110:,.0f} BDT (approx)")
print(f"                    ≈ {total_cost / pop_total:.2f} USD per person/year")

# ============================================================
# SAVE
# ============================================================
econ_summary = pd.DataFrame({
    'Category': ['Cooling Electricity', 'Productivity Loss', 'Health Burden', 'Total'],
    'Cost_USD': [extra_electricity_cost_usd, productivity_loss_usd, 
                 total_health_cost, total_cost]
})
econ_summary.to_csv("03_results/tables/economic_burden_2030.csv", index=False)

print()
print("✅ Economic impact estimation complete")
print(f"   Saved: 03_results/tables/economic_burden_2030.csv")