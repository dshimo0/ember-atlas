# Ember Atlas

**[Open Ember Atlas](https://ember-atlas-opal.vercel.app/)** · NASA Space Apps 2026 · Harmonization of MODIS and VIIRS Hot Spots

“Fire season, or sensor change?” Ember Atlas lets a regional land-management analyst compare NASA FIRMS observations across sensors before prioritizing an unusually active month for seasonal review. The English application opens on September 2024 in the full Pantanal study rectangle, with the holdout result, historical finding and downloadable evidence.

## Shortest judge walkthrough

1. Read the opening result: **80.5% lower monthly MAE against MODIS**, from **1,021.7 to 199.7 occupied cell-days/month**, over 24 paired holdout months in 2023–2024. Factors were fit only on 2020–2022.
2. In September 2024, compare **MODIS 5,819**, **VIIRS common-grid 8,809**, and **adjusted VIIRS 4,879.1 cell-days**. The adjusted value is still **16.2% below MODIS**; MODIS is a reference, not ground truth.
3. Both sensors recorded activity above their own prior September medians: MODIS **2,532**, VIIRS **4,782**, from **2020–2023 (n=4)**. Expand either baseline to inspect its years and values. Native detections remain separate: **23,396 MODIS / 101,659 VIIRS**.
4. Select any of the 60 released months. Training and holdout years are labeled. Select a subregion to see why its adjustment and historical anomaly are unavailable. Country boundaries orient the map; the rectangle is a study window, not the biome boundary.
5. Download the selected month's observations, then the selected-period aggregates. Reconcile the figures using the validation and provenance links, available without a login.

## Released coverage and export scopes

Both aggregate history and observation exports cover **2020-01-01–2024-12-31 UTC** for MODIS C6.1 SP (Terra/Aqua pooled) and VIIRS NOAA-20 375 m SP: **1,213,587 deduplicated observations**, 737 canonical raw window manifests, 60 complete paired months. Retrieval is complete; actual swath/cloud observation coverage is unknown.

| Control or export | Actual scope |
| --- | --- |
| Available calendar range | Changes visible months and the aggregate export period. Default is the full released history. |
| Calendar month | Changes the selected comparison, map and observation export. September 2024 is preselected. |
| Area / sensor | Applies to every view and both exports. Northern and southern halves never receive the full-area adjustment. |
| Observations CSV | Selected month intersected with the UTC date range, chosen area and sensors. Includes source references, original confidence, FRP, UTC acquisition time and snapshot SHA-256. Default September export: 125,055 records. |
| Selected-period aggregates CSV | One row per visible month and chosen product, with native counts, occupied cell-days, exact date scope, retrieval status, method and supported adjustment. Default full-history export: 120 rows. |

Partial months retain their actual selected dates, with no full-month adjustment or anomaly. Unretrieved periods have blank aggregate counts and disabled observation exports. A successfully retrieved zero-detection selection is labeled separately. Neither thermal anomalies nor cell-days identify unique fires or burned area.

## Evidence and provenance

- [Versioned validation JSON](https://ember-atlas-opal.vercel.app/data/validation-ba55acfc7909.json): frozen split, factors, acceptance rule, overall and quarterly error/bias.
- [UI provenance index](https://ember-atlas-opal.vercel.app/data/dashboard.json): immutable derived summary, validation and original snapshot hashes.
- [Original observation snapshot](https://ember-atlas-opal.vercel.app/data/snapshot-19621fa88d40.json.gz): normalized records and original extract manifests.
- [Monthly full-area evidence](https://ember-atlas-opal.vercel.app/data/monthly_comparison.csv) and [sensitivity diagnostics](https://ember-atlas-opal.vercel.app/data/diagnostics.json).
- [Judging review](docs/Ember-Atlas-Judging-Review.md), [pitch and walkthrough](docs/Ember-Atlas-Pitch-Roast.md), [submission package](submission/PROJECT-PAGE.md), [resources](submission/RESOURCES.md) and [owner checklist](submission/RELEASE-CHECKLIST.md).

The adjustment passes the unchanged frozen rule but retains mean signed bias of **−124.0 cell-days/month** against MODIS in holdout. It is supported only for complete months in the full study rectangle and evaluated 2020–2024 domain. Timing, clouds, sensitivity and latitude-dependent grid area remain limitations. There is no calibrated earlier legacy handoff or defensible uncertainty interval from only two independent holdout years.

## Run and rebuild

The web app is static, requires no credentials and uses native ES modules and gzip `DecompressionStream`. Python 3.10+ standard library rebuilds the published data. Serve locally:

```sh
python -m http.server 8000 --directory web
```

Reproduce the pipeline from committed raw extracts, preserving the frozen split:

```sh
python scripts/merge_pilot.py
python scripts/build_calendar.py data/matched data/calendar.csv
python scripts/harmonize.py data/calendar.csv web/data/validation.json --train 2020,2021,2022 --holdout 2023,2024
python scripts/snapshot.py data/matched
python scripts/diagnostics.py
python scripts/build_dashboard.py
python -m unittest discover -s tests
node tests/test_model.mjs
```

`build_dashboard.py` verifies the pinned snapshot checksum, creates daily UI aggregates and versioned monthly observation shards, and reconciles every full-area monthly native/grid value with the frozen validation artifact. The browser verifies derivative checksums and loads only the selected month's observations. The original whole snapshot is retained; no new observations or calibration fits are introduced by this UI step. Rebuilding the original snapshot updates its build timestamp and identity while preserving scientific values; rebuilding derivatives from the same pinned input is deterministic.

For acquisition, configure `FIRMS_MAP_KEY` only in the ingestion environment, then run `python scripts/firms.py availability` before bounded fetches or `python scripts/resume_matched.py`. NASA places this credential in keyed URLs; never print, commit or add it to Vercel. Original source files and SHA-256 manifests remain under `data/`. See [data methodology](specs/002-data.md) and [deployment runbook](docs/DEPLOYMENT.md).

Browser verification uses Playwright and Chromium available in the execution environment. With the site served locally, run `BASE_URL=http://localhost:8000 python scripts/check_judging_flow.py`. It checks both desktop and mobile against the original snapshot, including zero versus missing and CSV contents. See `submission/judging-check-public.json` for the executed public release checks after deployment.

## Operating and submission limits

The first buyer hypothesis is a regional fire or land-management organization preparing recurring seasonal reviews. A pilot should measure review preparation time and reproducibility before making impact, demand or willingness-to-pay claims. Monitored areas and scheduled reports are potential services; NASA data remain publicly sourced.

The public app and source are available independently of PR merge status. Production uses the authorized explicit Vercel CLI workflow; Git auto-deployment is not enabled. A real screen recording is hosted at https://ember-atlas-opal.vercel.app/assets/workflow-capture.mp4 . Its official Project Demonstration format, local pitch duration, roster, eligibility, terms and final submission remain separate Team Owner checks. No final judging submission is claimed.
