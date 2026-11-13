"""Plan and cache bounded NASA FIRMS Area API requests."""

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = "https://firms.modaps.eosdis.nasa.gov/api"
PRODUCTS = {
    f"{sensor}_{level}"
    for sensor in ("MODIS", "VIIRS_SNPP", "VIIRS_NOAA20", "VIIRS_NOAA21")
    for level in ("SP", "NRT")
}
FIELDS = {"latitude", "longitude", "acq_date", "acq_time", "satellite"}
DAY = timedelta(days=1)


def windows(start, end):
    if end < start:
        raise ValueError("End date must be on or after start date")
    while start <= end:
        stop = min(end, start + 4 * DAY)
        yield start, stop
        start = stop + DAY


def bounds(value):
    west, south, east, north = map(float, value.split(","))
    if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
        raise ValueError("Use west,south,east,north without crossing the antimeridian")
    return ",".join(str(number) for number in (west, south, east, north))


def read_csv(payload):
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8-sig"), newline=""))
    if not FIELDS.issubset(reader.fieldnames or []):
        raise ValueError("FIRMS response is missing detection CSV headers")
    return reader


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            handle.write(payload)
            handle.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def download(path):
    for attempt in range(3):
        try:
            request = Request(f"{ROOT}/{path}", headers={"User-Agent": "EmberAtlas/0.1"})
            with urlopen(request, timeout=45) as response:
                return response.read()
        except HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt == 2:
                raise ValueError(f"FIRMS returned HTTP {error.code}") from None
            retry_after = error.headers.get("Retry-After", "")
            delay = min(60, int(retry_after)) if retry_after.isdecimal() else 2 ** attempt
        except (URLError, TimeoutError):
            if attempt == 2:
                raise ValueError("FIRMS connection failed") from None
            delay = 2 ** attempt
        time.sleep(delay)


def fetch(key, source, bbox, start, end, output):
    directory = output / bbox / source
    target = directory / f"{start}_{end}.csv"
    manifest = target.with_suffix(".json")
    if target.is_file() and manifest.is_file():
        meta = json.loads(manifest.read_text(encoding="utf-8"))
        if hashlib.sha256(target.read_bytes()).hexdigest() == meta["sha256"]:
            print(f"Cached {target}")
            return
    span = (end - start).days + 1
    payload = download(f"area/csv/{key}/{source}/{bbox}/{span}/{start}")
    rows = 0
    for row in read_csv(payload):
        if None in row or any(row[field] is None for field in FIELDS):
            raise ValueError("FIRMS response contains an incomplete row")
        if not start <= date.fromisoformat(row["acq_date"]) <= end:
            raise ValueError("FIRMS returned a detection outside the requested window")
        rows += 1
    meta = {
        "source": source, "bbox": bbox, "start": str(start), "end": str(end),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "sha256": hashlib.sha256(payload).hexdigest(), "rows": rows,
    }
    atomic_write(target, payload)
    atomic_write(manifest, json.dumps(meta, indent=2).encode("utf-8"))
    print(f"Saved {target} ({rows} detections)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("availability")
    for name in ("plan", "fetch"):
        command = commands.add_parser(name)
        command.add_argument("--start", required=True, type=date.fromisoformat)
        command.add_argument("--end", required=True, type=date.fromisoformat)
        command.add_argument("--bbox", default="-59,-23,-54,-15")
        command.add_argument("--sources", default="MODIS_SP,VIIRS_NOAA20_SP")
        command.add_argument("--out", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    key = os.environ.get("FIRMS_MAP_KEY", "")
    try:
        if args.command != "plan" and not re.fullmatch(r"[A-Za-z0-9_-]+", key):
            raise ValueError("Set FIRMS_MAP_KEY in your local environment")
        if args.command == "availability":
            payload = download(f"data_availability/csv/{key}/ALL")
            reader = csv.reader(io.StringIO(payload.decode("utf-8-sig")))
            header = next(reader, [])
            if len(header) < 3 or not any(row for row in reader if len(row) >= 3):
                raise ValueError("FIRMS did not return an availability table")
            print(payload.decode("utf-8-sig"), end="")
            return
        bbox = bounds(args.bbox)
        sources = list(dict.fromkeys(args.sources.split(",")))
        if not set(sources) <= PRODUCTS:
            raise ValueError(f"Choose sources from {', '.join(sorted(PRODUCTS))}")
        for start, end in windows(args.start, args.end):
            for source in sources:
                if args.command == "plan":
                    print(f"{source} {bbox} {start} {end}")
                else:
                    fetch(key, source, bbox, start, end, args.out)
    except (OSError, ValueError, KeyError) as error:
        message = str(error).replace(key, "[redacted]") if key else str(error)
        parser.exit(1, f"Error: {message}\n")


if __name__ == "__main__":
    main()
