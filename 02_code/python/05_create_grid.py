"""
Create 500m x 500m grid over Dhaka District
Output: clipped grid shapefile (cell count depends on the boundary)
"""
import geopandas as gpd
from shapely.geometry import box
import numpy as np
import os

print("=" * 60)
print("Creating 500m Grid Over Dhaka")
print("=" * 60)

# Load Dhaka boundary in UTM (for accurate metric grid)
dhaka = gpd.read_file("01_data/raw/boundaries/dhaka_district.shp")
dhaka_utm = dhaka.to_crs("EPSG:32646")

# Get bounding box in UTM
xmin, ymin, xmax, ymax = dhaka_utm.total_bounds
print("Bounding box (UTM 46N):")
print(f"  X: {xmin:.0f} to {xmax:.0f}")
print(f"  Y: {ymin:.0f} to {ymax:.0f}")

# Grid cell size = 500m
cell_size = 500

# Create grid cells
x_coords = np.arange(xmin, xmax, cell_size)
y_coords = np.arange(ymin, ymax, cell_size)

grid_cells = []
grid_id = 1

for x in x_coords:
    for y in y_coords:
        grid_cells.append({
            "grid_id": f"G{grid_id:04d}",
            "geometry": box(x, y, x + cell_size, y + cell_size)
        })
        grid_id += 1

grid = gpd.GeoDataFrame(grid_cells, crs="EPSG:32646")
print(f"\nTotal cells before clip: {len(grid)}")

# Clip to Dhaka boundary
grid_clipped = gpd.clip(grid, dhaka_utm)
print(f"Total cells after clip: {len(grid_clipped)}")

# Calculate centroids in UTM, then transform to WGS84
centroids_wgs84 = grid_clipped.geometry.centroid.to_crs("EPSG:4326")
grid_clipped["lon"] = centroids_wgs84.x.values
grid_clipped["lat"] = centroids_wgs84.y.values

# Save
output_path = "01_data/processed/dhaka_grid_500m.shp"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
grid_clipped.to_file(output_path)

# Also save as CSV with just grid_id and coordinates (lightweight)
csv_path = "01_data/processed/dhaka_grid_500m.csv"
grid_clipped[["grid_id", "lon", "lat"]].to_csv(csv_path, index=False)

print(f"\nGrid saved to: {output_path}")
print(f"CSV saved to: {csv_path}")
print("\nGrid summary:")
print(f"  Cell size: {cell_size}m x {cell_size}m")
print(f"  Total cells: {len(grid_clipped)}")
study_area_km2 = grid_clipped.geometry.area.sum() / 1_000_000
print(f"  Study area: {study_area_km2:.2f} km^2")