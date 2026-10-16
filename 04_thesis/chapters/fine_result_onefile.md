Dhaka Green Space Thesis — Basic Data Inventory

1. Study Area Boundary Data
Purpose: To define the geographical area used for the Dhaka green space analysis.
SL	File / Folder Name	Purpose	Status
1	dhaka_district.shp	Stores the geographical boundary	File available
2	dhaka_district.shx	Supports shapefile geometry indexing	File available
3	dhaka_district.dbf	Stores boundary attribute data	File available
4	dhaka_district.prj	Stores coordinate reference system information	File available
5	dhaka_simple.geojson	Provides the boundary in GeoJSON format	File available
6	dhaka_boundary.zip	Archived boundary dataset	File available
7	dhaka_boundary_shp.zip	Archived shapefile dataset	File available
8	gadm41_BGD_shp	Administrative boundary dataset	Folder available

2. Processed Data Inventory
Purpose: To document the processed datasets available for analyzing green space changes, spatial patterns, and environmental conditions in Dhaka.
SL	File Name	Purpose	Status
1	dhaka_green_space_master.csv	Main processed dataset, potentially combining multiple research variables	Available; columns not yet verified
2	dhaka_grid_500m.shp	Stores the 500-meter grid geometry for spatial analysis	File available
3	dhaka_grid_500m.csv	Contains tabular data associated with the 500-meter grid	Available; contents not yet verified
4	dhaka_grid_500m.dbf	Stores attribute data for the grid shapefile	File available
5	dhaka_grid_500m.shx	Supports shapefile geometry indexing	File available
6	dhaka_grid_500m.prj	Stores the grid's coordinate reference system	File available
7	dhaka_grid_500m.cpg	Specifies the character encoding for attribute data	File available

3. Research Scripts and Their Purposes
Purpose: To document the Python scripts available in the project and explain how they may contribute to the research workflow.
SL	Python File	Purpose	Status
1	test_environment.py	Checks whether the Python environment and required libraries work	File available
2	01_check_boundary.py	Checks the study-area boundary	File available
3	02_simplify_boundary.py	Simplifies the boundary geometry	File available
4	03_simplify_boundary.py	Another boundary simplification script; exact difference needs checking	File available
5	04_verify_rasters.py	Verifies raster datasets	File available
6	05_create_grid.py	Creates a spatial grid for the study area	File available
7	06_zonal_statistics.py	Calculates raster statistics within spatial zones or grid cells	File available
8	08_plot_ndvi.py	Plots NDVI data or vegetation patterns	File available
9	09_merge_population.py	Merges population data with other research data	File available
10	10_statistical_analysis.py	Performs statistical analysis	File available
11	11_machine_learning.py	Runs machine-learning analysis	File available
12	12_predict_2030.py	Implements a 2030 prediction workflow	File available
13	13_predict_2030_fixed.py	A revised version of the 2030 prediction script	File available
14	14_predict_2030_full.py	A more extensive 2030 prediction workflow	File available
15	15_population_exposure.py	Analyzes population exposure to environmental conditions	File available
16	16_population_exposure_fixed.py	A revised population-exposure script	File available
17	17_health_impact.py	Analyzes potential health impacts	File available
18	18_economic_impact.py	Analyzes potential economic impacts	File available


4. Merging Population Data into the Master Dataset
Script used: 02_code/python/09_merge_population.py
Purpose: To combine population estimates with the existing environmental dataset so that vegetation, surface temperature, built-up areas, and population can be analyzed together.
4.1 What I Did
1. Loaded the existing master dataset.
2. Loaded the population dataset containing six year-specific population estimates.
3. Integrated population information into the master dataset.
4. Updated the master CSV file.
5. Printed sample records and checked population values by year.
4.2 Results Obtained
Item	Result
Total master dataset rows	37,890
Total columns	10
Population records	6
First year	2000
Last year	2025
Environmental variables	NDVI, NDBI, LST, LST_Night
Spatial variables	grid_id, lon, lat
Population variables	Population, Density_per_km2
4.3 Population Data Summary
Year	Population
2000	10,500,000
2005	12,500,000
2010	14,500,000
2015	17,500,000
2020	21,000,000
2025	23,000,000
4.4 Understanding the Output
- NDVI: Indicates vegetation greenness.
- NDBI: Indicates built-up characteristics.
- LST: Land Surface Temperature during the daytime or the specified observation period.
- LST_Night: Nighttime Land Surface Temperature, where available.
- Population: Population estimate assigned to a record.
- Density_per_km2: Population density per square kilometre.


