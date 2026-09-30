# Chapter 2: Literature Review

## 2.1 Urban Green Space

Urban green space refers to vegetated areas within cities, including 
parks, gardens, street trees, wetlands, and undeveloped land. These 
spaces provide critical ecosystem services: temperature regulation, 
air purification, stormwater management, and recreational opportunities 
(Bolund & Hunhammar, 1999; Wolch et al., 2014).

In rapidly urbanizing South Asian cities, green space loss has been 
documented across multiple studies (Taubenböck et al., 2012; 
Rahman et al., 2017). Dhaka has experienced particularly rapid 
green space conversion due to population pressure and unplanned 
development (Byomkesh et al., 2012; Ahmed et al., 2013).

## 2.2 Remote Sensing of Urban Environments

Satellite remote sensing has become the primary tool for monitoring 
urban environmental change at scale. Landsat's 40+ year archive 
provides consistent imagery suitable for multi-decadal analysis 
(Wulder et al., 2019). The Google Earth Engine platform enables 
cloud-based processing of these archives (Gorelick et al., 2017).

For urban applications, key indices include:
- Normalized Difference Vegetation Index (NDVI) — vegetation
- Normalized Difference Built-up Index (NDBI) — built-up areas
- Land Surface Temperature (LST) — thermal conditions

## 2.3 NDVI

NDVI, introduced by Tucker (1979), uses the contrast between red and 
near-infrared reflectance to estimate vegetation cover. Values range 
from −1 to +1, with higher values indicating denser vegetation.

NDVI has been widely applied to urban vegetation monitoring (Weng 
et al., 2004; Myint et al., 2015). In dense urban environments, 
mixed pixels reduce NDVI sensitivity. Studies of Dhaka report 
anomalously low NDVI values (0.1–0.3) compared to vegetated 
regions (Byomkesh et al., 2012).

## 2.4 NDBI

NDBI, developed by Zha et al. (2003), identifies built-up areas 
using shortwave-infrared and near-infrared reflectance. Combined 
with NDVI, it helps separate urban from vegetated surfaces. NDBI 
correlates positively with land surface temperature in most urban 
studies (Chen et al., 2006).

## 2.5 Urban Heat Island

The urban heat island (UHI) effect — where cities are warmer than 
surrounding rural areas — has been documented globally since the 
19th century (Howard, 1833). Recent studies quantify UHI intensity 
using satellite thermal data (Voogt & Oke, 2003; Imhoff et al., 2010).

In South Asian megacities, UHI intensity of 2–5°C is common. 
Dhaka studies report UHI intensity of 2–4°C between urban and 
rural areas (Akbari et al., 2016; Shahid & Karim, 2020).

## 2.6 Land Surface Temperature (LST)

LST is retrieved from satellite thermal bands using radiative 
transfer models. Landsat's thermal infrared sensors (TM Band 6, 
TIRS Band 10) provide 100m LST for Landsat 8 and 120m for 
Landsat 5.

Important distinction: LST measures the temperature of the Earth's 
surface (roads, roofs, vegetation), not the air temperature. LST 
and near-surface air temperature correlate but are not identical 
(Voogt & Oke, 2003).

## 2.7 Health Implications of Urban Heat

Heat exposure is associated with:
- Heat stroke and heat exhaustion
- Cardiovascular stress
- Respiratory complications
- Premature mortality (Gasparrini et al., 2015)

Urban heat islands exacerbate these risks in dense cities. Studies 
in Delhi, Karachi, and Kolkata report significant heat-health 
associations (Hajat et al., 2014; Burkart et al., 2011).

For Dhaka, ward-level health data is limited, but national-level 
studies suggest heat-related mortality is increasing (Rahman et al., 
2019). This thesis uses exposure-based estimation rather than 
individual health outcomes.

## 2.8 Economic Implications of Urban Heat

Heat impacts economies through:
- Increased cooling demand (electricity consumption)
- Reduced worker productivity (especially outdoor workers)
- Increased healthcare costs
- Reduced quality of life

Global estimates suggest heat-related productivity losses of 
2–4% of GDP in South Asia (ILO, 2019). For Bangladesh, cooling 
demand has increased 30%+ over the last decade (BPDB reports).

## 2.9 Machine Learning in Urban Studies

Machine learning has become standard in urban remote sensing. 
Random Forest and XGBoost are widely used for:
- Land cover classification
- LST prediction
- Urban growth modeling

Advantages: capture nonlinear relationships, handle high-dimensional 
data, provide feature importance. In urban heat studies, ML models 
commonly achieve R² = 0.6–0.9 (Zhou et al., 2020).

## 2.10 Previous Dhaka Studies

Key studies on Dhaka's urban environment:

- **Byomkesh et al. (2012)**: Analyzed land use change 1975–2005
- **Ahmed et al. (2013)**: NDVI-based green space loss
- **Akbari et al. (2016)**: UHI intensity mapping
- **Shahid & Karim (2020)**: LST and land cover relationship
- **Rahman et al. (2017)**: Urban growth and green space

Limitations of prior work:
- Short or inconsistent time periods
- Focus on one index (NDVI or LST, rarely both)
- No future prediction
- Limited health/economic integration
- Inconsistent study boundaries

## 2.11 Research Gap

This thesis addresses five gaps:

1. **Long-term integration**: 25-year continuous analysis
2. **Multi-index synthesis**: NDVI, NDBI, LST, LST_Night
3. **Machine learning prediction**: 2030 scenarios
4. **Population exposure analysis**: gridded population × heat
5. **Reproducible workflow**: open code and data

No prior study of Dhaka combines all five elements.

## 2.12 Summary

The literature establishes:
- Dhaka has experienced significant urban environmental change
- Remote sensing provides reliable tools for this analysis
- UHI intensification is a growing concern
- Health and economic implications are serious
- Machine learning offers predictive capabilities

This thesis builds on this foundation by integrating long-term 
analysis, multi-index assessment, and predictive modeling to 
provide evidence for urban planning in Dhaka.