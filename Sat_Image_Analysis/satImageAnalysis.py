from glob import glob

import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

import rasterio as rio

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

import plotly.graph_objects as go

np.seterr(divide='ignore', invalid='ignore')


## Read Data
S_sentinel_bands = glob("../Data//sundarbans_data/*B?*.tiff")

print("here")
print(S_sentinel_bands)

S_sentinel_bands.sort()

l = []

for i in S_sentinel_bands:
  with rio.open(i, 'r') as f:
    l.append(f.read(1))

arr_st = np.stack(l)

## visualize bands
ep.plot_bands(arr_st,
              cmap = 'gist_earth',
              figsize = (20, 12),
              cols = 6,
              cbar = False)
plt.show()

# RGB Composite Image

rgb = ep.plot_rgb(arr_st,
                  rgb=(3,2,1),
                  figsize=(10, 16))
plt.show()

# RGB Composite Image with Strech
# stretch remove the darkness in the pixels
ep.plot_rgb(arr_st,
            rgb=(3, 2, 1),
            stretch=True,
            str_clip=0.2,
            figsize=(10, 16))
plt.show()


## histograms
colors = ['tomato', 'navy', 'MediumSpringGreen', 'lightblue', 'orange', 'blue',
          'maroon', 'purple', 'yellow', 'olive', 'brown', 'cyan']

ep.hist(arr_st,
        colors = colors,
        title=[f'Band-{i}' for i in range(1, 13)],
        cols=3,
        alpha=0.5,
        figsize = (12, 10))

plt.show()


############### Vegetation and soil indexes
## Normalized difference vegetation index (NDVI)
ndvi = es.normalized_diff(arr_st[7], arr_st[3])

ep.plot_bands(ndvi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))

plt.show()

## Soil adjusted vegetation index (SAVI)
## L depends on vegetation coverage from [-1, 1]
## L is 1 if no vegetation coverage, L is 0.5 if moderate vegetation coverage and L = 0 if high vegetation coverage
L = 0.5

savi = ((arr_st[7] - arr_st[3]) / (arr_st[7] + arr_st[3] + L)) * (1 + L)

ep.plot_bands(savi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))

plt.show()

## Visibility Atmospherically Resistant Index (VARI)

vari = (arr_st[2] - arr_st[3])/ (arr_st[2] + arr_st[3] - arr_st[1])

ep.plot_bands(vari, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))

plt.show()

############### water indexes
## modified normalized difference water index (MNDWI)
mndwi = es.normalized_diff(arr_st[2], arr_st[10])

ep.plot_bands(mndwi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))

plt.show()

## normalized difference moisture index (NDMI) monitor moisture levels, can be used to monitor droughts and fire prone area.
ndmi = es.normalized_diff(arr_st[7], arr_st[10])

ep.plot_bands(ndmi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))

plt.show()

############### geologiy indices
## clay minerals
cmr = np.divide(arr_st[10], arr_st[11])

ep.plot_bands(cmr, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))

plt.show()

## ferrous minerals
fmr = np.divide(arr_st[10], arr_st[7])

ep.plot_bands(fmr, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))

plt.show()
