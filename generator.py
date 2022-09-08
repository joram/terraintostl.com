#!/usr/bin/env python
import webbrowser
import time
import os
URL = "https://earthexplorer.usgs.gov/download/5e83a3efe0103743/{filename}/"
chrome_path = '/usr/bin/google-chrome %s'
browser = webbrowser.get(chrome_path)


def open_url(url):
    browser.open(url)


def get_filename(entity_id: str) -> str:
    entity_id = entity_id.replace("SRTM1", "").replace("V3", "").lower()
    filename = f"{entity_id[0:3]}_{entity_id[3:7]}_1arc_v3.tif"
    return filename


if __name__ == "__main__":
    content = open("srtm_v3_63177cde8169203e.txt").read()
    lines = content.split("\n")
    i = 0
    for line in lines:
        parts = line.split(",")
        entity_id = parts[1]
        filename = get_filename(entity_id)
        url = URL.format(filename=entity_id)
        print(f"{i}/{len(lines)}: {url} {filename}")
        i += 1

        exists = False
        for filepath in [f"/home/john/Downloads/{filename}", f"./data/raw/{filename}"]:
            if os.path.exists(filepath):
                exists = True
        if exists:
            continue

        open_url(url)
        time.sleep(5)