Script used: 02_code/python/10_statistical_analysis.py
Purpose: To analyze changes in vegetation, built-up characteristics, and land surface temperature in Dhaka from 2000 to 2025, and examine statistical relationships between these variables.
1. What I Did
1. Loaded the master dataset containing 37,890 records.
2. Calculated yearly averages and standard deviations for NDVI, NDBI, daytime LST, and nighttime LST.
3. Performed Pearson correlation analysis to measure relationships between vegetation, built-up characteristics, and temperature.
4. Built a multiple linear regression model to examine how NDVI and NDBI relate to daytime LST.
5. Analyzed linear time trends for the four environmental variables.
6. Saved the analysis outputs in the 03_results/ folder.
2. Descriptive Statistics
Year	Mean NDVI	Mean NDBI	Mean LST (°C)	Mean Night LST (°C)
2000	0.1598	-0.0565	25.0460	14.7783
2005	0.1530	-0.0651	24.5917	16.0973
2010	0.0997	-0.0543	24.5258	14.7436
2015	0.1716	-0.0733	25.5897	15.6405
2020	0.1757	-0.0708	25.1119	14.9349
2025	0.1767	-0.0665	26.2818	16.7166
Interpretation: Mean daytime LST was higher in 2025 than in 2000. NDVI declined between 2000 and 2010, then increased in the subsequent observations. Therefore, the results do not show a continuous decline in the study area's mean NDVI across the entire period.
3. Correlation Analysis
The script retained 9,726 complete observations for its correlation and regression analyses.
Relationship	Pearson correlation (r)	Interpretation
NDVI vs. daytime LST	-0.0827	Very weak negative relationship
NDBI vs. daytime LST	+0.6128	Stronger positive relationship
NDVI vs. nighttime LST	-0.4312	Moderate negative relationship
NDBI vs. nighttime LST	+0.3666	Moderate positive relationship
The script reports p-values as 0.0. This generally means the values are smaller than the displayed numerical precision, not that the true p-values are exactly zero.
Interpretation: NDBI had the strongest observed correlation with daytime LST. Higher NDBI values were associated with higher temperatures, while NDVI was negatively associated with nighttime LST.
These are statistical associations; they do not independently prove causation.
4. Multiple Linear Regression
Model: Daytime LST predicted using NDVI and NDBI.
Metric	Result
Observations	9,726
R-squared	0.522
Adjusted R-squared	0.522
F-statistic	5,303
NDVI coefficient	+13.0039
NDBI coefficient	+36.3686
The fitted equation is:
\[
\text{LST}=25.5257+13.0039(\text{NDVI})+36.3686(\text{NDBI})
\]

Interpretation:
- The model explains approximately 52.2% of the observed variation in daytime LST within the analyzed sample.
- Both coefficients are positive in this fitted model, after accounting for the other included variable.
- Both coefficients have reported p-values below 0.001.
The positive NDVI coefficient in the multiple regression does not match the weak negative NDVI–LST correlation. This can happen because regression coefficients account for the other predictor, NDBI. Check multicollinearity, year effects, spatial dependence, and model assumptions before interpreting the coefficients as environmental effects.
5. Time Trend Analysis
Variable	Estimated trend per year	p-value	Statistical significance at 5%
Daytime LST	+0.0503 °C/year	0.1117	Not significant
Nighttime LST	+0.0406 °C/year	0.3475	Not significant
NDVI	+0.00128/year	0.4185	Not significant
NDBI	-0.00049/year	0.2032	Not significant
Interpretation: All four estimated trends were statistically nonsignificant at the 5% level. The positive temperature slopes suggest an upward tendency in the fitted linear trends, but this analysis does not provide sufficient evidence to conclude that the long-term trends are statistically different from zero.
6. Expected Outputs
The terminal confirms that the script completed and saved files to 03_results/. The exact filenames and contents have not yet been provided.
Expected types of outputs from this analysis include:
- Yearly descriptive statistics.
- Correlation results.
- Regression summary.
- Time-trend estimates.
- Tables or graphs, if the script saves them.



