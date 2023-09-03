#!/usr/bin/env python3

import base64
import datetime
import json
import os

from stl_generator.stl_util import build_stl_from_polygon

polygon = "W1s1MC45NjQxNDk0Mjk4MDc3MiwtMTI5LjQ2NDA2OTkwMzc3OTAzXSxbNDkuODUwOTI2MzIyNzAyMDEsLTEyNy43ODg2NTQ4NjQ3MTY1NV0sWzUwLjY1ODcwMzYxNjY4NTk4LC0xMjUuODAwMTI5NDc0MDkxNTVdLFs1MS4yMTYwMTY0MTYwMTU5OCwtMTI3LjE3ODkxMzY1Mzc3OTA1XV0="
polygon = base64.b64decode(polygon)
polygon = json.loads(polygon)
print(polygon)

dir_path = os.path.dirname(os.path.realpath(__file__))
now = datetime.datetime.now()
filename = f"{dir_path}/../stls/test.stl"
build_stl_from_polygon(
    polygon=polygon,
    filename=filename,
    resolution=0.002,
    z_scale=0.00002 * 1,
    fit_to_region=True,
    drop_ocean_by=10,
)
print("done")
