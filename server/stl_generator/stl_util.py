#!/usr/bin/env python
import pymesh
import math
from typing import Optional

import numpy
import numpy as np
from numpy.linalg import norm
from shapely.geometry import Polygon, Point

from .geotiff import GeoTIFFS
from stl import mesh

geoTIFFS = GeoTIFFS()


def get_triangles(lon, lat, size=0.01, z_scale=1.0, digits=7, drop_ocean_by=0):
    lon = round(lon, digits)
    lat = round(lat, digits)

    def _get_pixel(x, y) -> Optional[float]:
        v = geoTIFFS.get_height(x, y)

        if v == -32767:
            return None

        if v <= 0:
            return -drop_ocean_by

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
    # https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates
    return longitude * math.cos(numpy.deg2rad(reference_latitude)), latitude, z
    # return longitude, latitude, z

# Write STL file
def build_stl(region, filename, resolution=0.0005, z_scale=0.00005, digits=8, fit_to_region=False, drop_ocean_by=0, callback=None):
    lons_vect = [lon for lon, lat in region]
    lats_vect = [lat for lon, lat in region]
    lons_lats_vect = np.column_stack((lons_vect, lats_vect))  # Reshape coordinates
    polygon = Polygon(lons_lats_vect)  # create polygon
    reference_longitude = polygon.centroid.x

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
            for triangle in get_triangles(lat, lon, resolution, z_scale, digits, drop_ocean_by):
                new_triangle = [mapCoordinates(lng,lat, z, reference_longitude) for lat,lng,z in triangle]
                triangles.append(new_triangle)

            if i % 2000 == 0:
                if callback:
                    callback(float(i)/num_triangles)
            i += 1
    if callback:
        callback(1.0)

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


def reduce_size(filename="../../stls/2022-9-8T11:38:59-vancouver island.stl", tolerance=0.0001):
    mesh = fix_mesh(pymesh.load_mesh(filename))
    pymesh.save_mesh(f"{filename}.reduced.stl", mesh)

    mesh = fix_mesh(pymesh.load_mesh(f"{filename}.reduced.stl"))
    pymesh.save_mesh(f"{filename}.reduced.reduced.stl", mesh)


def fix_mesh(mesh, detail="extrahigh", target_length=None):
    bbox_min, bbox_max = mesh.bbox
    diag_len = norm(bbox_max - bbox_min)
    target_len = {
        "extrahigh": diag_len * 5e-4,
        "normal": diag_len * 5e-3,
        "high": diag_len * 2.5e-3,
        "low": diag_len * 1e-2,
    }.get(detail, diag_len * 0.0001)
    if target_length is not None:
        target_len = target_length
    print(f"Target resolution: {target_len} mm")

    count = 0
    mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100)
    mesh, __ = pymesh.split_long_edges(mesh, target_len)
    num_vertices = mesh.num_vertices
    print("#v: {}".format(num_vertices))
    while True:
        mesh, __ = pymesh.collapse_short_edges(mesh, 1e-6)
        mesh, __ = pymesh.collapse_short_edges(mesh, target_len, preserve_feature=True)
        mesh, __ = pymesh.remove_obtuse_triangles(mesh, 150.0, 100)
        if mesh.num_vertices == num_vertices:
            break

        num_vertices = mesh.num_vertices
        print("#v: {}".format(num_vertices))
        count += 1
        if count > 10: break

    mesh = pymesh.resolve_self_intersection(mesh)
    mesh, __ = pymesh.remove_duplicated_faces(mesh)
    mesh = pymesh.compute_outer_hull(mesh)
    mesh, __ = pymesh.remove_duplicated_faces(mesh)
    mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5)
    mesh, __ = pymesh.remove_isolated_vertices(mesh)



    return mesh


if __name__ == "__main__":
    reduce_size()
