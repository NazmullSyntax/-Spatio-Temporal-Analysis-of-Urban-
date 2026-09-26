"""Create a simplified GeoJSON boundary for upload to Google Earth Engine."""
from pathlib import Path

import geopandas as gpd


ROOT = Path(__file__).resolve().parents[2]
BOUNDARY_DIR = ROOT / "01_data" / "raw" / "boundaries"
INPUT_PATH = BOUNDARY_DIR / "dhaka_district.shp"
OUTPUT_PATH = BOUNDARY_DIR / "dhaka_simple.geojson"
PROJECTED_CRS = "EPSG:32646"
SIMPLIFY_TOLERANCE_METERS = 100


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Dhaka boundary not found: {INPUT_PATH}")

    dhaka = gpd.read_file(INPUT_PATH)
    if dhaka.crs is None:
        raise ValueError(f"Boundary has no CRS: {INPUT_PATH}")
    if "NAME_2" not in dhaka.columns:
        raise ValueError("Boundary is missing the required NAME_2 column")

    simplified = dhaka.to_crs(PROJECTED_CRS)
    simplified.geometry = simplified.geometry.simplify(
        SIMPLIFY_TOLERANCE_METERS,
        preserve_topology=True,
    )
    simplified = simplified[["NAME_2", "geometry"]].rename(
        columns={"NAME_2": "name"}
    )
    simplified = simplified.to_crs("EPSG:4326")

    if not simplified.geometry.is_valid.all():
        raise ValueError("Simplification produced an invalid geometry")

    simplified.to_file(OUTPUT_PATH, driver="GeoJSON")
    size_kb = OUTPUT_PATH.stat().st_size / 1024

    print("Simplified Dhaka boundary for GEE")
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Tolerance: {SIMPLIFY_TOLERANCE_METERS} m")
    print(f"File size: {size_kb:.2f} KB")


if __name__ == "__main__":
    main()