# Reproducible Pantanal release

Python 3.10+ standard library; no Python dependencies to install. Serve `web/` as static files on Vercel. No web runtime receives NASA credentials. No paid DigitalOcean resource was created; the existing n8n host was not modified.

## Ingestion gate

Configure `FIRMS_MAP_KEY` in the runtime secret store, scoped to ingestion only. Never paste it into a command, Git, frontend, or submission. This session confirmed it is absent. NASA's public API documentation was reachable with authorized outbound network access; authenticated product availability remains unverified.

Run from repository root:

```sh
python scripts/firms.py availability
python scripts/firms.py fetch --start 2024-08-01 --end 2024-09-30
python scripts/build_calendar.py data/raw data/calendar.csv
```

Retain the returned availability table in `data/availability.csv` before backfill. Check both SP products' coverage. Freeze 2019–2021 training / 2022–2024 holdout before collecting/evaluating, provided all those years are available. If unavailable, document a different disjoint split before inspecting outcomes. Full years are preferred. For each supported year run bounded `fetch --start YYYY-01-01 --end YYYY-12-31`. Requests resume verified cached windows. Observe NASA quota and stop on rate-limit failures. A first two-month slice does not support adjustment.

```sh
python scripts/build_calendar.py data/raw data/calendar.csv
python scripts/harmonize.py data/calendar.csv data/evaluation --train 2019,2020,2021 --holdout 2022,2023,2024
python scripts/snapshot.py data/raw web/data
python -m unittest discover -s tests
python -m http.server 8000 --directory web
```

Raw files are ignored by Git. Archive them and manifests in approved durable storage. Commit only reviewed public content-addressed snapshots and pointer (`web/data` is versioned). Snapshot verifies all raw manifests before writing the immutable hash object and atomically updates the pointer last. Keep the previous pointer on ingestion failure. Rebuild from the same raw files yields the same snapshot bytes.

## Science release gate

Transfer version ember-seasonal-v1 uses DJF/MAM/JJA/SON and ratios of pooled training occupied cell-days. Minimum three distinct training and two holdout years; seasonal factors require six months over three training years and at least 100 VIIRS cell-days, otherwise use the pooled factor. Strictly lower holdout MAE with non-increasing absolute bias is required. Missing paired months are excluded, not set to zero. An adjustment passing the aggregate criterion still needs seasonal, platform, confidence, grid-size and transition diagnostics before publication. The current browser deliberately shows sensor-specific comparisons only. Exported calibration metrics are not yet integrated into the browser.

The static calendar recalculates unadjusted subarea cell-days from coordinates and requires three complete prior same-month years for a median. Full-month comparison is labeled as such; date filters restrict map/export records, and selected month further restricts both. Incomplete months cannot establish anomalies. A rectangle is not the official Pantanal biome boundary. No swath masks are provided; observation coverage is unknown.

## Deployment and verification

Deploy static `web/` using repository `vercel.json`; FIRMS secrets must never be configured on Vercel's public web project. Before release, test a clean browser: choose bounds, UTC dates and sensor; click a month; compare both rows; download CSV; verify timestamps, bounds, source checksums and selected dates against raw files. Test mobile and keyboard. No real-data end-to-end evidence exists yet. Do not equate an unavailable-data shell with a completed scientific release.
