# Data acceptance contract

The implemented method and measured evidence are documented in [methodology.md](../docs/methodology.md). This specification governs publication, not a future feature plan.

| ID | Acceptance criterion |
| --- | --- |
| D1 Inputs | Use real FIRMS observations only. Verify original CSV SHA, row count, requested region/product/processing class, coordinates and UTC acquisition window. Preserve raw payloads and adjacent manifests; never record keyed URLs. |
| D2 Registry | Version eight project-defined study rectangles in requested order, with exact WGS84 geometry, type, source, available products and immutable SP/NRT dataset references. Expose broad-area extents and no official biome implication. |
| D3 Completeness | Daily zero only from successful retrieval. Missing source windows remain absent and monthly missing values stay blank. Partial periods retain actual counts and clipped scope, with no full-month adjustment. Usable satellite coverage remains unknown. |
| D4 Grid | Globally anchored 0.05° WGS84, one occupied cell/product/UTC day. Native detections are separate. Full map-cell occupancies sum to the same selected-period/product cell-days as exports. |
| D5 Frozen fit | Preserve original 36 training / 24 holdout months, support and acceptance rules, source artifacts and quarter factors. No fitting on holdout or transfer to a different region/mask. |
| D6 Baselines | Recompute unadjusted, training-only through-origin least-squares scalar and frozen seasonal on identical full-area paired months. Publish MAE, signed bias and every monthly residual; verify both Python artifact and browser recomputation. |
| D7 Peaks | Six holdout months ranked by observed MODIS cell-days, month ascending for ties. Report all methods on this same subset; no selection using residuals. |
| D8 Selection protocol | The existing holdout is evaluation evidence, not a fresh selection set. Retain the frozen output; require a preregistered new outer holdout or nested blocked-year protocol before choosing a replacement. |
| D9 Replay | Derive January 2023 cutoff from verified training end. Observed MODIS before; eligible seasonal VIIRS after. Benchmark MODIS remains a separate observed layer. Every month/export identifies source, adjustment/factor and scenario. No actual source-availability cutoff is asserted. |
| D10 Historical context | Use earlier complete same-month values, no target/future years, minimum n=3. Replay baselines are limited to the paired 2020–2024 domain; older MODIS remains archive context. Show exact years/n and excluded periods. |
| D11 Regions | Enable historical views only for retrieved periods. All eight open real SP and separate NRT data without visitor keys. No regional factor before local multi-year training and independent holdout evaluation. |
| D12 NRT | Actual UTC window, last retrieval and partial-period status. No joining SP/NRT or full-month historical comparisons without matched-window and processing-transition evidence. |
| D13 Integrity | Version/hash inventories, summaries, shards and evaluation. Keep original snapshot/validation immutable. Verify credentials are absent from repository, exports and decompressed public data. |

Source availability: [FIRMS](https://firms.modaps.eosdis.nasa.gov/api/data_availability/) · [Area API](https://firms.modaps.eosdis.nasa.gov/api/area/) · [archive](https://firms.modaps.eosdis.nasa.gov/download/). Original frozen validation: [validation-ba55acfc7909.json](../web/data/validation-ba55acfc7909.json). Current regional release and scalar evaluation are addressed by `web/data/regions.json` and `web/data/replay-evaluation.json`.

## Regional expansion acceptance

- Keep the original Pantanal artifact and domain unchanged; 19 fresh months are an audit, not authorization to extend a 24-fresh-month gate.
- Apply registered inner selection on 2022 only, then refit on 2020–2022. Require complete support and pass all independent outer, known-month-excluded and external gates before publishing a regional adjustment.
- Preserve every original covering query and verify derived area/date masks against it before aggregation. Different study rectangles never share fitted factors.
- Keep raw regional history available when a gate fails. Show the failed gate and candidate residuals; do not silently switch candidates.
- Version and hash any externally served observation shard at an immutable repository commit. Integrity-check decompressed bytes before map/export use. Preserve previously published local URLs.
- Publish an SP/NRT join only after actual same-sensor/window overlap and a separate evaluation protocol; availability adjacency alone is insufficient.

## Source-field preservation

Preserve each reported `version` and `type` string in current observation shards/CSVs, while retaining immutable legacy files. Enrich frozen records only by joining their exact source manifest and observation identity, checking the source SHA and original normalized fields. Current daily version/type counts must sum to the same native counts and follow the same date/area mask. Include source versions in monthly/replay exports and benchmark versions separately. Do not infer uniform MODIS processing vintage from the source name, or treat all thermal types as independently classified vegetation fires. MODIS type-code definitions have a verified NASA source; VIIRS code interpretation remains explicitly unverified. Keep all types in the frozen metric and do not silently refit or filter the accepted record.

## Presentation invariants

The P0/P1 redesign does not refit factors, alter the grid, filter thermal types, extend any publication domain or rewrite observation shards. Calendar intensity is a view-relative encoding, not a percentile or anomaly estimate. Compact formatting applies only to display labels. The original monthly and observation exports retain numerical precision and provenance. NASA photographs/composites are editorial context with an independent image inventory, not evidence added to the quantitative evaluation.

## Experimental archive publication gates

Backfill detection-count research is isolated from the frozen cell-day release. See [spec 007](007-calendar-backfill.md). Product availability alone is not retrieval completeness or usable satellite coverage.
