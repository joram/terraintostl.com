import base64
import datetime
import json
import os
import threading
import time

from payloads import BuildSTLRequest
from stl_generator.stl_util import build_stl

running = True
build_requests = []


def build_stls():
    global build_requests
    global running
    while running:
        if len(build_requests) > 0:
            request = build_requests.pop()
            region = request.region
            region = base64.b64decode(region)
            region = json.loads(region)
            dir_path = os.path.dirname(os.path.realpath(__file__))
            now = datetime.datetime.now()
            filename = f"{dir_path}/../stls/{now.year}-{now.month}-{now.day}T{now.hour}:{now.minute}:{now.second}-{request.name}.stl"
            print(f"building STL with name: {request.name} region: {region},"
                  f" resolution: {request.resolution}, z_scale: {request.z_scale}")
            build_stl(
                region=region,
                filename=filename,
                resolution=0.002*request.resolution,
                z_scale=0.00002*request.z_scale,
                fit_to_region=True,
            )

        if len(build_requests) == 0:
            time.sleep(1)


t = threading.Thread(target=build_stls, daemon=True)
t.start()


def add_build_request(request: BuildSTLRequest):
    global build_requests
    build_requests.append(request)
