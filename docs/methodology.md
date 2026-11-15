# Observed archive and sensor transition replay

## Study areas and source identity

The versioned registry derives from `data/region-definitions-v1.json`. All eight presets are explicit WGS84 rectangles. The Pantanal study area preserves `[-59,-23,-54,-15]` in west/south/east/north order. Definitions and actual bounds are displayed rather than implying official biome or administrative boundaries. A different mask requires recomputation and evaluation.

Raw FIRMS CSVs retain byte hashes, requested product/bbox/window, retrieval UTC, delivered rows and processing class in adjacent manifests. The normalizer verifies checksums, requested dates, coordinates, acquisition times and row counts. It deduplicates product/platform/UTC time/coordinates while preserving each source-manifest reference. Public dataset inventories link those inputs; monthly observation shards and daily summaries are immutable checksum-verified derivatives. An original 2020–2024 Pantanal shard retains its original source dataset hash inside the expanded inventory.

Products are MODIS C6.1 SP (Terra/Aqua pooled), NOAA-20 VIIRS 375 m SP, and separate MODIS/NOAA-20 NRT snapshots. The source availability table is preserved in `data/source-availability-2026-11-15.csv` (UTC). Earliest service availability and published retrieval completeness are different facts. The SP archive release ends in 2024 even where NASA currently serves later data.

## Quantities and missingness

The globally anchored WGS84 grid is 0.05°. Each occupied cell counts once per product per UTC day. Sum daily occupied-cell counts into monthly occupied cell-days. Physical area varies with latitude. Native detections, occupied cell-days, unique fires and burned area are different quantities.

The map aggregates all selected observations into occupied UTC days for each cell and one explicitly named sensor. Its optional sampled-point layer is for inspection, not density estimation. Summing map cell occupancies equals the selected product's common-grid cell-days and cell CSV. Monthly factors never adjust point coordinates or individual cell occupancy.

A manifest-backed retrieved day with no observations contributes numeric zero. An absent source window contributes no daily row. Complete-month reference-scale values require all calendar days; missing and partial periods are unavailable, not zero. Usable satellite observation coverage remains unknown without swath/cloud quality masks. A complete retrieval does not establish complete observation opportunity.

## Frozen calibration and three baselines

The original `ember-1` training split, factors, support requirements and acceptance rule remain unchanged. Training is 36 complete paired months in 2020–2022; holdout is 24 complete paired months in 2023–2024, all in the full Pantanal study area. Quarterly training ratios use MODIS sum / VIIRS sum with the original minimum support and pooled fallback. Acceptance requires lower holdout monthly MAE and no worse absolute signed bias than the unadjusted grid baseline on identical months.

The audit adds a single scalar baseline with a stated fitting objective: nonnegative through-origin least squares on training monthly cell-days. The positive optimum is `sum(V*M)/sum(V²) = 0.5497999781946175`. It is not fitted to the holdout and is not the same objective as the quarterly total-ratio method. All three methods use identical paired area/months. MAE and signed bias are computed from `method VIIRS − observed MODIS` monthly residuals. Positive bias means exceeding MODIS.

The immutable replay evaluation contains all residuals, overall metrics and the six-month peak stress test. Peak selection is descending observed holdout MODIS activity, with month ascending for ties, taking six months; no candidate residual is used to select them. Peak months in order are 2024-08, 2024-09, 2023-11, 2024-10, 2024-06, 2024-07.

| Method | MAE | Bias | Peak MAE | Peak bias |
| --- | ---: | ---: | ---: | ---: |
| Unadjusted common-grid VIIRS | 1021.708333 | +1021.708333 | 2225.166667 | +2225.166667 |
| Single scalar | 175.329287 | −54.344752 | 404.601727 | −404.601727 |
| Frozen seasonal | 199.699731 | −123.968300 | 534.637305 | −534.637305 |

Units: occupied cell-days/month. The scalar is better on this existing holdout. That finding is evaluation evidence, not permission to select a new publication method on the same holdout. Retain the frozen seasonal output and explicitly expose the comparison. A later method-selection exercise must define its candidates and objective before looking at a new outer evaluation period, or use a nested blocked-year design. No confidence interval or ground-truth accuracy is inferred.

## Continuity replay and what was knowable then

The scenario cutoff is derived from the end of the verified training window: **January 2023**. Before it, replay values are observed MODIS. After it, replay values are seasonally adjusted NOAA-20 VIIRS on the MODIS-reference scale, limited to complete evaluated months. Observed MODIS still exists after the cutoff and is a separately revealed benchmark. This is an inspectable replay, not an actual end of MODIS availability or an independently validated future operational handoff.

