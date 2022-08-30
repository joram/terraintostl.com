import logging
import argparse
import math
import os
from collections import deque
from struct import pack, unpack
from typing import Optional

import numpy as np
import pymesh
import rasterio

from osgeo import gdal
from osgeo.gdal import Band
from shapely.geometry import Polygon
from stl import mesh

logger = logging.getLogger(__name__)
gdal.UseExceptions()
gdal.TermProgress = gdal.TermProgress_nocb


def NormalVector(t):
    (ax, ay, az) = t[0]
    (bx, by, bz) = t[1]
    (cx, cy, cz) = t[2]

    # first edge
    e1x = np.float32(ax) - np.float32(bx)
    e1y = np.float32(ay) - np.float32(by)
    e1z = np.float32(az) - np.float32(bz)

    # second edge
    e2x = np.float32(bx) - np.float32(cx)
    e2y = np.float32(by) - np.float32(cy)
    e2z = np.float32(bz) - np.float32(cz)

    # cross product
    cpx = np.float32(e1y * e2z) - np.float32(e1z * e2y)
    cpy = np.float32(e1z * e2x) - np.float32(e1x * e2z)
    cpz = np.float32(e1x * e2y) - np.float32(e1y * e2x)

    # return cross product vector normalized to unit length
    mag = np.sqrt(np.power(cpx, 2) + np.power(cpy, 2) + np.power(cpz, 2))
    return (cpx / mag, cpy / mag, cpz / mag)


class STLWriter:

    # path: output binary stl file path
    # facet_count: predicted number of facets
    def __init__(self, path, facet_count=0):
        self.f = open(path, 'wb')

        # track number of facets actually written
        self.written = 0

        # write binary stl header with predicted facet count
        self.f.write(b'\0' * 80)
        # (facet count is little endian 4 byte unsigned int)
        self.f.write(pack('<I', facet_count))

    # t: ((ax, ay, az), (bx, by, bz), (cx, cy, cz))
    def add_facet(self, t):
        # facet normals and vectors are little endian 4 byte float triplets
        # strictly speaking, we don't need to compute NormalVector,
        # as other tools could be used to update the output mesh.
        self.f.write(pack('<3f', *NormalVector(t)))
        for vertex in t:
            self.f.write(pack('<3f', *vertex))
        # facet records conclude with two null bytes (unused "attributes")
        self.f.write(b'\0\0')
        self.written += 1

    def done(self):
        # update final facet count in header before closing file
        self.f.seek(80)
        self.f.write(pack('<I', self.written))
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.done()


def fail(msg):
    logger.info(msg)
    exit(1)


def log(msg):
    logger.info(msg)


# ap = argparse.ArgumentParser(description='Convert a GDAL raster (like a GeoTIFF heightmap) to an STL terrain surface.')
# ap.add_argument('-x', action='store', default=0.0, type=float, help='Fit output x to extent (mm)')
# ap.add_argument('-y', action='store', default=0.0, type=float, help='Fit output y to extent (mm)')
# optg_z = ap.add_mutually_exclusive_group()
# optg_z.add_argument('-z', action='store', default=None, type=float,
#                     help='Z scale expressed as a vertical scale factor (1)')
# optg_z.add_argument('-s', action='store', default=None, type=float,
#                     help='Z scale expressed as a ratio of vertical units per horizontal unit (1)')
# ap.add_argument('-b', '--base', action='store', default=0.0, type=float, help='Base height (0)')
# ap.add_argument('-c', '--clip', action='store_true', default=False, help='Clip z to minimum elevation')
# ap.add_argument('-v', '--verbose', action='store_true', default=False, help='Print log messages')
# ap.add_argument('--band', action='store', default=1, type=int, help='Raster data band (1)')
# ap.add_argument('-m', '--minimum', action='store', default=None, type=float,
#                 help='Omit vertices below minimum elevation')
# ap.add_argument('-M', '--maximum', action='store', default=None, type=float,
#                 help='Omit vertices above maximum elevation')
# optg_region = ap.add_mutually_exclusive_group()
# optg_region.add_argument('-w', '--window', action='store', default=None, type=float, nargs=4,
#                          help='Opposing corner coordinates in geographic CRS')
# optg_region.add_argument('-p', '--pixels', action='store', default=None, type=float, nargs=4,
#                          help='Opposing corner coordinates in pixel coordinates')
# ap.add_argument('RASTER', help='Input heightmap image')
# ap.add_argument('STL', help='Output STL path')
# args = ap.parse_args()

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
            self.geotiffs[filename] = GeoTIFF(filename, lat, lng)
        return self.geotiffs[filename]

    def get_height(self, lat, lng) -> float:
        geotiff = self.get(lat, lng)
        if geotiff is None:
            return 0

        return geotiff.get_height(lat, lng)


class GeoTIFF:

    def __init__(self, filename: str, lat, lng, band_id=1):
        raster = rasterio.open(filename)
        self.band_arr = raster.read(band_id)
        self.lat = lat
        self.lng = lng

    def get_height(self, lat, lng) -> float:
        x = int((lng - self.lng) * 1800)
        y = int((lat - self.lat) * 1800)
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
def build_stl(region, filename, resolution=0.0005, z_scale=0.00005, digits=8):

    # get the triangles
    bounding_box = get_bounding_box(region)
    lons = np.arange(bounding_box[0], bounding_box[2], resolution)
    lats = np.arange(bounding_box[1], bounding_box[3], resolution)
    triangles = []
    for lat in lats:
        for lon in lons:
            ts = get_triangles(lat, lon, resolution, z_scale, digits)
            triangles.extend(ts)

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