#!/usr/bin/env python3

import webbrowser
import time
import os
URL = "https://earthexplorer.usgs.gov/download/5e83a3efe0103743/{filename}/"
chrome_path = '/usr/bin/google-chrome %s'
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
        url = URL.format(filename=entity_id)
        i += 1
        yield url, filename, i, total


def missing_filenames():
    for url, filename, i, total in all_filenames():
        exists = False
        for filepath in [f"/home/john/Downloads/{filename}", f"./data/raw/{filename}"]:
            if os.path.exists(filepath):
                exists = True
        if exists:
            continue
        yield url, filename, i, total


if __name__ == "__main__":
    for url, filename, i, total in missing_filenames():
        print(f"getting {i}/{total}\t {url}")
        browser.open(url)
        time.sleep(5)
