# Challenge traceability

Inspected input: branch `work`, commit `f695d772f6e8eaceec0d159ebbbef04a2da2b59b`. Existing production source was `ddefa36`. Root, /demo and /pitch were working; only Pantanal had observed snapshots. The stack remains static HTML/CSS, native modules and Leaflet, with the established Vercel deployment workflow.

| Requirement | Implementation and evidence | Remaining scope |
| --- | --- | --- |
| Demonstrate a sensor transition | January 2023 replay; observed MODIS before and frozen seasonal VIIRS afterward; source/adjustment per month; separate holdout MODIS toggle | Replay scenario, not actual source end or validated future operational handoff |
| Compare harmonization baselines | Versioned Python evaluation and browser recomputation: unadjusted, training-only scalar, original seasonal; identical 36/24 month split and area | Scalar beats seasonal on this evidence; no replacement selected on the existing holdout |
| Peak behavior | Six highest observed MODIS holdout months, no residual-based selection; all methods' MAE/bias and every monthly residual | Independent outer evaluation required for later method selection |
| Primary reference-scale calendar | Source-labeled replay calendar/time series; month drives comparison, map, earlier context and exports | Older MODIS is archive context; replay baselines use earlier complete paired-domain months only |
| Eight observed regions | Ordered registry with explicit geometry/source/products and immutable initial SP/NRT snapshots | Seven areas need multi-year archives and independently evaluated regional calibration |
| Spatial evidence | Full-data occupied UTC days/cell for named product; optional sampled detections; same mask/grid/export | No adjusted coordinates, burned area, unique-fire or complete-observation claim |
| Earliest MODIS | Manifest-verified Pantanal backfill from available November 2000; successful empty days and missing windows distinguished | Older platform mix not independently harmonized; public SP record ends in 2024 |
| Recent activity | Separate source-tagged NRT snapshots, actual UTC dates/retrieval and partial-month status | NRT/SP joining and matched-window historical NRT comparison not validated |
| Maps and geography | OSM, scale/pan/zoom/fit; global Natural Earth fallback; exact project-defined study boxes | No official biome mask; changing it requires recomputation/evaluation |
| Reproducible evidence | Observations, raw aggregates, cell occupancies, replay months, immutable manifests and exact CSV checksums | No usable swath/cloud masks or ground truth |
| Presentation | Nine interactive sections follow source change, replay, benchmark, stronger scalar, peak residual and eight-area world map | Human rehearsal, roster and official demonstration format need owner confirmation |
| Delivery | Local and deployed eight-region desktop/mobile tests, route refresh/filter/cutoff/fallback/CSV checks; release identity in transition-release.json | Mobile is browser emulation; owner submits for judging |

## Published eight-area inventory

<!-- COVERAGE:START -->
| Study area (W/S/E/N) | Observed SP coverage | Recent NRT UTC window | Adjustment |
| --- | --- | --- | --- |
| Pantanal (-59, -23, -54, -15) | MODIS_SP: 2000-11-01–2026-07-31 (9404 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2026-07-31 (2404 retrieved days) | MODIS_NRT: 2026-09-01–2026-11-14 (75 retrieved days); VIIRS_NOAA20_NRT: 2026-08-01–2026-11-14 (106 retrieved days) | Evaluated full area, SP 2020–2024 only |
| Southern Amazon (-65, -13, -48, -5) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | MODIS_NRT: 2026-11-08–2026-11-14 (7 retrieved days); VIIRS_NOAA20_NRT: 2026-11-08–2026-11-14 (7 retrieved days) | No independently evaluated regional SP calibration; NRT remains separate. |
| Cerrado (-55, -20, -44, -8) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | MODIS_NRT: 2026-11-08–2026-11-14 (7 retrieved days); VIIRS_NOAA20_NRT: 2026-11-08–2026-11-14 (7 retrieved days) | No independently evaluated regional SP calibration; NRT remains separate. |
| Gran Chaco (-66, -32, -57, -17) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | MODIS_NRT: 2026-11-08–2026-11-14 (7 retrieved days); VIIRS_NOAA20_NRT: 2026-11-08–2026-11-14 (7 retrieved days) | No independently evaluated regional SP calibration; NRT remains separate. |
| California (-125, 32, -114, 42.5) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | MODIS_NRT: 2026-11-08–2026-11-14 (7 retrieved days); VIIRS_NOAA20_NRT: 2026-11-08–2026-11-14 (7 retrieved days) | No independently evaluated regional SP calibration; NRT remains separate. |
| Southeastern Australia (140, -44, 154, -28) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | MODIS_NRT: 2026-11-08–2026-11-14 (7 retrieved days); VIIRS_NOAA20_NRT: 2026-11-08–2026-11-14 (7 retrieved days) | No independently evaluated regional SP calibration; NRT remains separate. |
| Iberian Peninsula (-10, 35, 4, 44.5) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | MODIS_NRT: 2026-11-08–2026-11-14 (7 retrieved days); VIIRS_NOAA20_NRT: 2026-11-08–2026-11-14 (7 retrieved days) | No independently evaluated regional SP calibration; NRT remains separate. |
| Siberia (60, 50, 140, 72) | MODIS_SP: 2024-09-01–2024-09-30 (30 retrieved days); VIIRS_NOAA20_SP: 2024-09-01–2024-09-30 (30 retrieved days) | MODIS_NRT: 2026-11-08–2026-11-14 (7 retrieved days); VIIRS_NOAA20_NRT: 2026-11-08–2026-11-14 (7 retrieved days) | No independently evaluated regional SP calibration; NRT remains separate. |
<!-- COVERAGE:END -->

All eight initial presets contain real observations, interactive maps and exports without a visitor key. The broader challenge ambition exceeds this release's independently evaluated calibration scope. There is no full globally harmonized multi-decade record. A full archive and local evaluation for the seven added study areas remain explicit open dataset/science items.

## Verification and external gates

Execution reports: [eight-region-check-public.json](../submission/eight-region-check-public.json), [transition-release.json](../submission/transition-release.json), [immutable evaluation pointer](../web/data/replay-evaluation.json), [registry pointer](../web/data/regions.json). New raw payloads and retrieval manifests are committed byte-for-byte in `data/source-archives/`, with member hashes and deterministic restoration to `data/history` and `data/regions`. Original `data/matched` inputs remain unchanged.

Current official challenge/resources guidance could not previously be verified because the official pages returned 503. Do not infer an old deadline, slide cap, eligibility or submission success from documentation. The nine-slide local pitch and official Project Demonstration are separate deliverables. Team Owner confirms the current guide/media rules, human contributions/eligibility, accepts terms and personally completes submission.
