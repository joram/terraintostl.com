import math
import os
from typing import Optional

import gdal
import rasterio
from rasterio import DatasetReader


class GeoTIFFS:

    def __init__(self):
        self.geotiffs = {}

    def get(self, lat, lng) -> Optional["GeoTIFF"]:
        lat = math.floor(lat)
        lng = math.floor(lng)
        ew = "w" if lat < 0 else "e"
        ns = "n" if lng > 0 else "s"

        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = f"{dir_path}/../../data/clean/{ns}{lng}_{ew}{int(math.fabs(lat))}_1arc_v3.tif"
        if not os.path.exists(filename):
            return None
        if filename not in self.geotiffs:
            self.geotiffs[filename] = GeoTIFF(filename)
        return self.geotiffs[filename]

    def get_height(self, lat, lng) -> float:
        geotiff = self.get(lat, lng)
        if geotiff is None:
            return 0

        return geotiff.get_height(lat, lng)


class GeoTIFF:

    def __init__(self, filename: str, band_id=1):
        dataset: DatasetReader = rasterio.open(filename, driver='GTiff')
        self.band_arr = dataset.read(band_id)

        img = gdal.Open(filename)
        t = img.GetGeoTransform()
        self.git = gdal.InvGeoTransform(t)[1]
        self.left = dataset.bounds.left
        self.right = dataset.bounds.right
        self.top = dataset.bounds.top
        self.bottom = dataset.bounds.bottom
        self.height = self.top-self.bottom
        self.width = self.right-self.left

    def get_height(self, lat, lng) -> float:
        x = int(self.width) - int((lng - self.bottom)/self.height * self.git)
        y = int((lat - self.left)/self.width * self.git)
        v = self.band_arr[x, y]

        # # TODO: fix this hack
        # if v == -32767:
        #     try:
        #         return self.get_height(lat, lng+0.0001)
        #     except:
        #         return 0

        return v

