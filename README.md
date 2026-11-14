# Ember Atlas

NASA Space Apps Challenge 2026 · São Paulo, Brazil · Harmonization of MODIS and VIIRS Hot Spots.

Ember Atlas is building an interactive burning activity calendar from NASA FIRMS thermal anomaly detections. The initial demonstration uses a rectangular window around the Pantanal. See [requirements](specs/001-product.md), [data contract and methodology](specs/002-data.md), and [build plan](specs/003-plan.md).

## Run with Python 3.10+

Run from the repository root. Only the Python standard library is required.

```powershell
python scripts/firms.py plan --start 2024-08-01 --end 2024-09-30
python -c "import os; print('FIRMS key configured' if os.getenv('FIRMS_MAP_KEY') else 'Set FIRMS_MAP_KEY in your environment')"
python scripts/firms.py availability
python scripts/firms.py fetch --start 2024-08-01 --end 2024-09-30
python scripts/build_calendar.py data/raw data/calendar.csv
```

Set `FIRMS_MAP_KEY` locally using a key from the [FIRMS Area API](https://firms.modaps.eosdis.nasa.gov/api/area/). The default historical pair is `MODIS_SP,VIIRS_NOAA20_SP`. Check availability for both products first. An optional recent layer can be ingested separately with `--sources VIIRS_NOAA20_NRT --out data/recent` and explicit UTC dates. For a multiyear backfill, request regional CSV exports from the [FIRMS Archive](https://firms.modaps.eosdis.nasa.gov/download/) and record their actual processing level and date coverage. The Area API path is for bounded, resumable slices.

The calendar script emits daily raw detection counts and distinct grid-cell counts by UTC day, product and bounding box for successfully retrieved windows. It implements the spatial baseline only. Calibration and the public web app are specified and tracked in the build plan.

## Publish

The repository is intended for public collaboration. If a GitHub remote is pending, run `gh repo create ember-atlas --public --source=. --remote=origin --push` from this directory using the intended account. Credit NASA FIRMS and cite the products used in any release. See [NASA FIRMS](https://www.earthdata.nasa.gov/data/tools/firms) and the [challenge brief](https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/).

## ember-1 dashboard and reproducibility

Serve the pinned release with `python -m http.server 8000 --directory web` and open http://localhost:8000. No API key or dependency installation is needed for the dashboard. Modern browsers need native gzip `DecompressionStream` support. The compressed snapshot is about 11 MB; memory and initial-load cost remain a limitation on low-memory devices.

Rebuild from the committed raw extracts:

```sh
python scripts/merge_pilot.py
python scripts/build_calendar.py data/matched data/calendar.csv
python scripts/harmonize.py data/calendar.csv web/data/validation.json --train 2020,2021,2022 --holdout 2023,2024
python scripts/snapshot.py data/matched
python scripts/diagnostics.py
python -m unittest discover -s tests
```

See [measured release evidence](submission/RESULTS.md), [portal copy](submission/PROJECT-PAGE.md), [deployment runbook](docs/DEPLOYMENT.md) and [submission gates](submission/RELEASE-CHECKLIST.md). Snapshot payload hashes include build time: a rebuild produces the same scientific values, with a new snapshot identity. Original downloads and their checksums remain pinned. Gzip preserves all normalized observations; raw CSVs preserve all source fields.

The beachhead is a regional fire or land-management organization preparing seasonal reviews. The open product links sensor comparisons to reproducible evidence. Monitored AOIs and scheduled reporting are potential service offerings, subject to pilot validation of review time, reproducibility, demand and willingness to pay. NASA observations remain publicly sourced.
