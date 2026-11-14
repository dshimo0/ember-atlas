# Ember Atlas

[Public dashboard](https://ember-atlas-opal.vercel.app/) · NASA Space Apps 2026 · Harmonization of MODIS and VIIRS Hot Spots

Ember Atlas displays NASA FIRMS fire activity for the Pantanal study area from January 2020 through December 2024. The dashboard opens on September 2024 with an interactive map, a sensor comparison and the historical baseline. The full monthly calendar follows the map and comparison.

## Dashboard

- The OpenStreetMap basemap includes rivers, settlements and boundaries. Zoom, pan, metric scale and **Fit study area** operate on the map view. The study rectangle and sampled FIRMS observations are separate overlays.
- A locally served Natural Earth map supplies country boundaries, rivers and settlements if tiles fail. It supports the same navigation and observations. No Pantanal biome geometry is included.
- The selected month, area and sensor determine the observations on the map and in the observation CSV. Map pan and zoom do not change the export scope.
- The observation download is beside the map. The aggregate download is beside the calendar and covers the selected date range.

## Data and validation

The release contains **1,213,587 deduplicated observations**, 737 canonical raw window manifests and 60 complete paired months for MODIS C6.1 SP (Terra/Aqua) and NOAA-20 VIIRS 375 m SP. Both aggregate and observation coverage are **2020-01-01–2024-12-31 UTC**.

Quarterly adjustment factors were fit on **2020–2022** and evaluated on **24 complete paired months in 2023–2024**. Monthly MAE against MODIS decreased from **1,021.7 to 199.7 occupied cell-days/month**, an **80.5% reduction** calculated from the unrounded artifact values. Mean signed bias after adjustment is **−124.0 cell-days/month**. The factors apply only to complete months in the full study rectangle; subregion and partial-month adjustments are unavailable.

September 2024 recorded activity above both sensors' prior September medians (2020–2023, n=4):

| Product | Occupied cell-days | Historical median | Native detections |
| --- | ---: | ---: | ---: |
| MODIS | 5,819 | 2,532 | 23,396 |
| NOAA-20 VIIRS | 8,809 | 4,782 | 101,659 |
| Adjusted VIIRS | 4,879.1 | — | — |

The adjusted September value remains 16.2% below MODIS. MODIS is a reference for sensor agreement, not ground truth. Detections and cell-days do not measure unique fires or burned area. Retrieval completeness is distinct from swath/cloud observation coverage, which remains unknown. Missing numeric values stay blank; retrieved zero detections remain zero.

## Exports and provenance

| Export | Scope |
| --- | --- |
| Observations | Selected month intersected with the date range, area and sensors. Includes coordinates, UTC date/time, product, platform, confidence, FRP, original source reference and snapshot SHA-256. Default September export: 125,055 records. |
| Aggregates | Each month/product in the chosen date range, with native detections, occupied cell-days, clipped dates, retrieval status, method and eligible adjustment. Default full-history export: 120 rows. |

- [Immutable validation](https://ember-atlas-opal.vercel.app/data/validation-ba55acfc7909.json)
- [Snapshot and derivative index](https://ember-atlas-opal.vercel.app/data/dashboard.json)
- [Original observation snapshot](https://ember-atlas-opal.vercel.app/data/snapshot-19621fa88d40.json.gz)
- [Monthly reference evidence](https://ember-atlas-opal.vercel.app/data/monthly_comparison.csv)
- [Sensitivity diagnostics](https://ember-atlas-opal.vercel.app/data/diagnostics.json)
- [Resources and attribution](submission/RESOURCES.md)

## Run and reproduce

The static frontend uses locally vendored Leaflet 1.9.4, native ES modules and gzip `DecompressionStream`. Live FIRMS access is not required. Python 3.10+ standard library rebuilds the scientific inputs and presentation derivatives.

```sh
python -m http.server 8000 --directory web
```

From the committed raw inputs:

```sh
python scripts/merge_pilot.py
python scripts/build_calendar.py data/matched data/calendar.csv
python scripts/harmonize.py data/calendar.csv web/data/validation.json --train 2020,2021,2022 --holdout 2023,2024
python scripts/snapshot.py data/matched
python scripts/diagnostics.py
python scripts/build_dashboard.py
python scripts/build_geography.py
python -m unittest discover -s tests
node tests/test_model.mjs
```

The original versioned snapshot and frozen acceptance rules are unchanged. The derivative builder verifies the snapshot hash and reconciles all full-area monthly native/grid totals with validation before publishing summaries and monthly observation shards. Rebuilding from the same pinned input is deterministic; recreating the original snapshot updates its build timestamp and identity.

Browser checks require Playwright and Chromium. With a local server running, use `BASE_URL=http://localhost:8000 python scripts/check_judging_flow.py`. The suite checks desktop and mobile layouts, map navigation, tile-failure fallback, filter synchronization and CSV contents against the pinned observations. Public results are recorded in [judging-check-public.json](submission/judging-check-public.json).

Ingestion credentials belong only in `FIRMS_MAP_KEY` in the ingestion environment. Never add them to the frontend or Vercel. See [data methodology](specs/002-data.md), [deployment](docs/DEPLOYMENT.md), [verification review](docs/Ember-Atlas-Judging-Review.md) and [presentation script](docs/Ember-Atlas-Pitch-Roast.md).
