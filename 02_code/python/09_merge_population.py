"""
Merge population data into master CSV
"""
import pandas as pd
import os

print("=" * 60)
print("Merging Population Data into Master")
print("=" * 60)

# Load master
master = pd.read_csv("01_data/processed/dhaka_green_space_master.csv")
print(f"Master rows: {len(master)}")

# Load population
pop = pd.read_csv("01_data/raw/socioeconomic/dhaka_population.csv")
print(f"Population rows: {len(pop)}")

# Merge by Year
master = master.merge(pop, on='Year', how='left')

# Save to master folder
os.makedirs("01_data/master", exist_ok=True)
output = "01_data/master/dhaka_green_space_master.csv"
master.to_csv(output, index=False)

print()
print("=" * 60)
print("✅ Master Dataset Updated")
print("=" * 60)
print(f"Rows: {len(master)}")
print(f"Columns: {list(master.columns)}")
print()
print("Sample (first 5 rows):")
print(master.head().to_string())
print()
print("Population check:")
print(master.groupby('Year')['Population'].first())