# Observed archive and sensor transition replay

## Study areas and source identity

The versioned registry derives from `data/region-definitions-v1.json`. All eight presets are explicit WGS84 rectangles. The Pantanal study area preserves `[-59,-23,-54,-15]` in west/south/east/north order. Definitions and actual bounds are displayed rather than implying official biome or administrative boundaries. A different mask requires recomputation and evaluation.

Raw FIRMS CSVs retain byte hashes, requested product/bbox/window, retrieval UTC, delivered rows and processing class in adjacent manifests. The normalizer verifies checksums, requested dates, coordinates, acquisition times and row counts. It deduplicates product/platform/UTC time/coordinates while preserving each source-manifest reference. Public dataset inventories link those inputs; monthly observation shards and daily summaries are immutable checksum-verified derivatives. Original files stay immutable. Current enriched shards preserve every frozen record and add literal source fields through verified joins to the original CSVs.

Products are FIRMS MODIS_SP (Terra/Aqua pooled; literal reported versions retained), NOAA-20 VIIRS 375 m SP, and separate MODIS/NOAA-20 NRT snapshots. The source availability table is preserved in `data/source-availability-2026-11-15.csv` (UTC). Earliest service availability and published retrieval completeness are different facts. The original adjustment domain ends in 2024; raw SP coverage is listed independently in the current regional registry.

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

Replay historical context uses complete earlier same-calendar-month values in the published evaluation domain (2020–2024 for Pantanal; through July 2026 for the newly evaluated regions), excluding the target and future years and requiring at least three. Before the cutoff the baseline entries are observed MODIS; after it they use adjusted VIIRS where supported. Factors are trained before the scenario cutoff. The as-of rule concerns acquisition-month chronology. All values use the current retrieved SP records; uniform processing vintage is unverified; the replay does not reconstruct historical publication latency or past processing revisions. Older MODIS is observational archive context, not additional evidence for cross-era comparability. Platform mix and usable observation conditions can differ in the older archive. Raw sensor medians are descriptive within-product comparisons and show their actual years/n; they are not causal attribution.

## Other regions and NRT

The seven additional study areas have 79 complete paired SP months, January 2020–July 2026. Each independently met the registered local fit/evaluation gates and publishes its own selected quarterly factors, never the Pantanal factors. Pantanal north/south masks retain their own raw activity and prior-year medians but do not inherit full-area calibration. Arbitrary custom polygons and biome masks are not published.

Recent detections are separate NRT datasets with actual product names, UTC start/end, last retrieval and partial-month status. Do not compare seven NRT days against an entire historical month. NRT historical comparison is withheld. Joining NRT and SP requires matched revisions/overlap, identical geometry/grid/windows, quality and duplicate/revision handling, and independent evaluation of the processing-level transition. None of those joins is assumed here.

## Source archive packaging

The new original CSVs and adjacent retrieval manifests are preserved byte-for-byte in deterministic archives under `data/source-archives/`, with a SHA-256 index covering every archive member. `python scripts/source_archives.py unpack` restores the exact `data/history/`, `data/regions/` and original covering-query paths recorded in observation provenance. Unpacking refuses to overwrite changed existing source files. Regional building and resumed ingestion invoke this reconstruction automatically. The original `data/matched` files and original snapshot are retained unchanged. Packaging keeps the Git review manageable without omitting raw evidence.

## Registered regional expansion protocol

The original Pantanal snapshot, factors and 2020–2024 publication domain remain immutable. Protocol commit `17403f3` preceded the new acquisition: [regional-evaluation-protocol-v1.json](../data/regional-evaluation-protocol-v1.json). New regions use the same 0.05° grid, UTC-day occupancy definition and unchanged study rectangles.

For each new region, fit two candidates on 2020–2021: a through-origin least-squares scalar minimizing the sum of squared monthly residuals, and quarterly ratios of summed MODIS to VIIRS cell-days with the documented pooled fallback. Choose the smaller monthly MAE on 2022; ties within 1e-9 prefer the scalar. Refit that choice once on 2020–2022. Do not change the choice after inspecting outer results.

Evaluate all three methods (unadjusted, scalar, quarterly) on identical complete paired months in 2023–2024, those months excluding the already published September 2024, and January 2025–July 2026. The latter 19 months are out-of-time evaluation, never training or selection. September 2024 was already observed in the previous release, so the entire outer partition is not claimed to be unseen. Publish a new regional adjustment only with 36 training, 24 outer and 19 external complete months, and lower MAE with no worse absolute signed bias than unadjusted VIIRS on each evaluation partition. Report every candidate and monthly residual even if publication is withheld. Rank the six most active months by observed MODIS activity, not candidate errors.

Pantanal's 19 fresh months can audit extrapolation but do not meet the separately registered 24-fresh-month requirement to replace or extend its frozen publication. Additional observed months remain usable as raw sensor history.

### Source-preserving covering queries

