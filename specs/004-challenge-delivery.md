# Challenge delivery and Chilecito acceptance contract

Status: implementation target, not a statement of completed capabilities.
This addendum extends specs 001–003. Existing frozen Pantanal evidence remains immutable.
Requirement basis: challenge-author video transcript supplied by the project owner,
especially 01:12–01:32, 02:28–03:38 and 03:51–04:40. These are product requirements;
the stretch goals below are our commitments, not additional competition rules.

## Mission and user

Enable a fire monitoring analyst to select an area and period, inspect its historical
burning activity, identify seasonal patterns and unusual activity, and export evidence.
Preserve the usefulness of MODIS history as VIIRS becomes the continuing source.
The primary outcome is a defensible continuous activity record. A live hotspot map
and a sensor-transition replay support that outcome but do not replace it.

## Geographic scope

Keep the eight existing regions. Add **Chilecito, La Rioja, Argentina** as the ninth
study area and the challenge-author case study. Proposed acquisition rectangle:
west -68.0, south -30.0, east -67.0, north -29.0 (EPSG:4326).
This is a project-defined exploratory box, not a municipality, incident perimeter,
or CONAE-approved geometry. Verify it against authoritative geographic/incident
material before publishing a named event analysis. Version any geometry change and
invalidate incompatible factors, summaries and baselines.

Investigate July 2026 with an initial event review window July 20–August 5.
The screenshots show July 28 and July 31; the wider window is a project choice.
Acquire only products/dates actually available. Historical NRT may require archived
downloads; a currently unavailable API period is a gap, never a fabricated observation.
Include all retrieved hotspots without attributing each one to the illustrated fire.
Do not infer burned hectares or spread predictions from hotspot counts.

## Required deliverables and evidence

| ID | Deliverable | Release acceptance | Evidence / owner role |
| --- | --- | --- | --- |
| R1 | Reproducible NASA inputs | CSVs and hashes, product/platform, SP/NRT, UTC dates, exact geometry, retrieval timestamps; missing windows recorded | Acquisition manifest; data engineer |
| R2 | Historical calendar | Observed MODIS record from earliest available years, overlapping VIIRS and recent data; disclose actual coverage for every region | Per-product coverage matrix, monthly CSV; data engineer |
| R3 | Harmonized activity | Common spatial/time unit, documented reference scale and locally evaluated transfer; no silent union or borrowed regional coefficient | Versioned model card, fit/evaluation inputs and residuals; science lead |
| R4 | Continuous series | Explicit source-selection policy and each month's source/model; test transition against held-out observations | Source-tagged series and transition replay; science lead |
| R5 | Region and date selection | Nine presets plus coordinate AOI; synchronize calendar/map/results/export; unsupported AOIs retain observed data without adjustment | Desktop/mobile flow tests; frontend engineer |
| R6 | Patterns and anomalies | Seasonal profile, same-month historical median with years/n, selected-period anomaly and sufficient-support handling | Recomputed metrics and accessible table; science lead |
| R7 | Current context | Recent data and actual freshness; compare equivalent elapsed periods only; join SP/NRT only after transition evaluation | Matched-window report and product lineage; data engineer |
| R8 | Downloadable analytics | Observations, native counts, occupied cell-days, harmonized estimates, baseline, source and quality fields reconcile with UI | CSV round-trip tests and manifest; QA |
| R9 | Analyst workflow | Select area → read calendar → inspect unusual period → locate activity → export; English UI, keyboard/mobile, working attributed map | Recorded walkthrough, screenshots and URL; frontend engineer |
| R10 | Public submission | English description, NASA/other resource citations, accessible code and application, real measured results and limitations | Submission checklist and public-link test; team owner |

Historical coverage and regional validation are separate milestones. A nine-button
interface does not establish nine validated histories. Target multiple complete years
for all nine; prioritize Chilecito and Pantanal end-to-end. List remaining gaps explicitly.

## Scientific protocol

