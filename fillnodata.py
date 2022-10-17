#!/usr/bin/env python3
import os
import time

filenames = os.listdir("./data/raw")
filenames.sort()
for filename in filenames:
    if filename.endswith(".tif"):
        raw_filepath = f"./data/raw/{filename}"
        clean_filepath = f"./data/clean/{filename}"
        if os.path.exists(clean_filepath):
            print(f"Skipping {filename} already exists: {clean_filepath}")
            os.system(f"rm {raw_filepath}")
            continue
        if "(" in filename:
            print(f"Skipping {filename} duplicate")
            os.system(f'rm "{raw_filepath}"')
            continue

        print(f"Cleaning {raw_filepath} to {clean_filepath}")
        cmd = f'gdal_fillnodata.py "{raw_filepath}" "{clean_filepath}"'
        os.system(cmd)
        os.system(f"rm {raw_filepath}")
