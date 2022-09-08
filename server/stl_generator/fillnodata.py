import os

import rasterio

for filename in os.listdir("../../data/raw"):
    if filename.endswith(".tif"):
        clean_filepath = f"../../data/clean/{filename}"
        if os.path.exists(clean_filepath):
            print(f"Skipping {filename} already exists: {clean_filepath}")
            continue
        print(f"Cleaning {filename} to {clean_filepath}")
        cmd = f"gdal_fillnodata.py ../../data/raw/{filename} {clean_filepath}"
        os.system(cmd)