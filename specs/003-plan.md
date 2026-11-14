# Hackathon build plan

| Order | Task | Exit criterion |
| --- | --- | --- |
| 1 | Bootstrap ingestion and daily baseline | Dry-run, automated tests and a local fixture pass. |
| 2 | Acquire real pilot data | Retrieve MODIS SP and NOAA-20 SP for the demo rectangle, verify schemas and hashes, and review matched monthly counts. |
| 3 | Acquire regional historical data | Record coverage gaps, standard products and exact source versions in a reproducible manifest. |
| 4 | Implement and evaluate harmonization | Publish raw/grid/calibrated comparison and holdout results with data limitations. |
| 5 | Ship the browser demo | Region/date filters, calendar, anomaly view and CSV export work using cached data and a local static build. |
| 6 | Submit | Public source and demo links open without sign-in, and the pitch walks through one regional example and its evidence. |

Start with an analyst selecting the Pantanal, spotting an unusual month and exporting the underlying detections. Make the before/after sensor comparison the main scientific exhibit.

## 2026-11-14 execution evidence

Real pilot complete; canonical historical extracts and compressed public snapshot acquired. Common-grid and frozen seasonal candidate evaluated, but only five holdout months are complete, so adjusted publication is blocked by the minimum support rule. Static dashboard, subarea/date/sensor filtering, month selection, prior same-month sensor baselines and observation CSV implemented. Vercel create-project denied (403); no authorized DO SSH access. Official Space Apps resources returned 503. Submission package distinguishes these pending gates and does not claim public deployment or final submission.
