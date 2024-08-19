#!/usr/bin/env python3
import json
import os
import sqlite3
import subprocess

INDEX = None


class PeaksSearchEngine:
    def __init__(self):
        self.db_filepath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "./data/peaks.sqlite3")
        )
        self.peaks_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "./data/peaks")
        )
        if not os.path.exists(self.peaks_dir):
            self._clone_peaks_repo()

        if not os.path.exists(self.db_filepath):
            self._create_index()
            self._create_index()
            self._populate_table()

    def _clone_peaks_repo(self):
        """Clone the peaks repo if it does not exist, otherwise pull the latest changes."""
        print("looking at peaks dir", self.peaks_dir)

        if os.path.isdir(self.peaks_dir):
            print("Pulling latest changes from peaks repo...")
            output = subprocess.check_output(
                ["git", "pull"], cwd=self.peaks_dir, universal_newlines=True
            )
            print(output)
            return

        print("Cloning peaks repo...")
        output = subprocess.check_output(
            ["git", "clone", "git@github.com:joram/peaks.git", self.peaks_dir],
            universal_newlines=True,
        )
        print(output)

    def _create_index(self):
        conn = sqlite3.connect(self.db_filepath)
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS documents
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)"""
        )
        conn.commit()
        conn.close()

    def _populate_table(self):
        conn = sqlite3.connect(self.db_filepath)
        cursor = conn.cursor()
        for results in os.walk(self.peaks_dir):
            for file in results[2]:
                filepath = os.path.join(results[0], file)
                filepath = os.path.abspath(filepath)
                if not filepath.endswith(".geojson"):
                    continue
                if filepath.endswith("index.geojson"):
                    continue

                with open(filepath, "r") as f:
                    data = f.read()
                    cursor.execute(
                        "INSERT INTO documents (title, content) VALUES (?, ?)",
                        (filepath, data),
                    )
        conn.commit()
        conn.close()

    def search(self, keyword):
        conn = sqlite3.connect(self.db_filepath)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, content FROM documents WHERE title LIKE ? OR content LIKE ?",
            ("%" + keyword + "%", "%" + keyword + "%"),
        )
        results = cursor.fetchall()
        data = []
        for result in results:
            [id, title, content] = result
            content = json.loads(content)
            coords = content["geometry"]["coordinates"]
            data.append(
                {
                    "id": id,
                    "filepath": title,
                    "content": content,
                    "coords": coords,
                    "name": content["properties"]["name"],
                }
            )
        conn.close()
        return data


def get_peak_index():
    global INDEX
    if INDEX is None:
        print("Building peak index...")
        INDEX = PeaksSearchEngine()
        print("Done building peak index.")
    return INDEX


get_peak_index()
if __name__ == "__main__":
    index = get_peak_index()
    for search_text in ["Everest", "peak", "triple", "hinde"]:
        results = index.search(search_text)
        for result in results:
            print(result["filepath"], result["coords"])
