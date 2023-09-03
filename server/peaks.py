#!/usr/bin/env python3
import json
import os
import subprocess

from stl_generator.stl_util import build_stl_from_circle

LOADED_PEAKS = False


def _clone_peaks_repo():
    """Clone the peaks repo if it does not exist, otherwise pull the latest changes."""
    pwd = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(pwd, "../data/peaks")

    if os.path.isdir(data_dir):
        print("Pulling latest changes from peaks repo...")
        subprocess.call(["git", "pull"], cwd=data_dir)
        return

    print("Cloning peaks repo...")
    subprocess.call(["git", "clone", "git@github.com:joram/peaks.git", data_dir])


PEAKS = {}


def _cache_all_peak_filenames():
    """Cache all peak filenames."""
    global PEAKS
    pwd = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(pwd, "../data/peaks")
    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            filepath = os.path.join(subdir, file)
            if filepath.endswith(".geojson"):
                PEAKS[file[:-8].replace("-", " ")] = filepath


def find_peak(name: str):
    """Find a peak by its name."""
    global LOADED_PEAKS
    if not LOADED_PEAKS:
        _clone_peaks_repo()
        _cache_all_peak_filenames()
        LOADED_PEAKS = True

    name = name.lower()
    if name in PEAKS:
        filepath = PEAKS[name]
        with open(filepath, "r") as f:
            return json.loads(f.read())
    return None


def get_coordinates(name: str):
    """Get the coordinates of a peak by its name."""
    peak = find_peak(name)
    if peak:
        return peak["geometry"]["coordinates"]
    return None


if __name__ == "__main__":
    lng, lat = get_coordinates("Golden Hinde")
    print(lat, lng)
    build_stl_from_circle(
        center=(lat, lng),
        radius=0.1,
        z_scale=1,
        filename="golden_hinde.stl",
    )
