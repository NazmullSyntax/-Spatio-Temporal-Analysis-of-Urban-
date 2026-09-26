import os
import rasterio

folder = "01_data/raw/processed_rasters"

if not os.path.exists(folder):
    print(f"❌ Folder not found: {folder}")
    exit()

print("=" * 60)
print("Verifying Downloaded Rasters")
print("=" * 60)

files = sorted([f for f in os.listdir(folder) if f.endswith('.tif')])
total_size = 0

for f in files:
    path = os.path.join(folder, f)
    size_mb = os.path.getsize(path) / (1024 * 1024)
    total_size += size_mb
    
    with rasterio.open(path) as src:
        print(f"✅ {f:30s} — {size_mb:.2f} MB — {src.shape}")

print("=" * 60)
print(f"Total files: {len(files)}")
print(f"Total size: {total_size:.2f} MB")
print("=" * 60)
