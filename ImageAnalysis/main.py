import ee
# import folium
# from folium import plugins
from IPython.display import Image
from landIndex import *
import socketio
import eventlet
import json


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
        image_b64_string = getIndex(lat, lon, i_date, f_date, landsatWaterIndex, 'NDWI', palette=palette)
        dic = {"imageData": image_b64_string}
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


if __name__ == '__main__':
    main()