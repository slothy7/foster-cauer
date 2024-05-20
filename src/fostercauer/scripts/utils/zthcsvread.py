"""Read Zth vs. Time CSV"""

import csv


def read_zth_csv(csv_path):
    """read csv and return time and zth vectors"""
    time = []
    zth = []
    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time.append(float(row[0]))
            zth.append(float(row[1]))
    return time, zth
