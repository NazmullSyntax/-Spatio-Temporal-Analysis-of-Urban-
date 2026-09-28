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

## Day 5
### Done
- Population data merged (10.5M → 23M)
- Correlation analysis complete
- Regression: LST ~ NDVI + NDBI
- Time trends computed
- Scatter plots + time series plots created
- Chapter 1.5 written
### Key Findings
- LST trend: X.XXXX °C/year
- NDVI trend: X.XXXXX/year
- Correlation NDVI-LST: r = X.XXX
- Correlation NDBI-LST: r = X.XXX
### Next (Day 6)
- Machine learning prediction
- 2030 scenario modeling


## Day 6
### Done
- Trained Random Forest, XGBoost, Gradient Boosting
- Compared model performance (R², MAE, RMSE)
- Feature importance analysis complete
- Saved best model (03_results/models/best_model_lst.pkl)
- Chapter 1.6 written

### Key Results (fill in after running)
- Best model: [name]
- Best R²: [value]
- Top feature: [name]
- Second feature: [name]
- Third feature: [name]

### Files Created
- 03_results/tables/model_comparison.csv
- 03_results/tables/feature_importance.csv
- 03_results/figures/feature_importance.png
- 03_results/figures/actual_vs_predicted.png

### Next (Day 7)
- Load best model
- Predict 2030 NDVI, NDBI, LST
- Create 2030 prediction maps
- Compare 2025 vs 2030