1. Keep native detections separate from occupied cell-days and harmonized estimates.
   Common grid aggregation reduces resolution effects but does not correct sensitivity,
   overpass schedule, cloud cover or sensor drift by itself. MODIS is a reference, not truth.
2. Calibrate each region/product pair independently. NOAA-20 factors cannot silently
   transfer to S-NPP or NOAA-21. Preserve platform and processing class in lineage.
3. The supplied local script reproduces the existing seasonal method and compares a
   training-only scalar and raw VIIRS. Default train 2020–2022, evaluation 2023–2024.
   Require 36 complete training and 24 complete evaluation months. Retrieval completeness
   is not clear-sky coverage. A passed legacy acceptance gate is not deployment approval.
4. Freeze protocol before new evaluation. Existing inspected 2023–2024 results cannot
   become a fresh blind test. Replacement selection requires nested blocked-year evaluation
   or a new untouched time block with adequate available data. Prefer a scalar if more
   complex candidates do not demonstrate useful out-of-sample improvement.
5. Report MAE, signed bias, every monthly residual, relative error where reference >0,
   peak-season errors and anomaly agreement. Examine grid-size/latitude sensitivity,
   missing observations and day/night composition. Do not fit to headline catastrophes.
6. A historical median uses only earlier comparable years, with a floor of three and
   a preferred target of ten or more. Show years/n; do not call a three-year reference
   a stable climatology. No synthetic curves, added noise or event multipliers.
7. Keep observed historical context, validated continuity and replay visually distinct.
   An unsupported recent transfer remains native data. Do not normalize a monthly median
   to a week by simple day multiplication without validating within-month seasonality.
8. Preserve high-resolution VIIRS observations in the map/export alongside the aggregate
   calendar. An adjusted aggregate is not a new geolocated hotspot detection.

## Exceeding the brief: prioritized stretch deliverables

| Priority | Deliverable | Measurable completion |
| --- | --- | --- |
| E1 | Chilecito case study | Reproducible observed July 2026 timeline, actual sources, verified geometry, contextual calendar and downloadable briefing; unavailable records disclosed |
| E2 | Counterfactual sensor retirement | Hide MODIS after a fixed cutoff; recover reference-scale history with VIIRS; reveal held-out MODIS and all errors |
| E3 | Strong-method comparison | Raw, scalar and seasonal evaluated on identical months; peak errors visible; no cherry-picked winner |
| E4 | Analyst briefing | Printable one-page region/period/map/calendar/anomaly/evidence report, with source links and retrieval timestamp |
| E5 | Geographic portability | Nine independent coverage/model cards; arbitrary AOI recalculation; unsupported calibration gracefully disabled |
| E6 | Reproducible science | One local command, resumable downloads, immutable inputs, model artifacts, input hashes and documented failure recovery |

Satellite imagery and official incident products can enrich E1 with attribution and
licensing review. A forecasting system, fire-spread model, deep-learning model or GPU
training is not required by the supplied challenge brief.

## Release gates and current gaps

- G0: geometry and data-availability review; approve documented study extent.
- G1: all requested files accounted for; hash and coordinate checks pass.
- G2: complete paired overlap and independent evaluation; publish failures too.
- G3: R1–R9 exercised end-to-end on actual data, including zero/missing/partial months.
- G4: submission links, attribution, language and team eligibility checked by owner.

Current addition delivers this specification and a local acquisition/calibration script.
Chilecito data ingestion, UI publication, current/historical joining, nine-area calibration,
briefing export and final submission are not completed by writing this document.
Update the coverage matrix with observed dates, artifact paths and evidence before
marking any row complete. Retain an implementation backlog linked to these IDs.

## Local execution

See [local-calibration.md](../docs/local-calibration.md). Run acquisition/evaluation
into an isolated directory; inspect results before integrating with the published site.
NASA reference: https://firms.modaps.eosdis.nasa.gov/api/area/ and
https://firms.modaps.eosdis.nasa.gov/api/data_availability/ . The Area API supports
one-to-five-day queries; availability must be checked for each product and period.
