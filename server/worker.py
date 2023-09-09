import base64
import datetime
import json
import os
from typing import List

from payloads import BuildSTLRequest, BoundsEnum, RequestType
from peaks import get_coordinates
from sessions import get_session
from stl_generator.stl_util import build_stl_from_polygon

in_progress_requests = []


def get_api_url() -> str:
    return os.environ.get("API_URL", "https://terraintostlapi.oram.ca")


def get_progress() -> List[dict]:
    global in_progress_requests
    return [
        {
            "name": r.name or "",
            "progress": r.percentage_processed,
        }
        for r in in_progress_requests
    ]


def _build_polygon(request: BuildSTLRequest):
    region = request.region
    region = base64.b64decode(region)
    region = json.loads(region)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    now = datetime.datetime.now()
    email = get_session(request.session_key)["email"]
    filename = f"{dir_path}/../stls/{email}/{now.year}-{now.month}-{now.day}T{now.hour}:{now.minute}:{now.second}-{request.name}.stl"
    print(
        f"building STL with name: {request.name} region: {region},"
        f" resolution: {request.resolution}, z_scale: {request.z_scale}, bounds: {request.bounds}"
    )

    def update_progress(progress):
        request.percentage_processed = progress

    request.percentage_processed = 0
    build_stl_from_polygon(
        polygon=region,
        filename=filename,
        resolution=0.002 * request.resolution,
        z_scale=0.00002 * request.z_scale,
        fit_to_region=request.bounds == BoundsEnum.polygon,
        drop_ocean_by=request.drop_ocean_by,
        callback=update_progress,
    )


def _build_peak(request: BuildSTLRequest):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    now = datetime.datetime.now()
    email = get_session(request.session_key)["email"]
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")
    filename = f"{dir_path}/../stls/{email}/{timestamp}-{request.name}.stl"
    lng, lat = get_coordinates(request.name)

    global in_progress_requests
    in_progress_requests.append(request)

    def update_progress(progress):
        global in_progress_requests
        for r in in_progress_requests:
            if r.name == request.name:
                request.percentage_processed = progress
                break
        if progress == 1.0:
            in_progress_requests = [
                r for r in in_progress_requests if r.name != request.name
            ]

    def calculate_bounding_box(center_lat, center_lng, square_size_meters=10000):
        import pyproj
        import numpy as np

        # Create an azimuthal equidistant projection centered on the given point
        ae_proj = pyproj.Proj(proj="aeqd", lat_0=center_lat, lon_0=center_lng)

        # Calculate the coordinates of the square's corners
        square_coords = []
        for angle in np.linspace(0, 2 * np.pi, 5):
            x_offset = square_size_meters * np.cos(angle)
            y_offset = square_size_meters * np.sin(angle)
            lng, lat = ae_proj(x_offset, y_offset, inverse=True)
            square_coords.append((lat, lng))
        return square_coords

    request.percentage_processed = 0
    print(f"Peak of {request.name} is at ({lat}, {lng})")
    build_stl_from_polygon(
        polygon=calculate_bounding_box(lat, lng),
        resolution=0.0005 * request.resolution,
        z_scale=0.000015 * request.z_scale,
        digits=10,
        filename=filename,
        callback=update_progress,
    )


def build_stl(request: BuildSTLRequest):
    print("building STL")
    request.z_scale = request.z_scale or 1
    request.resolution = request.resolution or 1
    if request.request_type == RequestType.polygon:
        _build_polygon(request)
    elif request.request_type == RequestType.peak:
        _build_peak(request)
    else:
        raise Exception(f"unknown request type {request.request_type}")

    print(f"done building STL {request.name}")
