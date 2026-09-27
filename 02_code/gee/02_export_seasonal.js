// Seasonal export: same months every year (Dec 1 – Feb 28)
// This ensures consistent comparisons across years

var dhaka = ee.FeatureCollection(
  "projects/dhaka-green-space-thesis/assets/dhaka_boundary_shp"
);

var years = [2000, 2005, 2010, 2015, 2020, 2025];

years.forEach(function(year) {
  // December of previous year to February of current year
  var start = ee.Date.fromYMD(year - 1, 12, 1);
  var end = ee.Date.fromYMD(year, 2, 28);
  
  var collection;
  if (year < 2013) {
    collection = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
      .filterBounds(dhaka)
      .filterDate(start, end)
      .filter(ee.Filter.lt('CLOUD_COVER', 30));  // relaxed to get more images
  } else {
    collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
      .filterBounds(dhaka)
      .filterDate(start, end)
      .filter(ee.Filter.lt('CLOUD_COVER', 30));
  }
  
  var count = collection.size().getInfo();
  print('Year ' + year + ' (Dec-Feb): ' + count + ' images');
  
  if (count === 0) {
    print('⚠️ No images for ' + year + ' — skipping');
    return;
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
    description: 'NDVI_' + year + '_seasonal',
    folder: 'Dhaka_Seasonal',
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
    description: 'NDBI_' + year + '_seasonal',
    folder: 'Dhaka_Seasonal',
    scale: 30,
    region: dhaka.geometry(),
    maxPixels: 1e13
  });
  
  // LST
  var lst;
  if (year < 2013) {
    lst = composite.select('ST_B6')
      .multiply(0.00341802).add(149.0).subtract(273.15)
      .rename('LST');
  } else {
    lst = composite.select('ST_B10')
      .multiply(0.00341802).add(149.0).subtract(273.15)
      .rename('LST');
  }
  
  Export.image.toDrive({
    image: lst,
    description: 'LST_' + year + '_seasonal',
    folder: 'Dhaka_Seasonal',
    scale: 30,
    region: dhaka.geometry(),
    maxPixels: 1e13
  });
});

// MODIS Nighttime LST — same seasonal window
years.forEach(function(year) {
  var start = ee.Date.fromYMD(year - 1, 12, 1);
  var end = ee.Date.fromYMD(year, 2, 28);
  
  var modis = ee.ImageCollection('MODIS/061/MOD11A1')
    .filterBounds(dhaka)
    .filterDate(start, end)
    .select('LST_Night_1km');
  
  var lst_night = modis.mean()
    .multiply(0.02).subtract(273.15)
    .rename('LST_Night').clip(dhaka);
  
  Export.image.toDrive({
    image: lst_night,
    description: 'LST_Night_' + year + '_seasonal',
    folder: 'Dhaka_Seasonal',
    scale: 1000,
    region: dhaka.geometry(),
    maxPixels: 1e13
  });
});

print('✅ All seasonal export tasks created');
print('Files will go to Google Drive folder: Dhaka_Seasonal');