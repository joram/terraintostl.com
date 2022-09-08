import math
from typing import Optional

import numpy
import numpy as np
from shapely.geometry import Polygon, Point

from .geotiff import GeoTIFFS
from stl import mesh

geoTIFFS = GeoTIFFS()


def get_triangles(lon, lat, size=0.01, z_scale=1.0, digits=7):
    lon = round(lon, digits)
    lat = round(lat, digits)

    def _get_pixel(x, y) -> Optional[float]:
        v = geoTIFFS.get_height(x, y)
        if v == -32767:
            return None
        return v

    av = _get_pixel(lon, lat)
    bv = _get_pixel(lon+size, lat)
    cv = _get_pixel(lon, lat+size)
    dv = _get_pixel(lon+size, lat+size)
    if av is None or bv is None or cv is None or dv is None:
        return []

    # a-c   a-c     c
    # |/| = |/  +  /|
    # b-d   b     b-d
    a = (lon, lat, round(av*z_scale,digits))
    b = (lon+size, lat, round(bv*z_scale,digits))
    c = (lon, lat+size, round(cv*z_scale,digits))
    d = (lon+size, lat+size, round(dv*z_scale,digits))

    return [(a, b, c), (d, c, b)]


def get_bounding_box(region):
    lons_vect = [lon for lon, lat in region]
    lats_vect = [lat for lon, lat in region]
    lons_lats_vect = np.column_stack((lons_vect, lats_vect))  # Reshape coordinates
    polygon = Polygon(lons_lats_vect)  # create polygon
    bounding_box = polygon.bounds  # get bounding box
    return bounding_box

def mapCoordinates(latitude, longitude, z, reference_latitude):
#    return new Vector2(longitude, Mathf.Rad2Deg * Mathf.Tan(latitude *  Mathf.Deg2Rad));
#     return latitude, numpy.rad2deg(math.tan(numpy.deg2rad(longitude))), z
    #return latitude, longitude, z
    # return latitude, longitude * numpy.rad2deg(math.cos(numpy.deg2rad(latitude))), z
    return longitude * math.cos(numpy.deg2rad(reference_latitude)), latitude, z


# Write STL file
def build_stl(region, filename, resolution=0.0005, z_scale=0.00005, digits=8, fit_to_region=False):
    lons_vect = [lon for lon, lat in region]
    lats_vect = [lat for lon, lat in region]
    lons_lats_vect = np.column_stack((lons_vect, lats_vect))  # Reshape coordinates
    polygon = Polygon(lons_lats_vect)  # create polygon
    reference_longitude = numpy.mean(lons_vect)

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
            for triangle in get_triangles(lat, lon, resolution, z_scale, digits):
                new_triangle = [mapCoordinates(lng,lat, z, reference_longitude) for lat,lng,z in triangle]
                triangles.append(new_triangle)

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