Script used: 02_code/python/11_machine_learning.py
Purpose: To train and compare machine-learning models that predict Land Surface Temperature (LST) using environmental and population-related variables.
1. What I Did
1. Loaded the master dataset containing 37,890 records.
2. Removed records with missing values required for the analysis, leaving 9,726 complete observations.
3. Selected five input features: NDVI, NDBI, nighttime LST, population, and year.
4. Selected daytime LST as the target variable.
5. Split the data into training and testing sets.
6. Trained three machine-learning models.
7. Compared their prediction errors and R² scores.
8. Compared feature importance across the models.
9. Saved the selected model to a file.
2. Dataset Preparation
Item	Result
Original dataset rows	37,890
Complete observations used	9,726
Input features	5
Training samples	7,780
Testing samples	1,946
Target variable	LST
Input features: NDVI, NDBI, LST_Night, Population, Year.
Target: Daytime Land Surface Temperature (LST).
3. Model Comparison Results
Model	MAE	RMSE	R²
Random Forest	0.6854	0.9269	0.7314
XGBoost	0.6810	0.9115	0.7402
Gradient Boosting	0.6829	0.9103	0.7409
Assuming LST is measured in °C, MAE and RMSE are also expressed in °C. Confirm the units of the input data before final reporting.
Interpretation
- Random Forest: R² = 0.7314, explaining about 73.14% of the test-set variation according to the reported metric.
- XGBoost: R² = 0.7402, with a slightly lower MAE than Random Forest.
- Gradient Boosting: R² = 0.7409, the highest R² and lowest RMSE among the three models.
Selected model: Gradient Boosting, based on its highest R² and lowest RMSE in the reported comparison.
4. Feature Importance
Feature	Random Forest	XGBoost	Gradient Boosting
NDBI	0.5481	0.5277	0.5842
NDVI	0.2087	0.1467	0.1949
LST_Night	0.0935	0.0466	0.0489
Population	0.0771	0.2790	0.1192
Year	0.0726	0.0000	0.0529
Interpretation
1. NDBI has the highest reported feature importance across all three models.
2. NDVI is the second most important feature in Random Forest and Gradient Boosting.
3. Population has considerably higher importance in XGBoost than in the other two models.
4. Year has low importance in these fitted models, and XGBoost reports zero importance.
Feature importance indicates how the models use variables for prediction. It does not prove that NDBI causes higher temperatures or that vegetation loss directly causes temperature increases.
5. Saved Output
Model file:
03_results/models/best_model_lst.pkl


Script used: 02_code/python/14_predict_2030_full.py
Purpose: To estimate daytime Land Surface Temperature (LST) for 2030 across the Dhaka study area's 500-meter grid cells using historical environmental data from 2000 to 2025 and a machine-learning model.
1. What I Did
1. Loaded the master dataset containing 37,890 records.
2. Identified 6,315 unique grid cells across six observation years.
3. Checked data availability for NDVI, NDBI, daytime LST, and nighttime LST.
4. Filled missing values in the environmental variables.
5. Retrained the prediction model using the available historical data.
6. Calculated historical trends for each environmental variable.
7. Generated predicted daytime LST values for 2030 across all 6,315 grid cells.
8. Saved the predictions to a CSV file.
2. Dataset Overview
Item	Result
Total records	37,890
Unique grid cells	6,315
Historical years	2000, 2005, 2010, 2015, 2020, 2025
Grid size	500 m, according to the project grid name
Grid cells with 2025 data	6,315
Grid cells with both 2000 and 2025 records	6,315
Predicted grid cells for 2030	6,315
The script reports 6,295 available observations per year for NDVI, NDBI, and daytime LST, and 1,621 for nighttime LST, before missing-value filling.
3. Model Performance
Metric	Result
Model R²	0.7388
Model MAE	0.7084°C
Training samples	30,312
Interpretation: The reported R² indicates that the model explains approximately 73.88% of the variation in the data used for its evaluation, depending on how that metric was calculated. The MAE indicates an average absolute prediction error of about 0.71°C on the evaluation data, assuming the reported evaluation was performed in degrees Celsius.
Important: These metrics do not, by themselves, establish the accuracy of the 2030 forecast. The script's evaluation method needs to be checked.
4. Historical Trends Used by the Script
Variable	Estimated trend per year
NDVI	+0.000673
NDBI	-0.000400
Daytime LST	+0.0494°C
Nighttime LST	+0.0775°C
Interpretation: The script estimates upward temperature trends and a slight upward NDVI trend, alongside a slight downward NDBI trend. These are calculated trends in the available data; they do not establish that these patterns will continue unchanged through 2030.
5. Main 2030 Prediction Results
Predicted mean daytime LST
2025 baseline
26.28°C

2030 prediction
26.53°C



Difference in mean LST
+0.25°C


