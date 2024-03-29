import math
import os
from typing import Optional

import gdal
import rasterio
from numpy import ma
from rasterio import DatasetReader


class GeoTIFFS:
    def __init__(self):
        self.geotiffs = {}

    def get_geotiff(self, lat, lng) -> Optional["GeoTIFF"]:
        if lat is None or lng is None:
            return None

        lat = math.floor(lat)
        lng = math.floor(lng)
        ew = "w" if lat < 0 else "e"
        ns = "n" if lng > 0 else "s"

        dir_path = os.path.dirname(os.path.realpath(__file__))

        def get_filename():

            filename1 = f"{ns}{lng}_{ew}{abs(lat)}_1arc_v3.tif"
            filename2 = f"{ns}{lng}_{ew}0{abs(lat)}_1arc_v3.tif"
            filename3 = f"{ns}{lng}_{ew}00{abs(lat)}_1arc_v3.tif"
            for filename in [filename1, filename2, filename3]:
                clean_dir_path = f"{dir_path}/../../data/clean/"
                filepath = os.path.join(clean_dir_path, filename)
                if os.path.exists(filepath):
                    return filepath
            print(f"geotiff does not exist!: {filepath}")
            return None

        filename = get_filename()
        if filename not in self.geotiffs:
            print(f"opening geotiff {filename}")
            self.geotiffs[filename] = GeoTIFF(filename)
        return self.geotiffs[filename]

    def get_height(self, lat, lng) -> float:
        geotiff = self.get_geotiff(lat, lng)
        if geotiff is None:
            return 0

        return geotiff.get_height(lat, lng)


class GeoTIFF:
    def __init__(self, filename: str, band_id=1):
        dataset: DatasetReader = rasterio.open(filename, driver="GTiff")
        self.band_arr = dataset.read(band_id)

        img = gdal.Open(filename)
        gt = img.GetGeoTransform()
        width = img.RasterXSize
        height = img.RasterYSize

        self.img = img
        self.gt = gt
        self.git = gdal.InvGeoTransform(gt)[1]
        self.left = dataset.bounds.left
        self.right = dataset.bounds.right
        self.top = dataset.bounds.top
        self.bottom = dataset.bounds.bottom
        self.height = self.top - self.bottom
        self.width = self.right - self.left

    def get_height(self, lat, lng) -> float:
        x = (self.width) - (lng - self.bottom) / self.height
        y = (lat - self.left) / self.width

        x = int(x * self.img.RasterYSize)
        y = int(y * self.img.RasterXSize)

        if x >= self.img.RasterYSize:
            x = self.img.RasterYSize - 1
        if y >= self.img.RasterXSize:
            y = self.img.RasterXSize - 1

        return self.band_arr[x, y]
