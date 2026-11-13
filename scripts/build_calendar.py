"""Aggregate verified FIRMS extracts to daily counts and occupied grid cells."""

import argparse
import csv
import hashlib
import io
import json
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path

from firms import DAY, atomic_write, read_csv


def grid_cell(lat, lon):
    latitude, longitude = Decimal(lat), Decimal(lon)
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        raise ValueError("Detection coordinates outside WGS84 bounds")
    return tuple(
        int((value * 20).to_integral_value(rounding=ROUND_FLOOR))
        for value in (latitude, longitude)
    )


def aggregate(directory):
    days = {}
    for manifest in sorted(directory.rglob("*.json")):
        meta = json.loads(manifest.read_text(encoding="utf-8"))
        payload = manifest.with_suffix(".csv").read_bytes()
        if hashlib.sha256(payload).hexdigest() != meta["sha256"]:
            raise ValueError(f"Checksum mismatch for {manifest}")
        first, last = map(date.fromisoformat, (meta["start"], meta["end"]))
        if first > last:
            raise ValueError(f"Invalid date window in {manifest}")
        counts = defaultdict(int)
        cells = defaultdict(set)
        for row in read_csv(payload):
            day = date.fromisoformat(row["acq_date"])
            if not first <= day <= last:
                raise ValueError(f"Detection outside its source window in {manifest}")
            counts[day] += 1
            cells[day].add(grid_cell(row["latitude"], row["longitude"]))
        if sum(counts.values()) != meta["rows"]:
            raise ValueError(f"Unexpected row count in {manifest}")
        day = first
        while day <= last:
            key = (day, meta["bbox"], meta["source"])
            if key in days:
                raise ValueError(f"Overlapping extracts for {key}")
            days[key] = (counts[day], len(cells[day]))
            day += DAY
    if not days:
        raise ValueError(f"No FIRMS manifests under {directory}")
    return days


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer)
        writer.writerow(["date_utc", "bbox", "source", "raw_detections", "occupied_cells_0_05deg"])
        for key, counts in sorted(aggregate(args.input).items()):
            writer.writerow((*key, *counts))
        atomic_write(args.output, buffer.getvalue().encode("utf-8"))
    except (OSError, ValueError, KeyError, ArithmeticError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
