import ee
import numpy as np
import requests
import io
import cv2
from icecream import ic
import base64
# import folium
# from folium import plugins
from IPython.display import Image

def getIndex(lat, lon, startDate, endDate, landIndexDataset, indexName, scale=30, palette=['brown', 'white', 'green'], bufferZone=1e4):
    ## a collection of `ee.images`
    lst = ee.ImageCollection(landIndexDataset)

    # Selection of appropriate bands and dates for LST.
    lst = lst.select(indexName).filterDate(startDate, endDate)

    # Define the point of interest
    u_poi = ee.Geometry.Point(lon, lat)

    lst_urban_point = lst.mean().sample(u_poi, scale).first().get(indexName).getInfo()
    ic(lst_urban_point)
    # Define a region of interest with a buffer zone of 1000 km around Lyon.
    roi = u_poi.buffer(bufferZone)

    lst_img = lst.mean()

    # # Create a URL to the styled image for a region around France.
    # url = lst_img.getThumbUrl({
    #     'min': -1, 'max': 1, 'dimensions': 1024, 'region': roi,
    #     'palette': palette})
    # print('\nPlease wait while the thumbnail loads, it may take a moment...')
    # print(url)

    # Display the thumbnail land surface temperature in France.
    # Image(url=url)
    url = lst_img.getDownloadUrl({
        'bands': [indexName],
        'region': roi,
        'scale': scale,
        'format': 'NPY',
    })
    response = requests.get(url)
    data = np.load(io.BytesIO(response.content))

    # convert data into 0-255 grayscale image array
    image = data.astype(np.float32)
    image = (image + 1) * 127.5
    image = image.astype(np.uint8)

    print(image.shape)

    # show converted image
    # cv2.imshow(indexName, image)
    # cv2.waitKey(0)

    # decode into base64 string
    _, image_bytes = cv2.imencode('.jpg', image)
    image_bytes = image_bytes.tobytes()
    im_b64 = base64.b64encode(image_bytes)
    b64_string = im_b64.decode('ascii')

    # return base 64 image string
    return b64_string

    # Additional code for decoding base64 string into image

    # im_bytes = base64.b64decode(im_b64)
    # im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    # img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    #
    # cv2.imshow(indexName, img)
    # cv2.waitKey(0)
