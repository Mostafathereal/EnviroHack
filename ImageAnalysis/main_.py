import ee
# import folium
# from folium import plugins
from IPython.display import Image
from landIndex import *
from landRGB import *

try:
    ee.Initialize()

except Exception as e:
    print("EXCEPTION: ", e)
    print("please authenticate: ")
    ee.Authenticate()
    ee.Initialize()

## a collection of `ee.images`
landsatWaterIndex = 'LANDSAT/LC08/C01/T1_8DAY_NDWI'
landsatVegIndex = 'LANDSAT/LC08/C01/T1_8DAY_NDWI'
highResRGB = 'SKYSAT/GEN-A/PUBLIC/ORTHO/RGB'

i_date = '2015-01-01'
f_date = '2015-12-10'

lat, lon = 23.8634, 69.1328
# lat, lon = 25.385092, 68.356720
u_poi = ee.Geometry.Point(lon, lat)

scale = 30  # scale in meters

palette = ['ffffff', 'ff0000', 'ffff00', '00ffff', '0000ff']

getRGB(lat, lon, i_date, f_date, highResRGB)