Prediction statistic	Result
Minimum predicted LST	21.34°C
Maximum predicted LST	32.20°C
Standard deviation	1.35°C
Reported 95% CI	26.52–26.55°C
Interpretation: The model predicts a mean daytime LST increase of approximately 0.25°C from 2025 to 2030. This is a model-based estimate, not a confirmed future measurement.
The reported 95% confidence interval is very narrow. Before interpreting it as uncertainty around the 2030 forecast, verify how it was calculated. It may represent uncertainty in a mean rather than the range of possible future outcomes.
6. Output File
Saved file: 03_results/prediction_2030.csv

Script used: 02_code/python/16_population_exposure_fixed.py
Purpose: To estimate how many people live in grid cells with different daytime land surface temperature (LST) levels in 2025 and under a simulated 2030 warming scenario.
1. What I Did
1. Loaded the environmental and population data for the study area.
2. Used the 2025 observed LST values as the baseline.
3. Applied a uniform warming shift of \(+0.25^\circ C\) to estimate the 2030 scenario.
4. Classified grid cells by temperature thresholds.
5. Estimated population exposure above each threshold for 2025 and 2030.
6. Calculated changes in exposed population and percentages.
7. Generated a comparison map named heat_exposure_2025_vs_2030.png.
2. Main Inputs and Outputs
Item	Result
2025 mean LST	26.28°C
Simulated 2030 mean LST	26.53°C
Assumed warming shift	+0.25°C
Population total used	25,000,000
Grid cells	6,315
Reported average population per cell	3,959
Map output	heat_exposure_2025_vs_2030.png
Important: This is a scenario analysis based on a uniform temperature shift, not an independent estimate of future population or a direct measurement of future heat exposure.
3. Population Exposed Above Temperature Thresholds
Temperature threshold	2025 population	2030 scenario	Increase	Increase (%)
Above 25°C	21,749,802	23,044,338	1,294,536	5.95%
Above 26°C	12,672,209	14,901,029	2,228,820	17.59%
Above 27°C	7,090,261	8,103,721	1,013,460	14.29%
Above 28°C	3,618,368	4,457,640	839,271	23.19%
Above 29°C	1,100,554	1,528,107	427,553	38.85%
Above 30°C	233,570	352,335	118,764	50.85%
Above 31°C	63,341	67,300	3,958	6.25%
Above 32°C	15,835	27,711	11,876	75.00%
These thresholds overlap. For example, people exposed above 30°C are also included in the counts above 29°C and 28°C. Do not add these rows together.
4. 2030 Heat Exposure Classes
Temperature class	Grid cells	Estimated population	Percentage of cells
Low (below 25°C)	494	1,955,661	7.82%
Moderate (25–28°C)	4,695	18,586,700	74.35%
High (28–30°C)	1,037	4,105,305	16.42%
Extreme (above 30°C)	89	352,336	1.41%
Interpretation: Under the simulated 2030 scenario, most grid cells fall within the moderate temperature class. Approximately 1.41% of cells are classified as extreme, with an estimated population of about 352,336.
5. Main Findings for the Thesis
- Population estimated to be in grid cells above 28°C increases from approximately 3.62 million in 2025 to 4.46 million in 2030.
- Population estimated to be in grid cells above 30°C increases from approximately 233,571 to 352,336.
- The model estimates an increase of approximately 839,272 people above 28°C and 118,765 above 30°C.
- These are scenario-based exposure estimates, not predictions of confirmed illness, deaths, or individual health outcomes.
6. Important Data Quality Checks
Before using these figures in the final thesis, verify the following:
1. Population allocation: The script reports an average of 3,959 people per cell. Check whether this is a real grid-level population estimate or whether the same average population was assigned to every grid cell. If every cell receives the same population, the exposure estimates will depend mainly on the number of cells above each threshold.
2. Temperature thresholds: LST is satellite-measured land surface temperature, not the same as air temperature or a person's actual heat exposure. Explain this distinction in the thesis.
3. Scenario assumptions: The 2030 values use a uniform \(+0.25^\circ C\) shift. This assumes the same warming increment across the study area.
4. Rounding: Some summary values differ by one person from the threshold table. Use a consistent calculation and rounding method in the final report.
7. Output File
- Map: heat_exposure_2025_vs_2030.png

