"""
Quick visualization of NDVI for 2000 and 2025
"""
import rasterio
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

for idx, year in enumerate([2000, 2025]):
    path = f"01_data/raw/processed_rasters/NDVI_{year}_seasonal.tif"
    with rasterio.open(path) as src:
        data = src.read(1)
        # Mask nodata
        data = np.where(data < -10, np.nan, data)
    
    ax = axes[idx]
    im = ax.imshow(data, cmap='RdYlGn', vmin=-0.2, vmax=0.8)
    ax.set_title(f'NDVI {year}', fontsize=16)
    plt.colorbar(im, ax=ax, fraction=0.046)
    
    print(f"{year} NDVI stats:")
    print(f"  Mean: {np.nanmean(data):.4f}")
    print(f"  Min:  {np.nanmin(data):.4f}")
    print(f"  Max:  {np.nanmax(data):.4f}")
    print(f"  % pixels > 0.3 (green): {100 * np.sum(data > 0.3) / data.size:.2f}%")
    print()

plt.tight_layout()
plt.savefig("03_results/figures/ndvi_check.png", dpi=150)
print("Saved: 03_results/figures/ndvi_check.png")