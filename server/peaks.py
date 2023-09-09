#!/usr/bin/env python3
import json
import os
import subprocess

LOADED_PEAKS = False
PEAKS = {}
pwd = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(pwd, "../data/peaks")
PEAKS_DIR = os.path.abspath(data_dir)


def _clone_peaks_repo():
    """Clone the peaks repo if it does not exist, otherwise pull the latest changes."""
    print("looking at peaks dir", PEAKS_DIR)

    if os.path.isdir(PEAKS_DIR):
        print("Pulling latest changes from peaks repo...")
        subprocess.call(["git", "pull"], cwd=PEAKS_DIR)
        return

    print("Cloning peaks repo...")
    subprocess.call(["git", "clone", "git@github.com:joram/peaks.git", PEAKS_DIR])


def _cache_all_peak_filenames():
    """Cache all peak filenames."""
    global PEAKS
    for subdir, dirs, files in os.walk(PEAKS_DIR):
        for file in files:
            filepath = os.path.join(subdir, file)
            if filepath.endswith(".geojson"):
                PEAKS[file[:-8].replace("-", " ")] = filepath


def find_peak(name: str):
    """Find a peak by its name."""
    global LOADED_PEAKS
    if not LOADED_PEAKS:
        try:
            _clone_peaks_repo()
            _cache_all_peak_filenames()
        except Exception as e:
            print(e)
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
