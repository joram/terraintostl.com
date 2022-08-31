import os

import rasterio

for filename in os.listdir("../data/raw"):
    if filename.endswith(".tif"):
        cmd = f"gdal_fillnodata.py ./data/raw/{filename} ./data/clean/{filename}"
        os.system(cmd)