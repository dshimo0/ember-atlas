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

## Access recovery follow-up

After the environment configuration was published, FIRMS availability and bounded downloads worked again. Resume fills only uncovered UTC days, preserving prior manifests. The full 2020–2024 paired domain is required before the updated release report is generated; the frozen 2020–2022 training / 2023–2024 holdout and acceptance rule remain unchanged. The Vercel team still has no Ember Atlas project, and no CLI credential is present.

## Production hosting closeout

After user-completed CLI authentication, project creation and static production deployment succeeded in the existing Vercel Hobby team. https://ember-atlas-opal.vercel.app serves the pinned observations anonymously. Deployment inputs were checked to exclude ingestion and raw data. Complete public browser flow, CSV downloads and mobile checks passed; official portal guide verification and final owner submission remain separate pending gates.

## Current release closeout

The earlier dated access/hosting statements above are historical. The current release adds eight observed SP/NRT presets, a 2000–2024 Pantanal MODIS archive, the January 2023 continuity replay, independent holdout benchmark, scalar/seasonal/unadjusted comparison and full-data map cells. See docs/challenge-traceability.md and submission/transition-release.json for current implementation and deployed evidence. No regional adjustment is published without local multi-year evaluation, and final portal submission remains with the Team Owner.
