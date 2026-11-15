# Ember Atlas

[Explore](https://ember-atlas-opal.vercel.app/) · [Sensor transition replay](https://ember-atlas-opal.vercel.app/demo?region=pantanal&view=replay&benchmark=1&month=2024-09) · [Pitch](https://ember-atlas-opal.vercel.app/pitch)

Ember Atlas serves observed NASA FIRMS fire activity for eight explicitly bounded study areas. Pantanal is the default scientific walkthrough. All initial observations, daily summaries and exports are versioned snapshots; visitors do not supply a FIRMS key. The interactive OpenStreetMap basemap has an attributed local Natural Earth fallback.

## Verify the transition

1. Open `/demo` on Pantanal. The primary reference-scale calendar replays a source change at **January 2023**, immediately after training ends.
2. Select December 2022 and January 2023. The source changes from observed MODIS to frozen seasonally adjusted NOAA-20 VIIRS on the MODIS reference scale. Every month identifies its source and adjustment.
3. Reveal the separate observed holdout MODIS benchmark. MODIS actually remains available after the cutoff; the cutoff is a replay scenario, not a mission end date.
4. Inspect September 2024: MODIS 5,819, common-grid VIIRS 8,809, seasonal replay 4,879.1 occupied cell-days. The replay is 16.2% below MODIS. Historical context uses complete earlier matched-domain months, without future years.
5. Export source-tagged replay months, matching observations, full-data occupied-day cells, selected-period aggregates and a checksum manifest. Change region, sensor or dates; the map and exports use the same mask and UTC scope.

The map's primary analytical layer is observed occupied UTC days per 0.05° cell for one named sensor, computed from all matching records. Sampled detections are a separate optional inspection layer. Monthly calibration does not move points or adjust the spatial occupancy layer. Retrieved zero detections, missing retrieval and unknown usable satellite observation coverage remain distinct.

## Published coverage

<!-- COVERAGE:START -->
| Study area (W/S/E/N) | Observed SP coverage | Recent NRT UTC window | Adjustment |
| --- | --- | --- | --- |
| Pantanal (-59, -23, -54, -15) | MODIS_SP: 2000-11-01–2024-12-31 (8827 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2024-12-31 (1827 retrieved days) | 2026-11-08–2026-11-14 | Evaluated full area, SP 2020–2024 only |
| Southern Amazon (-65, -13, -48, -5) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | 2026-11-08–2026-11-14 | Unavailable; multi-year regional evaluation missing |
| Cerrado (-55, -20, -44, -8) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | 2026-11-08–2026-11-14 | Unavailable; multi-year regional evaluation missing |
| Gran Chaco (-66, -32, -57, -17) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | 2026-11-08–2026-11-14 | Unavailable; multi-year regional evaluation missing |
| California (-125, 32, -114, 42.5) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | 2026-11-08–2026-11-14 | Unavailable; multi-year regional evaluation missing |
| Southeastern Australia (140, -44, 154, -28) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | 2026-11-08–2026-11-14 | Unavailable; multi-year regional evaluation missing |
| Iberian Peninsula (-10, 35, 4, 44.5) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | 2026-11-08–2026-11-14 | Unavailable; multi-year regional evaluation missing |
| Siberia (60, 50, 140, 72) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | 2026-11-08–2026-11-14 | Unavailable; multi-year regional evaluation missing |
<!-- COVERAGE:END -->

Each preset is a project-defined WGS84 rectangle called a **study area**, not an official biome/state mask. The [versioned registry](https://ember-atlas-opal.vercel.app/data/regions.json) links to exact geometries, sources, products, observation counts and immutable SP/NRT datasets. Broad Siberia means 60–140°E, 50–72°N; Southeastern Australia means 140–154°E, 44–28°S, including Tasmania. Full bounds appear in the application and registry.

Pantanal's older MODIS backfill extends observational history only. The paired calibration domain remains **2020–2024**. The seven other areas initially have one complete matched SP month and no independently evaluated adjustment. All eight have a separate recent seven-day NRT snapshot; it is a partial-month view, never spliced into the SP series. Missing or incomplete archive periods remain blank where a complete monthly reference-scale value is required.

## Three-method evidence

All methods use the same full Pantanal study area, 36 training months in 2020–2022 and 24 complete paired holdout months in 2023–2024. The scalar minimizes training-only through-origin squared monthly residuals: `a = sum(VIIRS × MODIS) / sum(VIIRS²)`.

| Method | Holdout MAE | Signed bias | Peak-six MAE | Peak-six bias |
| --- | ---: | ---: | ---: | ---: |
| Unadjusted VIIRS, common grid | 1,021.7 | +1,021.7 | 2,225.2 | +2,225.2 |
| Training-only scalar (0.5497999782) | 175.3 | −54.3 | 404.6 | −404.6 |
| Existing frozen quarterly factors | 199.7 | −124.0 | 534.6 | −534.6 |

Units are occupied cell-days/month. The six peak months are the holdout months with greatest observed MODIS activity, ranked before considering method residuals: August/September 2024, November 2023, October/June/July 2024 in descending activity. Every monthly residual is published in [CSV](https://ember-atlas-opal.vercel.app/data/replay-residuals.csv) and the [versioned evaluation](https://ember-atlas-opal.vercel.app/data/replay-evaluation.json).

The scalar performs better on this existing holdout. The seasonal method remains the published frozen rule; no replacement was selected using the same evaluation evidence. Any later method selection requires a preregistered new outer holdout or nested blocked-year protocol. The seasonal 80.5% reduction is against unadjusted common-grid VIIRS, **not against the scalar**. MODIS is a comparison reference; these results do not establish detection accuracy, ground-truth accuracy or global performance.

## Evidence and reproduction

- [Original frozen validation](https://ember-atlas-opal.vercel.app/data/validation-ba55acfc7909.json) and [original snapshot](https://ember-atlas-opal.vercel.app/data/snapshot-19621fa88d40.json.gz) remain unchanged.
- [Methodology](docs/methodology.md), [data specification](specs/002-data.md), [challenge traceability](docs/challenge-traceability.md), [pitch/script](docs/pitch.md), [resources](submission/RESOURCES.md) and [release checks](docs/release-checklist.md).
- [Eight-region execution evidence](submission/eight-region-check-public.json) and [release identity](submission/transition-release.json).

```sh
python scripts/serve.py
python -m unittest discover -s tests
node --test tests/test_*.mjs
BASE_URL=http://127.0.0.1:8000 python scripts/check_eight_regions.py
```

Static HTML/CSS, native ES modules and locally vendored Leaflet 1.9.4; no new backend or framework. Direct loads/refreshes of `/`, `/demo` and `/pitch` use the established Vercel rewrites. Browser checks require Playwright, Chromium and pdfinfo. Mobile checks use viewport/touch emulation, not a physical device.

Ingestion requires `FIRMS_MAP_KEY` only in its environment. `scripts/acquire_regions.py` reuses the original bounded downloader and checksum manifests; `--history --respect-quota` resumes older Pantanal MODIS with quota backoff. Run `scripts/evaluate_replay.py`, `scripts/build_regions.py` and `scripts/build_geography.py` to reproduce public derivatives, then update coverage documentation. Original raw payload bytes and manifests are retained in deterministic `data/source-archives/` packages. `python scripts/source_archives.py unpack` restores their exact recorded paths; resumed ingestion and building do this automatically. Run `python scripts/source_archives.py pack` after new ingestion.

Remaining scientific gaps: multi-year overlap and independent calibration for seven areas; expanded out-of-time evaluation; usable swath/cloud masks; ground truth; validated NRT/SP joining and a biome-mask analysis. Team roster, current official media requirements, human pitch rehearsal, terms and final submission remain Team Owner actions. The nine-slide presentation is separate from the unverified official Project Demonstration format.
