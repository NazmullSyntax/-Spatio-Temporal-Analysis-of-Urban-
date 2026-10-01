# Chapter 3: Methodology

## 3.1 Study Area
## 3.2 Data Sources
## 3.3 Satellite Data Acquisition
## 3.4 Preprocessing
## 3.5 NDVI Calculation
## 3.6 NDBI Calculation
## 3.7 Land Surface Temperature
## 3.8 Grid-Based Spatial Analysis
## 3.9 Population Data
## 3.10 Statistical Analysis
## 3.11 Machine Learning
## 3.12 2030 Prediction
## 3.13 Health and Economic Estimation
## 3.14 Validation and Uncertainty
## 3.15 Software and Reproducibility
## 3.16 Limitations of Methodology

 3.1 Study Area

 ### 3.1.1 Geographic Location

Dhaka District is located in central Bangladesh, at approximately 
23.78°N latitude and 90.40°E longitude. The district is bounded by 
the Padma River to the south, the Dhaleshwari River to the west, and 
Gazipur District to the north. It is the administrative district 
containing Dhaka, the capital of Bangladesh.

### 3.1.2 Administrative Boundary

The study area is defined by the GADM (Global Administrative Areas) 
Level 2 boundary for Dhaka District. GADM is a widely used, publicly 
available spatial database of administrative boundaries. The Level 2 
boundary represents the district level — the second administrative 
tier in Bangladesh.

**Selection criteria for Dhaka District boundary:**
1. It is the official administrative unit containing the urban core
2. It provides a consistent boundary across all satellite years
3. It encompasses all major urban zones (Uttara, Mirpur, Gulshan, 
   Dhanmondi, Motijheel, Old Dhaka, Savar, Keraniganj)
4. It aligns with data availability from Bangladesh Bureau of Statistics

**Boundary properties:**
- Total area: 1,463.61 km²
- Administrative level: GADM Level 2 (District)
- Coordinate Reference System (geographic): EPSG:4326 (WGS 84)
- Coordinate Reference System (projected): EPSG:32646 (UTM Zone 46N)

### 3.1.3 Population

Dhaka District's population grew from approximately 10.5 million in 
2000 to over 23 million in 2025 (BBS Census 2022, UN World 
Urbanization Prospects). This rapid growth — averaging 2.1% annually 
— has driven urban expansion, infrastructure development, and land-
use change.

### 3.1.4 Urban Characteristics

Dhaka is characterized by:
- One of the highest urban population densities in the world 
  (>15,000 persons/km²)
- Rapid formal and informal urban expansion
- Mixed land use — residential, commercial, industrial interwoven
- Limited planned green space (parks, gardens)
- Significant heat island effect

### 3.1.5 Climate

Dhaka experiences a tropical monsoon climate (Köppen: Aw):
- **Winter (December–February)**: Cool, dry; temperatures 12–25°C
- **Pre-monsoon (March–May)**: Hot; temperatures 25–35°C
- **Monsoon (June–September)**: Hot, humid, heavy rain
- **Post-monsoon (October–November)**: Warm, transition

The **December–February** period was selected for satellite composites 
due to minimal cloud cover and stable atmospheric conditions.

### 3.1.6 Analysis Grid

A 500m × 500m grid was created over the study area:
- Total cells: 6,315
- Total area covered: ~1,578 km²
- Cell area: 0.25 km²
- CRS: EPSG:32646 (UTM Zone 46N)

Each grid cell serves as the fundamental analysis unit. This grid size 
was selected to balance:
- **Spatial resolution**: Fine enough to capture intra-urban variation
- **Statistical power**: Large enough for meaningful analysis
- **Computational efficiency**: Manageable dataset size

 Fill Section 3.2 — Data Sources 

 ### 3.2.1 Satellite Imagery

**Landsat Collection 2 Level-2 Surface Reflectance**
- **Source**: USGS Earth Resources Observation and Science (EROS) Center
- **Access**: Google Earth Engine (`LANDSAT/LT05/C02/T1_L2`, `LANDSAT/LC08/C02/T1_L2`)
- **Landsat 5 TM (Thematic Mapper)**: Used for 2000, 2005, 2010
- **Landsat 8 OLI (Operational Land Imager)**: Used for 2015, 2020, 2025
- **Spatial resolution**: 30m (multispectral), 100m resampled (thermal)
- **Temporal resolution**: 16-day revisit
- **Spectral bands used**:
  - Red (Band 3 for Landsat 5; Band 4 for Landsat 8)
  - NIR (Band 4 for Landsat 5; Band 5 for Landsat 8)
  - SWIR (Band 5 for Landsat 5; Band 6 for Landsat 8)
  - Thermal (Band 6 for Landsat 5; Band 10 for Landsat 8)
  - QA_PIXEL (cloud mask)