02_code/python/17_health_impact.py
Purpose: Estimate possible heat-related health impacts in Dhaka for 2025 and 2030 using heat-exposure estimates and literature-based assumptions.
2. What I Did
1. Loaded data for 6,315 grid cells across Dhaka.
2. Used the estimated population of 25 million.
3. Compared average land surface temperature (LST) in 2025 and 2030.
4. Applied literature-based assumptions about health risks when LST exceeds 30°C.
5. Estimated possible heat-related deaths, hospitalizations, and emergency department (ED) visits.
6. Saved health-exposure maps.
3. Main Results
Measurement	2025	2030
Mean LST	26.28°C	26.53°C
Population exposed above 30°C	233,571	352,336
Estimated heat-related deaths	12	18
Estimated hospitalizations	118	177
Estimated ED visits	484	729
4. Assumptions Used
Parameter	Assumed value
Heat threshold	30°C
Mortality increase	2% per °C
Hospitalization increase	1% per °C
ED visit increase	5% per °C
Baseline mortality rate	5 per 100,000/year
Baseline hospitalization rate	50 per 100,000/year
Baseline ED visit rate	200 per 100,000/year
These are literature-based model assumptions, not verified Dhaka-specific health statistics.
5. Interpretation
- The estimated population exposed above 30°C increases by approximately 118,765 people between 2025 and 2030.
- Estimated deaths increase from approximately 12 to 18 under the model's assumptions.
- Estimated hospitalizations increase from approximately 118 to 177.
- Estimated ED visits increase from approximately 484 to 729.
These figures represent model-based estimates, not confirmed numbers of actual deaths or hospital visits.
6. Important Limitations
1. LST is not air temperature. Satellite-measured land surface temperature does not directly represent the temperature experienced by people.
2. The 30°C threshold and health-risk coefficients need appropriate scientific sources and justification.
3. The estimates depend on baseline health rates and the method used to calculate heat exposure.
4. The results do not prove that green-space loss caused these health outcomes.
5. The model does not establish actual hospital admissions or deaths in Dhaka.
7. Output Files
- Health exposure maps: Saved by the script. The exact filenames and folder were not shown in the terminal output.

02_code/python/18_economic_impact.py
Purpose: Estimate possible economic costs associated with increased cooling electricity demand, worker productivity loss, and heat-related health impacts by 2030.
2. What I Did
1. Used the projected temperature increase of 0.25°C from 2025 to 2030.
2. Estimated additional electricity needed for cooling.
3. Estimated possible productivity losses among outdoor workers.
4. Calculated estimated economic costs associated with the health-impact results.
5. Combined these estimates into a total annual economic burden.
3. Main Results
Economic impact	Estimated annual cost (USD)
Extra cooling electricity	$4,000,000
Worker productivity loss	$180,000,000
Health-related costs	$1,857,473
Total estimated burden	$185,857,473
Estimated total annual economic burden by 2030
$185.86 million
Approximately ৳20.44 billion per year, using the script's assumed exchange rate.

4. Calculations and Assumptions
A. Cooling electricity
- Baseline electricity: 12.5 billion kWh/year
- Cooling portion: 40% = 5 billion kWh/year
- Assumed extra demand: 1% = 50 million kWh/year
- Estimated additional cost: $4 million/year
B. Worker productivity
- Assumed outdoor workers: 7.5 million
- Average annual wage: $2,400
- Total wage bill: $18 billion
- Assumed productivity loss: 1%
Estimated annual productivity loss: $180 million.
C. Health-related costs
Item	Estimated annual cost
Premature deaths	$1,785,572
Hospitalizations	$35,473
Emergency visits	$36,428
Total	$1,857,473
These health costs use the estimated health outcomes from the previous script and assumed costs per case.
5. Interpretation
- Worker productivity loss is the largest component of the estimated economic burden.
- Additional cooling electricity and heat-related health costs contribute to the total.
- The results suggest that heat exposure could have economic implications worth investigating in Dhaka.
Important: These are scenario-based estimates, not verified measurements of actual economic losses caused by green-space decline.
6. Output File
03_results/tables/economic_burden_2030.csv

result
The folder contains 12 result files.
No.	File name	Purpose
1	correlation_results.csv	Relationships between NDVI, NDBI, and LST
2	descriptive_by_year.csv	Yearly mean and standard deviation
3	economic_burden_2030.csv	Estimated economic costs for 2030
4	feature_importance.csv	Importance of features in ML models
5	health_burden.csv	Estimated heat-related health impacts
6	heat_exposure_2025.csv	Heat exposure estimates for 2025
7	heat_exposure_2030.csv	Heat exposure estimates for 2030
8	model_comparison.csv	Comparison of machine-learning models
9	population_exposure.csv	Population exposed at different temperature thresholds
10	regression_lst.txt	Detailed LST regression results
11	time_trends.csv	Trends in temperature and vegetation indices
12	top_hotspot_cells_2030.csv	Grid cells identified as potential 2030 hotspots

