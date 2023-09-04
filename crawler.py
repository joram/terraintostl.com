#!/usr/bin/env python3

import webbrowser
import time
import os

URL = "https://earthexplorer.usgs.gov/download/5e83a3efe0103743/{filename}/"
chrome_path = "/usr/bin/google-chrome %s"
browser = webbrowser.get(chrome_path)


def get_filename(entity_id: str) -> str:
    entity_id = entity_id.replace("SRTM1", "").replace("V3", "").lower()
    filename = f"{entity_id[0:3]}_{entity_id[3:7]}_1arc_v3.tif"
    return filename


def all_filenames():
    content = open("srtm_v3_63177cde8169203e.txt").read()
    lines = content.split("\n")
    i = 0
    total = len(lines)
    for line in lines:
        parts = line.split(",")
        if len(parts) < 2:
            continue
        entity_id = parts[1]
        filename = get_filename(entity_id)
        if not filename.endswith(".tif"):
            continue
        url = URL.format(filename=entity_id)
        i += 1
        yield url, filename, i, total


def missing_filenames():
    for url, filename, i, total in all_filenames():
        exists = False
        for filepath in [
            f"/home/john/Downloads/{filename}",
            f"./data/raw/{filename}",
            f"./data/clean/{filename}",
        ]:
            if os.path.exists(filepath):
                exists = True
        if exists:
            continue
        yield url, filename, i, total


def move_tifs_from_downloads_to_raw():
    for filename in os.listdir("/home/john/Downloads"):
        if filename.endswith(".tif"):
            os.system(f"mv /home/john/Downloads/{filename} ./data/raw")


def process_all_raw_tifs():
    for filename in os.listdir("./data/raw"):
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


if __name__ == "__main__":
    for url, filename, i, total in missing_filenames():
        print(f"getting {i}/{total}\t {url}")
        browser.open(url)
        time.sleep(5)
        move_tifs_from_downloads_to_raw()
        process_all_raw_tifs()
