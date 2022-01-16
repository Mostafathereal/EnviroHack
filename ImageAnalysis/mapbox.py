from icecream import ic
import requests # The requests package allows use to call URLS
import shutil   # shutil will be used to copy the image to the local
import mercantile

lat_lng = [43.640918, -79.371478]
delta=0.000005
north = lat_lng[0]+delta
south = lat_lng[0]-delta
east = lat_lng[1]+delta
west = lat_lng[1]-delta

# tl = [lat_lng[0]+delta, lat_lng[1]-delta]
# br = [lat_lng[0]-delta, lat_lng[1]+delta]

# mercantile.xy()

allTiles = mercantile.tiles(east=east, south=south, north=north, west=west, zooms=18)
counter = 0
for t in allTiles:
    counter += 1
    r =requests.get('https://api.mapbox.com/v4/mapbox.satellite/'+str(t.z)+'/'+str(t.x)+'/'+str(t.y)+'@2x.pngraw?access_token=pk.eyJ1IjoibW9zdGFmYXRoZXJlYWwiLCJhIjoiY2t5Z2s5cW14MHRnODMxcGw4eTd1bjhtMCJ9.wdYeqrlK23OWOhGuyWl-Wg', stream=True)

    with open('/Users/mostafamohsen/Documents/uni/hacks/EnviroHack/ImageAnalysis/satellite_images/' + str(t.x) + '.' + str(t.y) + '.png', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


ic(counter)


# # Loop over the tile ranges
# for i,x in enumerate(range(x_tile_range[0],x_tile_range[1]+1)):
#     for j,y in enumerate(range(y_tile_range[0],y_tile_range[1]+1)):

#         # Call the URL to get the image back
#         r = requests.get('https://api.mapbox.com/v4/mapbox.terrain-rgb/'+str(z)+'/'+str(x)+'/'+str(y)+'@2x.pngraw?access_token=pk.eyJ1I....', stream=True)

#         # Next we will write the raw content to an image
#         with open('./elevation_images/' + str(i) + '.' + str(j) + '.png', 'wb') as f:
#             r.raw.decode_content = True
#             shutil.copyfileobj(r.raw, f) 
#         # Do the same for the satellite data
#         r =requests.get('https://api.mapbox.com/v4/mapbox.satellite/'+str(z)+'/'+str(x)+'/'+str(y)+'@2x.pngraw?access_token=pk.eyJ1I....', stream=True)

#         with open('./satellite_images/' + str(i) + '.' + str(j) + '.png', 'wb') as f:
#             r.raw.decode_content = True
#             shutil.copyfileobj(r.raw, f)