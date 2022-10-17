import base64
import datetime
import json
import os
import threading
import time
from typing import Optional

from payloads import BuildSTLRequest, BoundsEnum
from stl_generator.stl_util import build_stl

running = True
build_requests = []
in_progress_request = None
in_progress_percentage = 0


def get_progress() -> Optional[dict]:
    global in_progress_request
    global in_progress_percentage
    if in_progress_request is not None:
        return {
            "name": in_progress_request.name,
            "progress": in_progress_percentage,
        }
    return None


def update_progress(progress: float):
    global in_progress_request
    global in_progress_percentage
    in_progress_percentage = progress
    print(f"progress {in_progress_percentage*100}%")
    if progress == 1:
        in_progress_request = None
        in_progress_percentage = 0


def build_stls_worker():
    global in_progress_request
    global build_requests
    global running
    while running:
        if len(build_requests) > 0:
            request = build_requests.pop()
            in_progress_request = request
            region = request.region
            region = base64.b64decode(region)
            region = json.loads(region)
            dir_path = os.path.dirname(os.path.realpath(__file__))
            now = datetime.datetime.now()
            filename = f"{dir_path}/../stls/{now.year}-{now.month}-{now.day}T{now.hour}:{now.minute}:{now.second}-{request.name}.stl"
            print(f"building STL with name: {request.name} region: {region},"
                  f" resolution: {request.resolution}, z_scale: {request.z_scale}, bounds: {request.bounds}")
            build_stl(
                region=region,
                filename=filename,
                resolution=0.002*request.resolution,
                z_scale=0.00002*request.z_scale,
                fit_to_region=request.bounds == BoundsEnum.polygon,
                drop_ocean_by=request.drop_ocean_by,
                callback=update_progress,
            )

        if len(build_requests) == 0:
            time.sleep(1)


t = threading.Thread(target=build_stls_worker, daemon=True)
t.start()


def add_build_request(request: BuildSTLRequest):
    global build_requests
    build_requests.append(request)
