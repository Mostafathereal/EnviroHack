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

col = ee.ImageCollection("SKYSAT/GEN-A/PUBLIC/ORTHO/RGB")

# img = ee.Image("SKYSAT/GEN-A/PUBLIC/ORTHO/RGB")

i_date = '2015-01-01'
f_date = '2015-12-10'

lat, lon = 23.8634, 69.1328

u_poi = ee.Geometry.Point(lon, lat)

# col = col.select(['R', 'G', 'B'])#.filterDate(i_date, f_date)
# temporalFiltered = col.filterBounds(u_poi).filterDate('2015-01-01', '2015-12-31')
# sortedd = temporalFiltered.sort('CLOUD_COVER');

col = col.select(['R', 'G', 'B'])

scene = col.first();

# ic(scene.getInfo())

roi = u_poi.buffer(100)

url = scene.getDownloadUrl({
    'bands': ['G'],
    'region': roi,
    # 'scale': 0.8,
    'format': 'NPY',
    "dimensions": [700, 700]
})

response = requests.get(url)
data = np.load(io.BytesIO(response.content))

# convert data into 0-255 grayscale image array
image = data.astype(np.float32)
# image = (image + 1) * 127.5
image = image.astype(np.uint8)
ic(image)
ic(np.max(image))
print(image.shape)

cv2.imshow('B', image)
cv2.waitKey(0)

# Create a URL to the styled image for a region around France.
# url = scene.getThumbUrl({
#     'min': 0.0, 'max': 255.0, 'dimensions': 1024, 'region': roi, 'bands': ['R'], 'palette': ['000000', 'ffffff']})
# print('\nPlease wait while the thumbnail loads, it may take a moment...')
# print(url)

# Define the point of interest
# u_poi = ee.Geometry.Point(lon, lat)

# lst = col.toArray(3)

# ic(scene.getInfo())



# ic(lst.select(['R']).getInfo())