**MODIS MOD11A1 (Nighttime LST)**
- **Source**: NASA LP DAAC via Google Earth Engine
- **Access**: `MODIS/061/MOD11A1`
- **Spatial resolution**: 1 km
- **Temporal resolution**: Daily
- **Band used**: LST_Night_1km
- **Purpose**: Nighttime surface temperature for heat retention analysis

### 3.2.2 Time Points

Six time points were selected at 5-year intervals:
- 2000, 2005, 2010, 2015, 2020, 2025

This 5-year interval balances:
- **Temporal resolution**: Sufficient to capture change
- **Data availability**: Avoids years with poor image availability
- **Computational efficiency**: Manageable number of time slices
- **Trend detection**: Adequate for regression analysis

### 3.2.3 Population Data

**Sources**:
- Bangladesh Bureau of Statistics (BBS) — Census 2011, 2022
- UN World Urbanization Prospects
- World Bank population indicators

**Data collected**:
- Total population by year
- Population density per km²
- Annual growth rate

**Limitation**: Grid-level (500m) population data is not available for 
Dhaka. Total district population was distributed uniformly across the 
6,315 grid cells (approximately 3,960 persons per cell in 2025).

### 3.2.4 Economic Data

**Sources**:
- Bangladesh Bank (CPI, wage index)
- Bangladesh Power Development Board (electricity data)
- World Bank (GDP per capita)
- ILO (productivity loss coefficients)

**Data collected**:
- GDP per capita
- Electricity consumption
- CPI and wage index
- Cooling demand indicators

### 3.2.5 Data Sources Summary Table

| Dataset | Variable | Source | Years | Resolution |
|---------|----------|--------|-------|------------|
| Landsat 5 TM | NDVI, NDBI, LST | USGS/GEE | 2000–2010 | 30m |
| Landsat 8 OLI | NDVI, NDBI, LST | USGS/GEE | 2015–2025 | 30m |
| MODIS MOD11A1 | Nighttime LST | NASA/GEE | 2000–2025 | 1km |
| GADM Level 2 | Boundary | GADM | — | Vector |
| BBS Census | Population | BBS | 2001, 2011, 2022 | District |
| World Bank | Economic data | World Bank | 2000–2025 | National |

3.3 Satellite Data Acquisition:

All satellite data were accessed through the Google Earth Engine (GEE) 
platform. GEE provides a cloud-based environment for planetary-scale 
geospatial analysis, with direct access to the Landsat and MODIS 
archives.

### 3.3.1 Landsat Image Selection

For each target year (2000, 2005, 2010, 2015, 2020, 2025), Landsat 
imagery was filtered to the December–February window (dry season) 
using:

- `filterBounds(dhaka_boundary)` — Spatial filter
- `filterDate(Dec 1, Feb 28)` — Temporal filter  
- `filter(CLOUD_COVER < 30%)` — Scene-level cloud filter

The December–February window ensures:
1. Minimal cloud cover for South Asian region
2. Consistent seasonal state across all years
3. Comparable vegetation and thermal conditions

**Why not all months?** Using different months for different years 
creates artificial trends due to seasonal NDVI variation. This is a 
common pitfall in multi-year studies.

### 3.3.2 Pixel-Level Cloud Masking

Scene-level cloud cover does not guarantee pixel-level cloud-free 
data. A scene labeled "10% cloudy" may have cloud pixels spread 
throughout the image.

To address this, the QA_PIXEL band was used for pixel-level masking:

```javascript
var qa = image.select('QA_PIXEL');
var mask = qa.bitwiseAnd(1 << 3).eq(0)   // No cloud
  .and(qa.bitwiseAnd(1 << 4).eq(0))      // No cloud shadow
  .and(qa.bitwiseAnd(1 << 1).eq(0));     // No dilated cloud
return image.updateMask(mask);


3.3 Composite Generation


Under `## 3.5 NDVI Calculation`:

