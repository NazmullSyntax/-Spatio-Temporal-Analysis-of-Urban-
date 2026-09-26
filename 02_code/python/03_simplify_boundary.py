"""
Simplify Dhaka boundary for GEE upload
Reduces file size from ~5 MB to ~100 KB
"""
import geopandas as gpd
import os

print("=" * 60)
print("Simplifying Dhaka Boundary for GEE")
print("=" * 60)

# Load Dhaka boundary
dhaka = gpd.read_file("01_data/raw/boundaries/dhaka_district.shp")

print(f"Original file size: {os.path.getsize('01_data/raw/boundaries/dhaka_district.shp')/1024:.2f} KB")

# Simplify geometry (tolerance ~100m)
dhaka['geometry'] = dhaka.geometry.simplify(0.001, preserve_topology=True)

# Keep only essential columns
dhaka_clean = dhaka[['NAME_2', 'geometry']].copy()
dhaka_clean = dhaka_clean.rename(columns={'NAME_2': 'name'})

# Save as GeoJSON (smaller than shapefile)
output_path = "01_data/raw/boundaries/dhaka_simple.geojson"
dhaka_clean.to_file(output_path, driver='GeoJSON')

size_kb = os.path.getsize(output_path) / 1024
print(f"Saved simplified boundary: {output_path}")
print(f"   File size: {size_kb:.2f} KB")