Every replay CSV month retains source, adjustment, factor, cutoff/scenario, value, separate benchmark, dates, retrieval status and dataset hash. Missing post-cutoff calibration remains unavailable. There is no sum or average of overlapping products. Native observations and spatial occupancy remain sensor-specific.

Replay historical context uses complete earlier same-calendar-month values in the paired evaluation domain (2020–2024), excluding the target and future years and requiring at least three. Before the cutoff the baseline entries are observed MODIS; after it they use adjusted VIIRS where supported. Factors are trained before the scenario cutoff. The as-of rule concerns acquisition-month chronology. All values use the current retrieved SP processing vintage; the replay does not reconstruct historical publication latency or past processing revisions. Older MODIS is observational archive context, not additional evidence for cross-era comparability. Platform mix and usable observation conditions can differ in the older archive. Raw sensor medians are descriptive within-product comparisons and show their actual years/n; they are not causal attribution.

## Other regions and NRT

The seven additional study areas have verified common-grid MODIS/NOAA-20 SP comparison for their published matched window. They have no multi-year regional fit/holdout, so adjustment and continuity replay are disabled. Pantanal north/south masks retain their own raw activity and prior-year medians but do not inherit full-area calibration. Arbitrary custom polygons and biome masks are not published.

Recent detections are separate NRT datasets with actual product names, UTC start/end, last retrieval and partial-month status. Do not compare seven NRT days against an entire historical month. NRT historical comparison is withheld. Joining NRT and SP requires matched revisions/overlap, identical geometry/grid/windows, quality and duplicate/revision handling, and independent evaluation of the processing-level transition. None of those joins is assumed here.

## Source archive packaging

The new original CSVs and adjacent retrieval manifests are preserved byte-for-byte in deterministic archives under `data/source-archives/`, with a SHA-256 index covering every archive member. `python scripts/source_archives.py unpack` restores the exact `data/history/` and `data/regions/` paths recorded in observation provenance. Unpacking refuses to overwrite changed existing source files. Regional building and resumed ingestion invoke this reconstruction automatically. The original `data/matched` files and original snapshot are retained unchanged. Packaging keeps the Git review manageable without omitting raw evidence.

## Registered regional expansion protocol

The original Pantanal snapshot, factors and 2020–2024 publication domain remain immutable. Protocol commit `17403f3` preceded the new acquisition: [regional-evaluation-protocol-v1.json](../data/regional-evaluation-protocol-v1.json). New regions use the same 0.05° grid, UTC-day occupancy definition and unchanged study rectangles.

For each new region, fit two candidates on 2020–2021: a through-origin least-squares scalar minimizing the sum of squared monthly residuals, and quarterly ratios of summed MODIS to VIIRS cell-days with the documented pooled fallback. Choose the smaller monthly MAE on 2022; ties within 1e-9 prefer the scalar. Refit that choice once on 2020–2022. Do not change the choice after inspecting outer results.

Evaluate all three methods (unadjusted, scalar, quarterly) on identical complete paired months in 2023–2024, those months excluding the already published September 2024, and January 2025–July 2026. The latter 19 months are out-of-time evaluation, never training or selection. September 2024 was already observed in the previous release, so the entire outer partition is not claimed to be unseen. Publish a new regional adjustment only with 36 training, 24 outer and 19 external complete months, and lower MAE with no worse absolute signed bias than unadjusted VIIRS on each evaluation partition. Report every candidate and monthly residual even if publication is withheld. Rank the six most active months by observed MODIS activity, not candidate errors.

Pantanal's 19 fresh months can audit extrapolation but do not meet the separately registered 24-fresh-month requirement to replace or extend its frozen publication. Additional observed months remain usable as raw sensor history.

### Source-preserving covering queries

[Acquisition amendment](../data/covering-acquisition-amendment-v1.json) reduces repeated South American source queries without changing any analytical mask or evaluation rule. Preserve the original covering CSV and its SHA-256. Derive each study area's missing date window using inclusive WGS84 bounds and UTC acquisition dates, retaining the original field values. Every derived manifest links the covering manifest and hash. Reapply that exact filter and compare bytes before aggregation. The original and filtered files are both packaged in the source archives. Empty filtered output is zero reported detections for a successfully retrieved area/time, not proof of usable satellite coverage.

### SP/NRT availability audit

[Processing-transition audit](../web/data/processing-transition.json) derives same-sensor temporal intersection from the captured NASA availability table. As captured, MODIS SP ends August 2026 and its NRT starts September; NOAA-20 SP ends July and NRT starts August. There is no coincident processing-class window. No empirical SP/NRT correction or joined series is supported. Preserve actual NRT retrieval vintages; when SP later covers those acquisition dates, retrieve the identical geometry and windows, evaluate each sensor/product pair, and define a new independent acceptance protocol before joining them. A temporal gap cannot be treated as paired evaluation.
