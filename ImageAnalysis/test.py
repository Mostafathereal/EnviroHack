# import folium
# from folium import plugins

import geetools

import ee
# import folium
# from folium import plugins
from IPython.display import Image
from landIndex import *
from landRGB import *
import cv2

from icecream import ic

try:
    ee.Initialize()

except Exception as e:
    print("EXCEPTION: ", e)
    print("please authenticate: ")
    ee.Authenticate()
    ee.Initialize()

# col = ee.ImageCollection("LANDSAT/LC08/C01/T1_8DAY_NDWI")
# # col = ee.ImageCollection("LANDSAT/LC08/C01/T1")

# # img = ee.Image("SKYSAT/GEN-A/PUBLIC/ORTHO/RGB")
# # ee.ImageCollection("SKYSAT/GEN-A/PUBLIC/ORTHO/RGB")

# i_date = '2015-01-01'
# f_date = '2015-12-10'

# lat, lon = 23.8634, 69.1328

# u_poi = ee.Geometry.Point(lon, lat)

# # col = col.select(['R', 'G', 'B'])#.filterDate(i_date, f_date)
# # temporalFiltered = col.filterBounds(u_poi).filterDate('2015-01-01', '2015-12-31')
# # sortedd = temporalFiltered.sort('CLOUD_COVER');

# # lst_urban_point = lst.mean().sample(u_poi, scale).first().get(indexName).getInfo()

# # lst_img = lst.mean()

# col = col.select(['NDWI'])

# # scene = col.first();
# scene = col.mean()

# # ic(scene.getInfo())

# roi = u_poi.buffer(1e4)

# url = scene.getDownloadUrl({
#     'bands': ['NDWI'],
#     'region': roi,
#     # 'scale': 0.8,
#     'format': 'NPY',
#     "dimensions": [700, 700]
# })

# response = requests.get(url)
# data = np.load(io.BytesIO(response.content))

# # convert data into 0-255 grayscale image array
# image = data.astype(np.float32)
# # image = (image + 1) * 127.5
# image = image.astype(np.uint8)
# ic(image)
# ic(np.max(image))
# print(image.shape)

# cv2.imshow('B', image)
# cv2.waitKey(0)

# # Create a URL to the styled image for a region around France.
# # url = scene.getThumbUrl({
# #     'min': 0.0, 'max': 255.0, 'dimensions': 1024, 'region': roi, 'bands': ['R'], 'palette': ['000000', 'ffffff']})
# # print('\nPlease wait while the thumbnail loads, it may take a moment...')
# # print(url)

# # Define the point of interest
# # u_poi = ee.Geometry.Point(lon, lat)

# # lst = col.toArray(3)

# # ic(scene.getInfo())



# # ic(lst.select(['R']).getInfo())


###########################################################################################################

import geetools

# StartDate= ee.Date.fromYMD(2015,1,16)
# EndDate = ee.Date.fromYMD(2021,10,17)

# Area = ee.Geometry.Polygon(
#         [[[-97.93534101621628, 49.493287372441955],
#           [-97.93534101621628, 49.49105034378085],
#           [-97.93049158231736, 49.49105034378085],
#           [-97.93049158231736, 49.493287372441955]]])

# collection = ee.ImageCollection('SKYSAT/GEN-A/PUBLIC/ORTHO/RGB').filterDate(StartDate,EndDate).filterBounds(Area)

# # d_type = 'int8'
# name_pattern = '{system_date}'
# date_pattern = 'yMMdd' # dd: day, MMM: month (JAN), y: year
# scale = 10
# folder_name = 'GEE_Images'

# tasks = geetools.batch.Export.imagecollection.toDrive(
#             collection=collection,
#             folder=folder_name ,
#             region=Area ,
#             namePattern=name_pattern,
#             scale=scale,
#             # dataType=d_type,
#             datePattern=date_pattern,
#             verbose=True,
#             maxPixels=1e10
#         )
##########################################################################################


# geometry = ee.Geometry.Polygon(
#     [[[-155.97117211519446, 20.09006980142336],
#       [-155.97117211519446, 19.7821681268256],
#       [-155.73256280122962, 19.7821681268256],
#       [-155.73256280122962, 20.09006980142336]]], None, False)

# image = ee.Image('SKYSAT/GEN-A/PUBLIC/ORTHO/RGB/s01_20161020T214047Z').clip(geometry).uint8()

# skysat.visualize(['R', 'G', 'B'], min = 0, max = 255, forceRgbOutput=True)

#################################################################
image = ee.Image('SKYSAT/GEN-A/PUBLIC/ORTHO/RGB/s01_20161020T214047Z')

geom = ee.Geometry.Polygon(
  [[[-116.8, 44.7],
    [-116.8, 42.6],
    [-110.6, 42.6],
    [-110.6, 44.7]]], None, False)

#   geom = img.geometry().getInfo();
geetools.batch.Export.image(image, image.get('system:index').getInfo());
