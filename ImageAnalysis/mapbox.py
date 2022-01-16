from icecream import ic
import requests # The requests package allows use to call URLS
import shutil   # shutil will be used to copy the image to the local
import mercantile

from PIL import Image
import math
from os import listdir
from os.path import isfile, join

lat_lng = [43.640919, -79.371478]
delta=0.05
north = lat_lng[0]+delta
south = lat_lng[0]-delta
east = lat_lng[1]+delta
west = lat_lng[1]-delta


allTiles = mercantile.tiles(east=east, south=south, north=north, west=west, zooms=16)
counter = 0
for t in allTiles:
    counter += 1
    r =requests.get('https://api.mapbox.com/v4/mapbox.satellite/'+str(t.z)+'/'+str(t.x)+'/'+str(t.y)+'@2x.pngraw?access_token=pk.eyJ1IjoibW9zdGFmYXRoZXJlYWwiLCJhIjoiY2t5Z2s5cW14MHRnODMxcGw4eTd1bjhtMCJ9.wdYeqrlK23OWOhGuyWl-Wg', stream=True)

    with open('./satellite_images/' + str(t.x) + '.' + str(t.y) + '.png', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


ic(counter)

x_tile_range = [0, 0]
y_tile_range = [0, 0]
for i, t in enumerate(allTiles):
    if i == 0:
        x_tile_range[0] = t.x
        y_tile_range[0] = t.y

    x_tile_range[1] = t.x
    y_tile_range[1] = t.y

# Loop over the elevation and satellite image set
for img_name in ['satellite']:

    # Make a list of the image names
    image_files = ['./' + img_name + '_images/' + f for f in listdir('./' + img_name + '_images/')]

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
    for i in range(0,edge_length_x):
        x_offset = 0
        for j in range(0,edge_length_y):

            # Open up the image file and paste it into the composed image at the given offset position
            tmp_img = Image.open('./' + img_name + '_images/' + str(i) + '.' + str(j) + '.png')
            composite.paste(tmp_img, (y_offset,x_offset))
            x_offset += width # Update the width

        y_offset += height # Update the height

# Save the final image
composite.save('./composite_images/'+ img_name + '.png')


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