```markdown
### 3.5.1 Formula

NDVI (Normalized Difference Vegetation Index) is calculated as:
NDVI = (NIR − Red) / (NIR + Red)

Where:
- NIR = Near-Infrared reflectance
- Red = Red reflectance

### 3.5.2 Landsat Band Mapping

| Satellite | Red Band | NIR Band |
|-----------|----------|----------|
| Landsat 5 TM | Band 3 (SR_B3) | Band 4 (SR_B4) |
| Landsat 8 OLI | Band 4 (SR_B4) | Band 5 (SR_B5) |

### 3.5.3 Value Interpretation

- NDVI > 0.3: Vegetated area
- 0.1 < NDVI < 0.3: Sparse vegetation
- -0.1 < NDVI < 0.1: Bare soil or built-up
- NDVI < -0.1: Water

### 3.5.4 Google Earth Engine Implementation

```javascript
var ndvi = composite.normalizedDifference(['SR_B5', 'SR_B4'])
  .rename('NDVI');

(The normalizedDifference function computes (b1-b2)/(b1+b2))


Under `## 3.6 NDBI Calculation`:

```markdown
### 3.6.1 Formula

NDBI (Normalized Difference Built-up Index) is calculated as:

NDBI = (SWIR − NIR) / (SWIR + NIR)

### 3.6.2 Landsat Band Mapping

| Satellite | SWIR Band | NIR Band |
|-----------|-----------|----------|
| Landsat 5 TM | Band 5 (SR_B5) | Band 4 (SR_B4) |
| Landsat 8 OLI | Band 6 (SR_B6) | Band 5 (SR_B5) |

### 3.6.3 Value Interpretation

- NDBI > 0.1: Built-up area
- NDBI ≈ 0: Bare soil
- NDBI < 0: Vegetation or water
## 3.7 Land Surface Temperature:

### 3.7.1 Daytime LST (Landsat Thermal)

LST was derived from Landsat thermal bands using the standard 
single-channel algorithm provided by USGS Collection 2 Level 2 
processing:

LST (°C) = DN × 0.00341802 + 149.0 - 273.15


Where:
- DN = Digital Number of thermal band
- 0.00341802 = Scaling factor
- 149.0 = Offset (Kelvin)
- 273.15 = Kelvin to Celsius conversion

**Thermal bands used:**
- Landsat 5 TM: ST_B6
- Landsat 8 OLI/TIRS: ST_B10

**Note**: LST is the temperature of the Earth's surface (roads, 
roofs, vegetation), NOT the air temperature. LST and air temperature 
are correlated but distinct physical quantities.

### 3.7.2 Nighttime LST (MODIS)

MODIS MOD11A1 provides nighttime LST at 1km resolution:

#LST_Night (°C) = DN × 0.02 - 273.15

Where:
- DN = Digital Number of LST_Night_1km band
- 0.02 = Scaling factor (Kelvin)
- 273.15 = Kelvin to Celsius conversion

Annual mean of daily nighttime LST was computed for each study year.

### 3.7.3 Handling Missing LST_Night Data

MODIS 1km resolution is coarser than the 500m analysis grid. As a 
result, some grid cells lacked direct LST_Night coverage.

**Filling strategy:**
1. For each cell, use the cell's own multi-year mean if available
2. For cells with no LST_Night at all, use the city-level mean for that year

About 74% of cells required filling. This is documented as a 
limitation.

## 3.8 Grid-Based Spatial Analysis:

### 3.8.1 Grid Creation

A fishnet grid was created over the Dhaka District boundary using:

- **Cell size**: 500m × 500m
- **CRS**: EPSG:32646 (UTM Zone 46N — appropriate for Bangladesh)
- **Cells generated**: 12,168 before clipping
- **Cells after clipping to boundary**: 6,315

The grid was created using the `shapely` and `geopandas` Python 
libraries:

```python
from shapely.geometry import box
x_coords = np.arange(xmin, xmax, 500)
y_coords = np.arange(ymin, ymax, 500)
# ... create box(x, y, x+500, y+500) for each cell

3.8.2 Zonal Statistics

from rasterstats import zonal_stats
stats = zonal_stats(
    grid_geometry,
    raster_values,
    affine=raster_transform,
    stats=['mean'],
    nodata=raster_nodata
)

# This produced a panel dataset:

Rows: 37,890 (6,315 cells × 6 years)

Columns: grid_id, Year, NDVI, NDBI, LST, LST_Night, lon, lat


Under `## 3.10 Statistical Analysis`:

