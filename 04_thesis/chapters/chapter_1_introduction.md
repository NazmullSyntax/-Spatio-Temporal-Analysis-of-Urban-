# Chapter 1: Introduction

## 1.1 Background

Dhaka, the capital of Bangladesh, is one of the fastest-growing megacities in the world. With a population exceeding 22 million in the metropolitan area, the city has experienced rapid urbanization over the past two decades. This growth has come at a significant environmental cost, particularly the loss of urban green spaces such as parks, trees, wetlands, and open fields.

Urban green spaces play a critical role in regulating urban microclimates. They reduce air temperature through shading and evapotranspiration, improve air quality, and provide recreational and psychological benefits to residents. The loss of green spaces is associated with the intensification of the urban heat island (UHI) effect, a phenomenon where urban areas become significantly warmer than surrounding rural areas.

In Dhaka, the combination of rapid population growth, unplanned infrastructure development, and weak enforcement of environmental regulations has led to the conversion of green spaces into built-up areas.

The consequences of this change depend not only on the total area of green space but also on its location, condition, and continuity across the urban landscape. Large parks, roadside vegetation, wetlands, and smaller patches of tree cover each contribute differently to the local environment. As development fragments or replaces these spaces, residents may have less access to shade and recreation, while the remaining vegetation may become less connected. A city-wide measure of green-space loss can therefore conceal important differences between neighborhoods and land-cover types. Understanding where change has occurred is an important step toward identifying areas that may face greater environmental pressure.

Satellite remote sensing and geographic information systems provide a way to examine land-cover patterns across multiple points in time. By comparing mapped green space from 2000 to 2025, this study can describe the direction and spatial distribution of change in Dhaka. It also considers the relationship between green-space patterns and Land Surface Temperature (LST). LST represents the temperature of the land surface observed by satellite; it is related to, but distinct from, the air temperature experienced by people. Vegetation can moderate surface heating through shade and evapotranspiration, while built materials can store and release heat. Measuring how these patterns correspond over time can help clarify the local role of green space in Dhaka's urban thermal environment without assuming that association alone demonstrates causation.

These environmental changes also raise questions about human well-being and the costs of urban development. Greater exposure to heat can create challenges for health, comfort, and outdoor activity, while the loss of accessible green space can reduce opportunities for recreation and contact with nature. This research considers these potential health and economic implications alongside land-cover and temperature change, while recognizing that a spatial analysis cannot by itself establish individual health outcomes or quantify every economic cost. Finally, projecting green-space and heat conditions to 2030 offers a way to explore the consequences of continued trends and to inform discussion of more sustainable planning. Such projections are scenarios based on data and assumptions, rather than certain predictions of the city's future.

## 1.2 Problem Statement

[To be written tomorrow]


## 1.5 Objectives

This study pursues five specific objectives aligned with the research questions:

**Objective 1: Quantify Green Space Change**
To quantify changes in urban green space in Dhaka District from 2000 to 
2025 using NDVI derived from Landsat satellite imagery, with attention 
to data limitations inherent in low-NDVI urban environments.

**Objective 2: Analyze Built-up Expansion**
To analyze the expansion of built-up areas using NDBI and characterize 
the relationship between green space loss and urbanization.

**Objective 3: Examine the Green Space–Temperature Relationship**
To examine the statistical and spatial relationship between green space 
and land surface temperature (both daytime and nighttime) using 
correlation and regression analysis.

**Objective 4: Assess Population Exposure**
To identify and quantify population exposure to elevated urban heat in 
Dhaka, focusing on areas where green space loss has been most pronounced.

**Objective 5: Predict 2030 Scenario**
To develop a machine-learning-based prediction of green space and land 
surface temperature conditions for Dhaka in 2030 under a business-as-usual 
scenario.

### Note on Data Limitations

Preliminary analysis reveals that Dhaka District exhibits low NDVI values 
(mean 0.10–0.18) due to its already high level of urbanization. This is 
consistent with published literature on South Asian megacities. The 
research therefore focuses on relative trends rather than absolute values, 
and explicitly acknowledges this limitation throughout the analysis.

## 1.6 Significance of the Study

This research contributes to the scientific understanding of urban 
environmental change in Dhaka in several ways:

### Scientific Contributions

**1. Long-term integrated analysis**
This study provides the first continuous 25-year analysis (2000–2025) 
of green space and urban heat in Dhaka using a consistent methodology. 
Previous studies covered shorter periods or used inconsistent methods, 
limiting comparability.

**2. Multi-source spatial dataset**
The 500m grid-based dataset (6,315 cells × 6 years = 37,890 observations) 
is one of the largest integrated environmental datasets for Dhaka. It 
combines satellite-derived indices (NDVI, NDBI, LST) with population data 
and enables both cross-sectional and time-series analysis.

**3. Machine learning prediction**
The study uses Random Forest, XGBoost, and Gradient Boosting to predict 
future scenarios up to 2030. This is among the first applications of 
ensemble machine learning for urban heat prediction in Bangladesh.

