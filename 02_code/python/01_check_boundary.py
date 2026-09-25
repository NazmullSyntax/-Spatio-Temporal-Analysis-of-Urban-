"""
Check Dhaka boundary shapefile
"""
import geopandas as gpd
import os

print("=" * 60)
print("Checking Dhaka Boundary Shapefile")
print("=" * 60)

# Check if file exists first
shp_path = "01_data/raw/boundaries/gadm41_BGD_shp/gadm41_BGD_2.shp"

if not os.path.exists(shp_path):
    print(f"❌ File not found: {shp_path}")
    print()
    print("You need to download the GADM Bangladesh shapefile first!")
    print("Go to: https://gadm.org/download_country.html")
    print("Download Bangladesh → Shapefile")
    print("Extract to: 01_data/raw/boundaries/")
    exit()

# Load Bangladesh district boundary
bd_districts = gpd.read_file(shp_path)

print(f"✅ Loaded shapefile successfully")
print(f"Total districts: {len(bd_districts)}")
print(f"Columns: {list(bd_districts.columns)}")
print()

# Filter to Dhaka
dhaka = bd_districts[bd_districts['NAME_2'] == 'Dhaka']

if len(dhaka) == 0:
    print("❌ Dhaka not found in shapefile")
    print(f"Available names: {bd_districts['NAME_2'].unique()[:10]}")
    exit()

print("Dhaka District Info:")
print(f"  Name: {dhaka['NAME_2'].values}")
print(f"  Division: {dhaka['NAME_1'].values}")
print(f"  CRS: {dhaka.crs}")
print()

# Save Dhaka boundary alone
output_path = "01_data/raw/boundaries/dhaka_district.shp"
dhaka.to_file(output_path)
print(f"✅ Saved Dhaka boundary as {output_path}")