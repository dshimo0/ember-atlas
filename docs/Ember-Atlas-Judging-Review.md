# Ember Atlas | Judging evidence and retest

Reviewed application: https://ember-atlas-opal.vercel.app/ . Input code baseline: `6f56476baa55cf845dad8a44b4372e5c2cde63a4`, branch `work`. Scientific input is unchanged: `snapshot-19621fa88d40.json.gz`, uncompressed SHA-256 `19621fa88d408fb5d9aa87482de1bb219e8dd7ed67128c1147d1a63fb087e677`. Immutable validation: `validation-ba55acfc7909.json`. UI aggregate identity: `dashboard-a8513f5e713b.json`. Refreshed application release commit: `26f646a3da5c5e3757ec41e1a9d7aee3b2f307ff`; production deployment `dpl_62Ng6iCCLSvKpBQyYEt4PjHY5ZBg`.

Before changing the interface, the deployed `data/latest.json` and `data/validation.json` were fetched and matched repository bytes. [Before desktop](../submission/review-before-desktop.png) and [before mobile](../submission/review-before-mobile.png) capture that release. This review is an engineering/scientific self-review, not a claim of independent judge or user approval.

## Scientific evidence checked

- Frozen fit: 2020–2022, 36 complete paired months. Holdout: 2023–2024, 24 complete paired months. Acceptance rules and factors were not changed or refit for this redesign.
- Common-grid monthly MAE against MODIS: 1,021.7083333333334 → 199.6997313847094 cell-days/month, a calculated 80.45433076451603% reduction (UI 80.5%). Signed bias: +1,021.7083 → -123.9683. The residual and two-year independent support remain limitations.
- September 2024: 5,819 MODIS / 8,809 VIIRS / 4,879.05299 adjusted VIIRS cell-days. Adjustment leaves -939.9470 cell-days (-16.1531%) relative to MODIS; it improves this month's agreement but does not establish accuracy against ground truth.
- Prior September medians: MODIS 2,532 and VIIRS 4,782, complete 2020–2023 (n=4), excluding the target year. September 2024 is above both, by 129.8% / 84.2%. Native detections remain separate at 23,396 / 101,659.
- The derivative builder verifies the snapshot checksum and reconciles every full-area monthly native/grid value with the original scientific artifact before publishing summaries and monthly shards. Coverage is 2020-01-01–2024-12-31 for both aggregates and observation exports. Retrieval is complete; swath/cloud observation coverage remains unknown.

## Findings and status

| Severity | Observed problem and judge consequence | Implemented fix | Owner / retest status |
| --- | --- | --- | --- |
| P0 | Strong validation result was below the map; percentage improvement and scope were not prominent. | First viewport derives 80.5% from unrounded artifact values, shows MAE before/after, split, sample size, geographic scope and reference caveat. | Engineering — Verified locally and on production |
| P0 | Landing state did not explain the September finding or residual in one common unit. | September preselected; three-series chart, -16.2% residual and two prior same-month median breakdowns with years/n. | Engineering — Verified locally and on production |
| P0 | Default date range exposed only two months despite five years of released inputs. | All 60 months visible by year; TRAIN / HOLDOUT text labels and selected-state markers. Mobile wraps into touch-sized four-column groups. | Engineering — Verified locally and on production |
| P0 | “Selected aggregates” exported only the active month, with ambiguous scope. | Explicit selected-month observations versus entire selected-period aggregates; 125,055 default observation rows / 120 aggregate rows reconcile with the source. | Engineering — Verified locally and on production |
| P0 | Incorrect treatment of missing periods could turn absence into a low-activity claim. | Real zero day 2020-01-08, partial September interval and absent December 2019 are separately exercised; unavailable counts export blank. | Engineering — Verified locally and on production |
| P1 | A subregion could appear to inherit the displayed overall validation result. | Overall card explicitly says full study area; subregion comparison explains why factors/anomalies are unavailable, and CSV factor/adjusted columns remain blank. | Engineering — Verified locally and on production |
| P1 | Coordinate-only plot lacked geographic context. | Attributed, locally served Natural Earth country boundaries/labels; study rectangle remains distinct from country borders and is explicitly not the biome. | Engineering — Verified locally and on production |
| P1 | Map/export scope and active selection were difficult to infer. | Month, area, sensor, count and UTC interval shown together; map, chart and observation CSV share selection; date controls explain aggregate-period effects. | Engineering — Verified locally and on production |
| P1 | Whole-snapshot loading was unnecessary for every selected month. | Small verified daily summary supplies the first-screen result; checksum-verified monthly shards supply points/CSV; original snapshot is retained. | Engineering — Verified locally and on production |
| P1 | Mobile reading order put geography before the useful finding. | Validation and month finding precede map; visible focus, shape-coded series, keyboard month/map activation and no document overflow. | Engineering — Verified locally and on production |

## Verification protocol and artifacts

`python -m unittest discover -s tests`: nine pipeline/science tests. `node tests/test_model.mjs`: eight selection, baseline, missingness, scope and CSV tests. `scripts/check_judging_flow.py` uses the original pinned observations as its independent export oracle in fresh desktop (1440×1000) and mobile (390×844) contexts. Mobile checks are viewport emulation, not a physical-device usability study.

The flow checks initial load, month change by keyboard, manual UTC date changes, sensor filter, both subregions, both CSVs, zero retrieval versus missing, native/grid reconciliation and JavaScript exceptions. Northern MODIS September export is 18,038 records. Every default observation row is compared by product, UTC date/time, coordinates and source reference with the original snapshot; common-grid totals and all 120 aggregate rows are checked. [Local machine-readable report](../submission/judging-check-local.json); [Public signed-out report](../submission/judging-check-public.json) passed on both viewports at 2026-11-14T21:38:23.487316+00:00. HTTPS/hostname were independently checked with the system CA store; Chromium used that validated leaf key to accommodate the Cloud proxy.

Visual evidence: `submission/judging-first-viewport.png`, `submission/judging-desktop.png`, `submission/judging-mobile.png`. Source credentials are scanned without printing their values. The original scientific artifact and snapshot checksums must remain unchanged.

## Checks that remain outside this review

- Official Project Demonstration format and São Paulo local pitch duration must be confirmed separately. A new actual 30-second silent recording matches the refreshed interface. Hosted playback is checked separately in submission/media-check.json; official format compliance is still pending.
- Team Owner must verify registration, roster, eligibility of prior work, final resource permissions, form limits and actual submission for judging. Engineering tests cannot establish those gates.
- No independent user interview, timed pilot, physical-device test or commercial demand evidence is claimed. No new geographic calibration or masked observation coverage is available.
- The scientific improvement is agreement with the MODIS reference, not ground-truth accuracy, burned area, unique fire counts or demonstrated prevention.