**4. Reproducible workflow**
All code (Google Earth Engine scripts and Python) is publicly available 
on GitHub. This enables replication, extension, and use by other 
researchers and planning agencies.

### Policy Contributions

**1. Spatial identification of heat hotspots**
Gridded heat maps can guide Dhaka City Corporation's urban greening 
priorities — identifying where tree planting, park development, or 
cool roofs would have maximum impact.

**2. Population exposure assessment**
By combining heat maps with population data, this study identifies 
where vulnerable populations are most exposed. This supports targeted 
intervention planning.

**3. 2030 planning horizon**
The 2030 scenario aligns with the SDG target year and Bangladesh's 
national planning cycle, providing evidence for long-term climate 
adaptation strategy.

### Methodological Contributions

**1. Seasonal bias correction**
The study demonstrates a method to avoid seasonal bias in multi-year 
NDVI studies, using consistent December–February windows. This is a 
common pitfall in urban remote sensing that this research addresses 
transparently.

**2. Grid-cell panel design**
The 500m grid panel enables statistical analysis at a spatial scale 
useful for urban planning. Most Dhaka studies analyze at administrative 
levels (ward, thana) which vary greatly in size.

### SDG Alignment

The findings support:
- **SDG 3** (Good Health): Quantifying heat exposure — a health risk factor
- **SDG 11** (Sustainable Cities): Evidence for green space planning
- **SDG 13** (Climate Action): Urban heat mitigation strategy
- **SDG 15** (Life on Land): Vegetation conservation in urban areas

### Contribution to Bangladesh's Climate Plans

The study supports:
- Bangladesh Climate Change Strategy and Action Plan (BCCSAP)
- National Adaptation Programme of Action (NAPA)
- Delta Plan 2100 urban resilience goals

### Limitations of the Significance

This study does not claim to:
- Establish causal relationships between green space loss and health outcomes
- Predict exact health or economic numbers
- Replace ground-level health monitoring

It provides environmental exposure evidence that can inform, but not 
replace, detailed epidemiological and economic studies.


## 1.7 Scope and Limitations

### Scope of the Study

**Geographic Scope**
The study covers Dhaka District, Bangladesh (approximately 1,463 km²) — 
the administrative district containing Bangladesh's capital and largest 
metropolitan area, home to over 22 million people. All major urban zones 
are included: Uttara, Mirpur, Gulshan, Banani, Dhanmondi, Motijheel, 
Old Dhaka, Savar, Keraniganj, and surrounding areas. The 500m × 500m 
analysis grid contains 6,315 cells, providing comprehensive spatial 
coverage.

**Temporal Scope**
- Historical analysis: 2000–2025 (6 time points)
- Prediction: 2030 (5-year forward scenario)

**Thematic Scope**
- Urban green space (NDVI)
- Built-up intensity (NDBI)
- Land surface temperature (daytime and nighttime)
- Population exposure
- Health and economic implications (association-based)

### Limitations

**Data Limitations**

1. **Spatial resolution**: Landsat's 30m resolution may miss small urban 
   green spaces. Mixed pixels in dense urban areas reduce vegetation 
   detection accuracy.

2. **Low NDVI values**: Dhaka's NDVI values (0.10–0.18) are lower than 
   typical vegetated regions. This reflects its high urban density and 
   limits detection of subtle changes.

3. **Temporal sampling**: Six time points (5-year intervals) may miss 
   interannual variability.

4. **Nighttime LST resolution**: MODIS 1km resolution is coarser than 
   Landsat. About 74% of grid cells lacked direct LST_Night coverage; 
   these were filled using cell-level and year-level averages.

**Methodological Limitations**

1. **Statistical power**: With only 6 time points, temporal trends have 
   limited statistical significance despite clear directional change.

2. **Causation vs. association**: All reported relationships are 
   statistical associations. Satellite data cannot establish causation.

3. **Model generalization**: Machine learning models trained on past 
   data assume continuation of current patterns.

**Health and Economic Limitations**

1. **Health data**: Ward-level health outcome data are not publicly 
   available for Dhaka. Health analysis uses environmental exposure 
   quantification with literature-based estimates.

2. **Economic data**: Household-level data are only available for survey 
   years. Analysis uses district-level or national proxies.

3. **Exposure ≠ outcome**: Environmental exposure does not directly 
   predict health outcomes — individual vulnerability matters.

**Prediction Uncertainty**

1. **Model uncertainty**: R² = 0.74 leaves 26% of LST variation unexplained.

2. **Scenario uncertainty**: 2030 prediction assumes business-as-usual.

3. **Extrapolation risk**: Predicting 5 years beyond last data introduces 
   moderate uncertainty.

### How Limitations Are Addressed

All findings are framed as:
- "Associations" rather than "causes"
- "Potential burden" rather than "observed impacts"
- "Model-based scenarios" rather than "future facts"

Data limitations are documented explicitly. All code and data processing 
steps are reproducible via GitHub.