```markdown
### 3.10.1 Descriptive Statistics

For each year and each variable, the following were computed:
- Mean, standard deviation
- Minimum, maximum
- Percentiles (25th, 50th, 75th)

### 3.10.2 Correlation Analysis

Pearson correlation coefficients were computed between all pairs of 
environmental variables (NDVI, NDBI, LST, LST_Night). Significance 
testing used two-tailed t-tests at α = 0.05.

### 3.10.3 Multiple Linear Regression

Model specification:

LST = β₀ + β₁·NDVI + β₂·NDBI + ε


Where:
- LST = Land Surface Temperature (dependent)
- NDVI, NDBI = predictors
- β₀, β₁, β₂ = coefficients
- ε = error term

Diagnostics included:
- R² (goodness of fit)
- Adjusted R²
- F-statistic (overall significance)
- t-tests for individual coefficients
- Durbin-Watson (autocorrelation)
- Variance Inflation Factor (multicollinearity)

### 3.10.4 Time Trend Analysis

For each variable (NDVI, NDBI, LST, LST_Night), annual mean values 
were regressed against time:

```python
slope, intercept, r, p, se = stats.linregress(years, annual_means)

# Reported metrics:

Slope (change per year)

R²

p-value


Under `## 3.11 Machine Learning`:

```markdown
### 3.11.1 Model Selection

Three ensemble machine learning models were evaluated:
1. **Random Forest** (Breiman, 2001)
2. **XGBoost** (Chen & Guestrin, 2016)
3. **Gradient Boosting** (Friedman, 2001)

These were selected because they:
- Handle non-linear relationships
- Provide feature importance
- Are robust to outliers
- Do not require feature scaling
- Are widely used in urban remote sensing

### 3.11.2 Features and Target

**Features (5):**
- NDVI
- NDBI
- LST_Night
- Population
- Year

**Target:**
- LST (daytime land surface temperature)

### 3.11.3 Data Split

Training/testing split:
- 80% training (30,312 samples)
- 20% testing (7,578 samples)

Random seed set to 42 for reproducibility.

### 3.11.4 Model Parameters

**Random Forest:**
- n_estimators = 100
- max_depth = 15
- random_state = 42

**XGBoost:**
- n_estimators = 100
- max_depth = 6
- learning_rate = 0.1
- random_state = 42

**Gradient Boosting:**
- n_estimators = 100
- max_depth = 5
- learning_rate = 0.1
- random_state = 42

### 3.11.5 Evaluation Metrics

- **R²**: Coefficient of determination
- **MAE**: Mean Absolute Error
- **RMSE**: Root Mean Squared Error

Models were compared and the best performer (highest R², lowest MAE) 
was retained for prediction.

### 3.11.6 Feature Importance

Feature importance was extracted from each model. Random Forest uses 
Gini importance; XGBoost uses gain-based importance. Averages across 
models provided robust ranking.

Fill Sections 3.12 to 3.16
### 3.12.1 Prediction Strategy

The 2030 prediction uses a hybrid approach:
1. **Spatial pattern from ML model** — captures cross-sectional 
   relationships between features and LST
2. **Temporal trend adjustment** — applies empirical warming rate 
   to account for time trend

This hybrid approach addresses the low importance of the "Year" 
feature in the ML model.

### 3.12.2 Feature Projection

2030 features were projected from 2025 baseline:

| Feature | Projection Method |
|---------|-------------------|
| NDVI | 2025 value + (2000–2025 trend × 5 years) |
| NDBI | 2025 value + (2000–2025 trend × 5 years) |
| LST_Night | 2025 value + (2000–2025 trend × 5 years) |
| Population | 2025 × 1.087 (8.7% growth over 5 years) |
| Year | 2030 |

### 3.12.3 Prediction and Trend Adjustment

Predicted LST was computed, then adjusted for empirical warming:

LST_2030 = Model_Prediction + (LST_trend × 5)

Where LST_trend = 0.0494°C/year (observed 2000–2025).

### 3.12.4 Uncertainty Quantification

95% confidence intervals were computed using:

CI = Point_estimate ± 1.96 × (RMSE / √n)


Where n = number of grid cells (6,315).

## 3.13 Health and Economic Estimation:
### 3.13.1 Health Impact Estimation

**Approach**: Literature-based exposure-response coefficients applied 
to spatially resolved heat exposure.

**Heat threshold**: 30°C LST

**Exposure-response coefficients (from literature)**:
| Outcome | Rate | Increase per °C | Source |
|---------|------|-----------------|--------|
| Mortality | 5 per 100k | +2% per °C | Gasparrini et al. 2015 |
| Hospitalization | 50 per 100k | +1% per °C | Burkart et al. 2011 |
| ED visits | 200 per 100k | +5% per °C | WHO 2021 |

**Formula**:

Health_outcome = Σ (baseline_rate × (1 + coefficient × (LST - threshold)) × population)


Summed over all grid cells with LST > threshold.

### 3.13.2 Economic Impact Estimation

**Components**:
1. **Cooling electricity cost** — based on temperature elasticity of demand
2. **Worker productivity loss** — based on ILO heat-stress coefficients
3. **Health-related cost** — based on value of statistical life and 
   healthcare costs

**Coefficients**:
- Electricity demand increase: 4% per °C
- Productivity loss: 2% per °C above threshold
- Value of Statistical Life (VSL): $100,000 USD
- Cost per hospitalization: $200 USD

### 3.13.3 Important Caveats

These are **estimates** based on published coefficients, not measured 
outcomes. They should be interpreted as indicative of magnitude, not 
as precise predictions.

3.14 Validation and Uncertainty:
### 3.14.1 Model Validation

- **Train/test split**: 80/20
- **Metrics**: R², MAE, RMSE
- **Comparison**: RF vs XGBoost vs Gradient Boosting

### 3.14.2 Cross-Sectional vs Temporal Validation

Cross-sectional relationships (spatial pattern) are validated by 
train/test split. Temporal trends are validated against literature 
on Dhaka warming.

### 3.14.3 Uncertainty Sources

1. **Model error**: R² = 0.74 (26% unexplained)
2. **Scenario uncertainty**: Business-as-usual assumption
3. **Extrapolation risk**: 5-year forward prediction
4. **Data limitations**: Low NDVI, missing nighttime LST
5. **Coefficient uncertainty**: Health/economic coefficients from 
   global literature

## 3.15 Software and Reproducibility:
### 3.15.1 Software Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10 | Analysis and modeling |
| Google Earth Engine | Cloud | Satellite data processing |
| VS Code | Latest | Code development |

**Python libraries**:
- `numpy`, `pandas` — data manipulation
- `geopandas`, `rasterio`, `rasterstats` — spatial analysis
- `scikit-learn`, `xgboost` — machine learning
- `matplotlib`, `seaborn` — visualization
- `scipy`, `statsmodels` — statistical tests

### 3.15.2 Code Availability

All code is available in the GitHub repository:
https://github.com/NazmullSyntax/-Spatio-Temporal-Analysis-of-Urban-

Repository structure:
- `01_data/` — Raw and processed data
- `02_code/` — GEE and Python scripts
- `03_results/` — Figures, maps, tables
- `04_thesis/` — Thesis chapters
- `05_docs/` — Documentation

### 3.15.3 Reproducibility Statement

All analyses can be reproduced by:
1. Cloning the GitHub repository
2. Running the GEE scripts to export rasters
3. Running the Python scripts in order (01 → 18)
4. Following the documented workflow

Random seeds are set where applicable to ensure reproducibility.
## 3.16 Limitations of Methodology:
### 3.16.1 Spatial Limitations

1. **Mixed pixels**: 30m Landsat resolution may miss small features
2. **Coarse nighttime LST**: MODIS 1km resolution limits detail
3. **Uniform population distribution**: Assumes equal population 
   per grid cell — unrealistic in dense urban areas

### 3.16.2 Temporal Limitations

1. **Six time points only**: Limited statistical power for trend 
   detection
2. **5-year intervals**: May miss interannual variability
3. **Seasonal compositing**: Only Dec–Feb window analyzed

### 3.16.3 Methodological Limitations

1. **Correlation ≠ causation**: All relationships are associations
2. **ML model generalization**: Assumes current patterns continue
3. **Literature-based coefficients**: May not perfectly fit Dhaka
4. **Uniform warming**: Assumes all areas warm by same amount

### 3.16.4 Data Availability Limitations

1. **Health data**: Ward-level outcomes not available
2. **Economic data**: Household-level data only for survey years
3. **Grid population**: Uniform distribution assumed

### 3.16.5 How Limitations Are Addressed

- All claims framed as "associations" or "estimates"
- Uncertainty ranges reported alongside point estimates
- Limitations explicitly documented in each chapter
- Reproducibility enables future refinement