2. Figures Found
The output shows 8 image files.
No.	File name	Purpose
1	actual_vs_predicted.png	Compare actual LST values with model predictions
2	correlation_matrix.png	Visualize relationships between numerical variables
3	feature_importance.png	Show which features contribute most to model predictions
4	lst_2025_vs_2030_distribution.png	Compare temperature distributions for 2025 and 2030
5	ndvi_check.png	Inspect NDVI data or vegetation patterns
6	scatter_ndvi_ndbi_vs_lst.png	Show relationships between NDVI, NDBI, and LST
7	temporal_trends.png	Visualize changes over time
8	test_plot.png	Test figure; purpose needs verification


2. Maps Found
The output shows 4 map files.
No.	File name	Purpose
1	health_exposure_maps.png	Visualize areas associated with estimated heat exposure and health impacts
2	heat_exposure_2025_vs_2030.png	Compare population heat exposure between 2025 and the 2030 scenario
3	heat_zones_2030.png	Show different temperature or heat-exposure zones for 2030
4	prediction_2030_vs_2025.png	Compare the 2025 temperature data with the 2030 prediction


2. Model Found
Item	Details
File name	best_model_lst.pkl
File size	435,688 bytes (approximately 426 KB)
Last modified	17 October 2026, 2:53 AM
File format	.pkl — Python pickle
Intended purpose	Store the trained model for LST prediction

File Found
Item	Details
File name	prediction_2030.csv
Location	03_results\prediction_2030.csv
File size	834,408 bytes (approximately 815 KB)
Last modified	17 October 2026, 2:53 AM
Expected purpose	Store the 2030 LST predictions for individual grid cells

Model Comparison and 2030 Temperature Prediction

2. Master Dataset
Item	Result
Total rows	37,890
Total columns	10
Years covered	2000–2025
Grid cells	6,315 per year
Explanation: The dataset contains 37,890 records across six years. With 6,315 grid cells per year, the total matches \(6,315 \times 6 = 37,890\).
3. Machine Learning Model Comparison
Model	MAE (°C)	RMSE (°C)	R²
Random Forest	0.6854	0.9269	0.7314
XGBoost	0.6810	0.9115	0.7402
Gradient Boosting	0.6829	0.9103	0.7409
Explanation of the metrics:
- MAE: Average absolute prediction error. Lower is better.
- RMSE: Prediction error metric that penalizes larger errors more strongly. Lower is better.
- R²: Indicates how much variation in the target temperature is explained by the model on the evaluated data. Higher is better.
Finding: Gradient Boosting has the highest R² (0.7409) and lowest RMSE (0.9103°C), so it performs best among these three models on the reported evaluation. XGBoost has a slightly lower MAE.
4. Feature Importance
Feature importance shows which input variables the models relied on most when predicting LST.
Feature	Random Forest	XGBoost	Gradient Boosting
NDBI	54.81%	52.77%	58.42%
NDVI	20.87%	14.67%	19.49%
LST_Night	9.35%	4.66%	4.89%
Population	7.71%	27.90%	11.92%
Year	7.26%	0.00%	5.29%
Main findings:
- NDBI is the most important feature in all three models. NDBI is an index commonly used to indicate built-up surfaces.
- NDVI is the second-most important feature in the Random Forest and Gradient Boosting models. NDVI is used to assess vegetation.
- Population importance varies considerably between models.
- Year has zero importance in XGBoost in this particular model.
Important: feature importance does not establish causation. It does not prove that built-up areas or vegetation changes alone caused the temperature patterns.
5. Predicted Average LST for 2030
Predicted mean land surface temperature, 2030
26.53°C
Modelled estimate across the 6,315 grid cells.

This is a model prediction, not a temperature measurement from 2030. The reliability of the estimate depends on how future input variables were generated and whether the model was properly tested on data not used for training.
6. Overall Conclusion
The results show that Gradient Boosting performed best overall by R² and RMSE among the three tested models. NDBI was the most influential feature, followed by NDVI in two of the models. The predicted mean LST for Dhaka's grid cells in 2030 is 26.53°C.
These findings are preliminary model results. They should not yet be interpreted as proof of future temperature changes caused by green-space loss.