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
