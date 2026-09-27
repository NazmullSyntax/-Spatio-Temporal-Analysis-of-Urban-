"""
Extract mean NDVI, NDBI, LST, LST_Night per grid cell per year
Output: dhaka_green_space_master.csv (~38,000 rows)
"""
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import pandas as pd
import numpy as np
from tqdm import tqdm
import os

print("=" * 60)
print("Extracting Zonal Statistics")
print("=" * 60)

# Load grid
grid = gpd.read_file("01_data/processed/dhaka_grid_500m.shp")
print(f"Grid loaded: {len(grid)} cells")

years = [2000, 2005, 2010, 2015, 2020, 2025]
indices = ['NDVI', 'NDBI', 'LST', 'LST_Night']

# Master dataframe
master_rows = []

for year in tqdm(years, desc="Processing years"):
    year_data = {'grid_id': grid['grid_id'].values, 'Year': year}
    
    for index in indices:
        raster_path = f"01_data/raw/processed_rasters/{index}_{year}_seasonal.tif"
        
        if not os.path.exists(raster_path):
            print(f"⚠️  Missing: {raster_path}")
            year_data[index] = np.nan
            continue
        
        with rasterio.open(raster_path) as src:
            # Match CRS
            grid_for_raster = grid.to_crs(src.crs) if grid.crs != src.crs else grid
            
            # Compute zonal statistics
            stats = zonal_stats(
                grid_for_raster,
                src.read(1),
                affine=src.transform,
                stats=['mean'],
                nodata=src.nodata
            )
            
            values = [s['mean'] if s['mean'] is not None else np.nan for s in stats]
            year_data[index] = values
    
    # Create year DataFrame
    year_df = pd.DataFrame(year_data)
    master_rows.append(year_df)

# Combine all years
master = pd.concat(master_rows, ignore_index=True)

# Add coordinates
coords = grid[['grid_id', 'lon', 'lat']].copy()
master = master.merge(coords, on='grid_id', how='left')

# Save
output_path = "01_data/processed/dhaka_green_space_master.csv"
master.to_csv(output_path, index=False)

print()
print("=" * 60)
print(f"✅ Master dataset saved: {output_path}")
print(f"   Rows: {len(master)}")
print(f"   Columns: {list(master.columns)}")
print()
print("Sample (first 5 rows):")
print(master.head().to_string())
print()
print("Mean values by year:")
print(master.groupby('Year')[['NDVI', 'NDBI', 'LST', 'LST_Night']].mean().round(3))