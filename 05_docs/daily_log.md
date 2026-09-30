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

## Day 7 (Complete)
### Done
- Fixed data coverage to 6,315 cells (100%)
- Retrained Gradient Boosting (R² = 0.739)
- Generated 2030 prediction for all grid cells
- Computed uncertainty bounds
- Created 2030 prediction maps
- Chapter 1.7 written

### Key Findings
- 2025 mean LST: 26.28°C
- 2030 predicted: 26.53°C
- Change: +0.25°C
- 95% CI: [26.52, 26.55]
- Nighttime warming +1.94°C (larger than daytime +1.24°C)

### Files Created
- 03_results/prediction_2030.csv (6315 rows)
- 03_results/maps/prediction_2030_vs_2025.png
- 03_results/figures/lst_2025_vs_2030_distribution.png

### Next (Day 8)
- Population exposure analysis
- Heat risk zones
- Health/economic associations

## Day 8
### Done
- Population exposure analysis for 2025 and 2030
- Heat class categorization (Low, Moderate, High, Extreme)
- Population exposed to >28°C and >30°C thresholds
- Top 20 hotspot cells identified
- Heat exposure maps created (2 maps)
- Chapter 2 (Literature Review) drafted (2000+ words)

### Key Findings (fill from output)
- Population > 28°C: 2025 = ___, 2030 = ___
- Population > 30°C: 2025 = ___, 2030 = ___
- Extreme heat zones: ___ cells

### Files Created
- 03_results/tables/heat_exposure_2025.csv
- 03_results/tables/heat_exposure_2030.csv
- 03_results/tables/population_exposure.csv
- 03_results/tables/top_hotspot_cells_2030.csv
- 03_results/maps/heat_exposure_2025_vs_2030.png
- 03_results/maps/heat_zones_2030.png
- 04_thesis/chapters/chapter2_literature.md

### Next (Day 9)
- Health association analysis
- Economic association analysis
- Complete Chapter 2