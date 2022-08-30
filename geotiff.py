import math
import os
from typing import Optional

import gdal
import numpy as np
import rasterio
from shapely.geometry import Polygon, Point
from stl import mesh


class GeoTIFFS:

    def __init__(self):
        self.geotiffs = {}

    def get(self, lat, lng) -> Optional["GeoTIFF"]:
        lat = math.floor(lat)
        lng = math.floor(lng)
        ew = "w" if lat < 0 else "e"
        ns = "n" if lng > 0 else "s"

        filename = f"./data/{ns}{lng}_{ew}{int(math.fabs(lat))}_1arc_v3.tif"
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
        dataset = rasterio.open(filename, driver='GTiff')
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
        return self.band_arr[x, y]


geoTIFFS = GeoTIFFS()


def get_triangles(lon, lat, size=0.01, z_scale=1.0, digits=7):
    lon = round(lon, digits)
    lat = round(lat, digits)

    def _get_pixel(x, y):
        return max(geoTIFFS.get_height(x, y), 0)

    av = _get_pixel(lon, lat)
    bv = _get_pixel(lon+size, lat)
    cv = _get_pixel(lon, lat+size)
    dv = _get_pixel(lon+size, lat+size)

    # a-c   a-c     c
    # |/| = |/  +  /|
    # b-d   b     b-d
    a = (lon, lat, round(av*z_scale,digits))
    b = (lon+size, lat, round(bv*z_scale,digits))
    c = (lon, lat+size, round(cv*z_scale,digits))
    d = (lon+size, lat+size, round(dv*z_scale,digits))

    return (a, b, c), (d, c, b)


def get_bounding_box(region):
    lons_vect = [lon for lon, lat in region]
    lats_vect = [lat for lon, lat in region]
    lons_lats_vect = np.column_stack((lons_vect, lats_vect))  # Reshape coordinates
    polygon = Polygon(lons_lats_vect)  # create polygon
    bounding_box = polygon.bounds  # get bounding box
    return bounding_box


# Write STL file
def build_stl(region, filename, resolution=0.0005, z_scale=0.00005, digits=8, fit_to_region=False):
    lons_vect = [lon for lon, lat in region]
    lats_vect = [lat for lon, lat in region]
    lons_lats_vect = np.column_stack((lons_vect, lats_vect))  # Reshape coordinates
    polygon = Polygon(lons_lats_vect)  # create polygon

    # get the triangles
    bounding_box = get_bounding_box(region)
    lons = np.arange(bounding_box[0], bounding_box[2], resolution)
    lats = np.arange(bounding_box[1], bounding_box[3], resolution)
    triangles = []
    num_triangles = len(lons)*len(lats)
    i = 0
    for lat in lats:
        for lon in lons:
            if fit_to_region and not polygon.contains(Point(lon, lat)):
                continue

            triangles.extend(get_triangles(lat, lon, resolution, z_scale, digits))

            if i % 50000 == 0:
                print(f"{round(i*100/num_triangles, 2)}%")
            i += 1
    print(f"{round(i * 100 / num_triangles, 2)}%")

    # build the mesh
    num_triangles = len(triangles)
    data = np.zeros(num_triangles, dtype=mesh.Mesh.dtype)
    i = 0
    for triangle in triangles:
        data["vectors"][i] = np.array(triangle)
        i += 1

    # write the mesh
    m = mesh.Mesh(data)
    m.save(filename)
    print("STL file saved to", filename)