[Acquisition amendment](../data/covering-acquisition-amendment-v1.json) reduces repeated South American source queries without changing any analytical mask or evaluation rule. Preserve the original covering CSV and its SHA-256. Derive each study area's missing date window using inclusive WGS84 bounds and UTC acquisition dates, retaining the original field values. Every derived manifest links the covering manifest and hash. Reapply that exact filter and compare bytes before aggregation. The original and filtered files are both packaged in the source archives. Empty filtered output is zero reported detections for a successfully retrieved area/time, not proof of usable satellite coverage.

### SP/NRT availability audit

[Processing-transition audit](../web/data/processing-transition.json) derives same-sensor temporal intersection from the captured NASA availability table. As captured, MODIS SP ends August 2026 and its NRT starts September; NOAA-20 SP ends July and NRT starts August. There is no coincident processing-class window. No empirical SP/NRT correction or joined series is supported. Preserve actual NRT retrieval vintages; when SP later covers those acquisition dates, retrieve the identical geometry and windows, evaluate each sensor/product pair, and define a new independent acceptance protocol before joining them. A temporal gap cannot be treated as paired evaluation.

## Literal source versions and thermal-source flags

The NASA download page advertises MODIS Collection 6.1, but observed API rows include literal version strings such as `6.03` and `61.03`. They are retained without rewriting or inferring that these labels establish a uniform processing vintage. Independent interpretation/normalization of reported version transitions remains unverified. The comparison reference is the actual MODIS_SP archive as delivered, not an independently established homogeneous collection or ground truth.

All reported thermal-source types remain in the frozen count/grid metric. NASA documents MODIS flags 0 presumed vegetation fire, 1 active volcano, 2 other static land source and 3 offshore. VIIRS raw codes are retained without asserting an independently validated mapping. Missing NRT type fields stay blank. These flags do not establish fire-event identity. Source counts by type are native-detection counts, not additive shares of occupied cell-days.

For the frozen September 2024 Pantanal case, raw MODIS flags are 23,368 type 0 and 28 type 2; VIIRS reports 101,263 type 0, 4 type 2 and 392 type 3. Totals remain 23,396/101,659; the published 5,819/8,809 cell-days and frozen factors are unchanged. Additional source fields are joined back to each original frozen record using its exact source manifest and observation identity, with SHA and original-field checks. No existing snapshot or factor file is overwritten. Every current observation CSV, daily attribute total and monthly export retains literal source information.

Verified source definitions (HTTP 200, 2026-11-15 UTC): [NASA attributes](https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs), [FIRMS FAQ](https://www.earthdata.nasa.gov/data/tools/firms/faq), [NASA archive](https://firms.modaps.eosdis.nasa.gov/download/). Historical statistics describe reported activity and do not independently remove processing-vintage or source-type effects.

## Regional evaluation

<!-- REGIONAL-EVALUATION:START -->
| Study area | Inner choice | Outer MAE: raw → choice (n) | Fresh MAE: raw → choice (n) | Fresh signed bias | Published adjustment |
| --- | --- | ---: | ---: | ---: | --- |
| Pantanal | seasonal | 1,021.7 → 199.7 (24) | 399.4 → 70.8 (19) | 67.4 | frozen seasonal through 2024-12-31 |
| Southern Amazon | seasonal | 4,584.5 → 567.5 (24) | 1,428.4 → 168.7 (19) | 61.5 | seasonal through 2026-07-31 |
| Cerrado | seasonal | 3,826.8 → 506.5 (24) | 2,641.7 → 322.1 (19) | 116.5 | seasonal through 2026-07-31 |
| Gran Chaco | seasonal | 3,941.8 → 405.8 (24) | 2,923.7 → 213.9 (19) | 97.5 | seasonal through 2026-07-31 |
| California | seasonal | 945.1 → 124.1 (24) | 977.7 → 146.0 (19) | 124.9 | seasonal through 2026-07-31 |
| Southeastern Australia | seasonal | 1,453.3 → 228.9 (24) | 1,604.0 → 147.8 (19) | 13.8 | seasonal through 2026-07-31 |
| Iberian Peninsula | seasonal | 738.9 → 71.5 (24) | 794.6 → 123.0 (19) | -72.8 | seasonal through 2026-07-31 |
| Siberia | seasonal | 5,521.3 → 824.5 (24) | 5,080.4 → 850.0 (19) | 303.9 | seasonal through 2026-07-31 |

Units: occupied cell-days/month; full named study rectangle, SP only. Inner choice uses 2022 after fitting 2020–2021; refit uses 2020–2022. Outer: 2023–2024, including the previously published September 2024; the artifact also reports the sensitivity excluding that month. Fresh: January 2025–July 2026, excluded from fitting and selection. Pantanal retains the original publication regardless of the new audit. A failed regional gate withholds adjustment. MODIS is the comparison reference, not ground truth.
<!-- REGIONAL-EVALUATION:END -->

The literal MODIS label split is systematic in this archive: 6.03 for training, 61.03 for outer/fresh evaluation. Source-field audit files record native counts by product/version/type and split. Factors target the as-delivered training MODIS_SP scale; holdout comparison uses the as-delivered later reference. Numerical agreement does not isolate sensor effects or establish homogeneous processing continuity. The monthly replay remains an explicitly labeled scenario.
