## Day 3
### Done
- GEE project registered (Community tier, free)
- Boundary shapefile uploaded to GEE Assets
- Verified boundary loads correctly in GEE
- Created export script for NDVI, NDBI, LST, LST_Night
- Submitted 24 export tasks (6 years × 4 indices)
- Tasks running in cloud
### Asset path
projects/dhaka-green-space-thesis/assets/dhaka_boundary_shp
### Next
- Wait for tasks to complete
- Download rasters from Google Drive
- Verify downloads
- Write Chapter 1.4 (Research Questions)

## Day 3 (Complete)
### Done
- GEE project registered (Community tier — free, non-commercial)
- Boundary uploaded to GEE Assets: projects/dhaka-green-space-thesis/assets/dhaka_boundary_shp
- Created export script: 02_code/gee/01_export_low_size.js
- Ran 24 export tasks in GEE
- Downloaded all 24 rasters from Google Drive
- Verified all rasters (165.69 MB total)
- Moved to 01_data/raw/processed_rasters/
### Raster Specifications
- Landsat (NDVI, NDBI, LST): 1939 × 1887 pixels @ 30m resolution
- MODIS (LST_Night): 59 × 57 pixels @ 1km resolution
- 6 years each: 2000, 2005, 2010, 2015, 2020, 2025
### Next (Day 4)
- Create 500m × 500m grid over Dhaka
- Extract zonal statistics per grid cell
- Build master CSV
- Write Chapter 1.5 (Objectives)
