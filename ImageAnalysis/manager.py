import ee
# import folium
# from folium import plugins
from IPython.display import Image
from landIndex import *
import socketio
import eventlet
import json
import torch
from land_cover_classification_unet.unet import UNet
from land_cover_classification_unet.predict import *
import shutil
import mercantile
from os import listdir
from io import BytesIO
import os
import glob
import numpy as np

from PIL import ImageStat

try:
    ee.Initialize()

except Exception as e:
    print("EXCEPTION: ", e)
    print("please authenticate: ")
    ee.Authenticate()
    ee.Initialize()

###########  LOADING MODEL  ###########################
img_scale = 1
net = UNet(n_channels=3, n_classes=7)
# logging.info("Loading model {}".format(args.model))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
logging.info(f'Using device {device}')
net.to(device=device)
model_path = "./land_cover_classification_unet/checkpoints/CP_epoch30.pth"
net.load_state_dict(torch.load(model_path, map_location=device))
logging.info("Model loaded !")
ic("loaded model ..........................")



## a collection of `ee.images`
landsatWaterIndex = 'LANDSAT/LC08/C01/T1_8DAY_NDWI'
landsatVegIndex = 'LANDSAT/LC08/C01/T1_8DAY_NDVI'
landsatBurnIndex = 'LANDSAT/LC08/C01/T1_8DAY_BAI'

i_date = '2017-01-01'
f_date = '2017-12-10'

# lat, lon = 23.8634, 69.1328
lat, lon = 25.385092, 68.356720
u_poi = ee.Geometry.Point(lon, lat)

scale = 30  # scale in meters

palette = ['ffffff', 'ff0000', 'ffff00', '00ffff', '0000ff']

# getIndex(lat, lon, i_date, f_date, landsatWaterIndex, 'NDWI', palette=palette)


def main():
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ):  ## session ID (), dictionary with details of client request
        print(sid, " connected")
        print(environ)

    @sio.event
    def my_message(sid, data):
        print('message :', data)
        print("sid: ", sid)
        lat, lon = str(data).split();
        lat, lon = float(lat), float(lon)
        ndwi_b64_string = getIndex(lat, lon, i_date, f_date, landsatWaterIndex, 'NDWI', palette=palette)
        ndvi_b64_string = getIndex(lat, lon, i_date, f_date, landsatVegIndex, 'NDVI', palette=palette)
        bai_b64_string = getBurnIndex(lat, lon, i_date, f_date, landsatBurnIndex, 'BAI', palette=palette)

        # ndvi_im = BytesIO(base64.b64decode(ndvi_b64_string))
        # ndvi_stat = ImageStat.Stat(ndvi_im)
        # print(ndvi_stat.mean)

        print('Got All Indices')

        print('Beginning Prediction')
        composite_img = satMapbox(lat, lon)

        ###############   PREDICT   #####################
        seg, mask_indices = predict_img(net=net,
                            full_img=composite_img,
                            scale_factor=img_scale,
                            out_threshold=0.5,
                            device=device)
        mask_im = Image.fromarray(seg)

        buffered = BytesIO()
        mask_im.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        img_str = img_str.decode('ascii')

        print('Prediction Done')

        # image_b64_string = getIndex(lat, lon, i_date, f_date, landsatWaterIndex, 'NDWI', palette=palette)
        dic = {"NDWIImageData": ndwi_b64_string, "NDVIImageData": ndvi_b64_string, "BAIImageData": bai_b64_string, "segImageData": img_str}
        # data = data.split()
        # jdata = json.dumps(data)
        jdata2 = json.dumps(dic)
        sio.emit("my_message_response", jdata2)

    @sio.event
    def Hello(sid, data):
        print('message :', data)

    @sio.event
    def disconnect(sid):
        print(sid, " disconnected")

    if __name__ == '__main__':
        eventlet.wsgi.server(eventlet.listen(('', 3050)), app)


def satMapbox(lat, lon):
    satPAth = './land_cover_classification_unet/satellite_images/'

    files = glob.glob(satPAth + '*')
    for f in files:
        if os.path.isfile(f):
            os.remove(f)

    lat_lng = [lat, lon]
    delta=0.005

    north = lat_lng[0]+delta
    south = lat_lng[0]-delta
    east = lat_lng[1]+delta
    west = lat_lng[1]-delta

    allTiles = mercantile.tiles(east=east, south=south, north=north, west=west, zooms=17)
    counter = 0
    for t in allTiles:
        counter += 1
        r =requests.get('https://api.mapbox.com/v4/mapbox.satellite/'+str(t.z)+'/'+str(t.x)+'/'+str(t.y)+'@2x.pngraw?access_token=pk.eyJ1IjoibW9zdGFmYXRoZXJlYWwiLCJhIjoiY2t5Z2s5cW14MHRnODMxcGw4eTd1bjhtMCJ9.wdYeqrlK23OWOhGuyWl-Wg', stream=True)

        with open(satPAth + str(t.x) + '.' + str(t.y) + '.png', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    ic(counter)

    x_tile_range = [0, 0]
    y_tile_range = [0, 0]
    allTiles = mercantile.tiles(east=east, south=south, north=north, west=west, zooms=17)
    for i, t in enumerate(allTiles):
        if i == 0:
            x_tile_range[0] = t.x
            y_tile_range[0] = t.y

        x_tile_range[1] = t.x
        y_tile_range[1] = t.y

    # Make a list of the image names
    image_files = [satPAth + f for f in listdir(satPAth)]

    # Open the image set using pillow
    images = [Image.open(x) for x in image_files]

    # Calculate the number of image tiles in each direction
    edge_length_x = x_tile_range[1] - x_tile_range[0]
    edge_length_y = y_tile_range[1] - y_tile_range[0]

    edge_length_x = max(1, edge_length_x)
    edge_length_y = max(1, edge_length_y)

    # Find the final composed image dimensions
    width, height = images[0].size
    total_width = width * edge_length_x
    total_height = height * edge_length_y

    # Create a new blank image we will fill in
    composite = Image.new('RGB', (total_width, total_height))

    # Loop over the x and y ranges
    y_offset = 0
    for i in range(x_tile_range[0], x_tile_range[1] + 1):
        x_offset = 0
        for j in range(y_tile_range[0], y_tile_range[1] + 1):

            # Open up the image file and paste it into the composed image at the given offset position
            with Image.open(satPAth + str(i) + '.' + str(j) + '.png') as tmp_img:
                composite.paste(tmp_img, (y_offset, x_offset))
            x_offset += width # Update the width

        y_offset += height # Update the height

    # composite = np.array(composite);
    # ic(composite.shape)
    # composite = Image.fromarray(composite[:, :, ::-1])
    return composite.convert('RGB')

if __name__ == '__main__':
    satPAth = './land_cover_classification_unet/satellite_images/'

    files = glob.glob(satPAth + '*')
    for f in files:
        if os.path.isfile(f):
            os.remove(f)
    main()