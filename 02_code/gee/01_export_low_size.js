// Low-size GEE export: NDVI, NDBI, LST for Dhaka (2000-2025)
// Total output: ~200 MB

var dhaka = ee.FeatureCollection(
  "projects/dhaka-green-space-thesis/assets/dhaka_boundary_shp"
);

var years = [2000, 2005, 2010, 2015, 2020, 2025];

// ============================================================
// LANDSAT: NDVI, NDBI, LST
// ============================================================
years.forEach(function(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = ee.Date.fromYMD(year, 12, 31);
  
  var collection;
  if (year < 2013) {
    collection = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
      .filterBounds(dhaka)
      .filterDate(start, end)
      .filter(ee.Filter.lt('CLOUD_COVER', 10));
  } else {
    collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
      .filterBounds(dhaka)
      .filterDate(start, end)
      .filter(ee.Filter.lt('CLOUD_COVER', 10));
  }
  
  var composite = collection.median().clip(dhaka);
  
  // NDVI
  var ndvi;
  if (year < 2013) {
    ndvi = composite.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI');
  } else {
    ndvi = composite.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI');
  }
  
  Export.image.toDrive({
    image: ndvi,
    description: 'NDVI_' + year + '_Dhaka',
    folder: 'Dhaka_LowSize',
    scale: 30,
    region: dhaka.geometry(),
    maxPixels: 1e13
  });
  
  // NDBI
  var ndbi;
  if (year < 2013) {
    ndbi = composite.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDBI');
  } else {
    ndbi = composite.normalizedDifference(['SR_B6', 'SR_B5']).rename('NDBI');
  }
  
  Export.image.toDrive({
    image: ndbi,
    description: 'NDBI_' + year + '_Dhaka',
    folder: 'Dhaka_LowSize',
    scale: 30,
    region: dhaka.geometry(),
    maxPixels: 1e13
  });
  
  // LST
  var lst;
  if (year < 2013) {
    lst = composite.select('ST_B6')
      .multiply(0.00341802)
      .add(149.0)
      .subtract(273.15)
      .rename('LST');
  } else {
    lst = composite.select('ST_B10')
      .multiply(0.00341802)
      .add(149.0)
      .subtract(273.15)
      .rename('LST');
  }
  
  Export.image.toDrive({
    image: lst,
    description: 'LST_' + year + '_Dhaka',
    folder: 'Dhaka_LowSize',
    scale: 30,
    region: dhaka.geometry(),
    maxPixels: 1e13
  });
});

// ============================================================
// MODIS: Nighttime LST
// ============================================================
years.forEach(function(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = ee.Date.fromYMD(year, 12, 31);
  
  var modis = ee.ImageCollection('MODIS/061/MOD11A1')
    .filterBounds(dhaka)
    .filterDate(start, end)
    .select('LST_Night_1km');
  
  var lst_night = modis.mean()
    .multiply(0.02)
    .subtract(273.15)
    .rename('LST_Night')
    .clip(dhaka);
  
  Export.image.toDrive({
    image: lst_night,
    description: 'LST_Night_' + year + '_Dhaka',
    folder: 'Dhaka_LowSize',
    scale: 1000,
    region: dhaka.geometry(),
    maxPixels: 1e13
  });
});

print('✅ All 24 export tasks created.');
print('Go to the Tasks tab → click RUN for each task.');