#!/usr/bin/env python
import dataclasses
import threading
import time
from typing import List, Tuple

import uvicorn as uvicorn
from fastapi import FastAPI


app = FastAPI()


@dataclasses.dataclass
class BuildSTLRequest:
    filename: str = "example.stl"
    region: List[Tuple[float, float]] = dataclasses.field(default_factory=[
        [50.7573, -129.3420],
        [48.4292, -124.8486],
        [48.2393, -123.7500],
        [48.4073, -122.9370],
        [49.1026, -123.4753],
        [50.2332, -125.1453],
        [50.8129, -127.1008],
        [51.1173, -128.5730],
        [51.0483, -129.1113],
    ])


@dataclasses.dataclass
class BuildSTLResponse:
    pass


running = True
build_requests = []


def build_stls():
    global build_requests
    global running
    while running:
        if len(build_requests) > 0:
            request = build_requests.pop()
            build_stl(
                region=request.region,
                filename=request.filename,
                resolution=0.002,
                z_scale=0.00002,
                fit_to_region=True,
            )

        if len(build_requests) == 0:
            time.sleep(1)


t = threading.Thread(target=build_stls)
t.start()


@app.post("/stl")
def build_stl(request: BuildSTLRequest) -> BuildSTLResponse:
    build_requests.append(request)
    return BuildSTLResponse()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)