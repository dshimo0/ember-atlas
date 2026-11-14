# FIRMS data and harmonization

## Ingestion

- Pilot region uses WGS84 bbox `-59,-23,-54,-15` in west, south, east, north order. The demonstration starts with August–September 2024. Use FIRMS availability before requesting additional dates.
- Use MODIS C6.1 SP for the legacy series and VIIRS NOAA-20 SP for the continuation. Consider S-NPP SP as a bridge from 2012 and NOAA-21 SP as an additional sensitivity check. Validate each platform transition independently. NASA's archive lists S-NPP coverage ending on 2 November 2026.
- API requests cover at most five inclusive dates. Persist raw CSV and a manifest with product, bbox, date window, download UTC, byte hash and row count. Keep NRT files in a separate directory and track their processing level.
- Use the bulk regional FIRMS archive for the long history. It requires Earthdata or email authentication. Verify the processing level of delivered files before incorporating them.

## Reference dataset and reproducibility

| Layer | Contract |
| --- | --- |
| Raw reference | Keep every record and field returned for the selected AOI, products and dates in immutable original CSV extracts. Pair each extract with a manifest containing source, processing class, AOI, requested dates, retrieval time, SHA-256 and delivered row count. Record platform identifiers where available. Use the Area API for bounded extracts and the regional archive for the historical backfill. |
| Normalized observations | Preserve source and original confidence, normalize coordinates and acquisition datetime in UTC, and retain platform, day/night and fire radiative power (FRP, MW) when present. Keep a reference to the raw extract and track deduplication separately from delivered counts. |
| Published analysis | Generate versioned monthly data by AOI and product, with native detection counts, occupied cell-days, retrieval completeness, and calibrated values only where validated. Missing windows remain missing. A retrieved day with zero records indicates zero recorded detections. |

Begin with the existing paired August–September 2024 Pantanal extract to check ingestion, schemas and aggregation. Then acquire multiple full overlapping years of MODIS and VIIRS NOAA-20 standard processing and pin their input manifests before calibration. Keep standard processing and near-real-time records separate. Keep the FIRMS key in `FIRMS_MAP_KEY` and exclude keyed request URLs from published artifacts.

## Common metric

Retain all original fields in raw CSV. Normalize coordinates, UTC acquisition timestamp, platform and sensor-specific confidence in the next stage. An exact duplicate within a product should contribute once to the raw comparison, using source platform, time and coordinates. Preserve the raw delivered count for auditing. The current baseline counts delivered records and unique occupied cells on a globally aligned 0.05-degree WGS84 grid per UTC day and product. Grid cells have latitude-dependent physical area and edge sensitivity. Aggregate occupied cell-days monthly within a fixed AOI. Keep the number of retrieved UTC days as a separate completeness indicator. A retrieved day with zero detections leaves actual observation coverage unknown without swath and quality masks.

## Calibration and acceptance

1. Compare raw monthly counts against occupied cell-days on aligned complete months. Test sensitivity to grid size, confidence selection and MODIS Terra versus Aqua sampling changes.
2. Fit a robust VIIRS-to-MODIS scale on matched complete months from training years. Compute the ratio from seasonal totals with a documented fallback for sparse seasons. Use blocked holdout years and keep each platform's results visible. Quantify seasonal error and transition discontinuity, and report uncertainty via year-block resampling if enough years exist.
3. Compare against both raw concatenation and the uncalibrated grid baseline. Report holdout MAE, signed bias and seasonal behavior. If calibration fails to improve the grid baseline or overlap is insufficient, ship sensor-specific lines and flag the harmonized series as unavailable.
4. Compute anomalies against the historical median for the same month using only complete comparable years, excluding the target year. Emit absolute deviation and omit percent when the median is zero. Keep partial current months provisional.

## Calibration command and output contract

Implement `scripts/harmonize.py` as the reproducible next stage after `scripts/build_calendar.py`. The input is the daily calendar CSV with dates, AOI, product, raw counts and occupied cells. Require explicit training and holdout year lists and reject overlapping lists or mixed AOIs in a single fit. A paired month is eligible only when the extract manifests and daily calendar establish retrieval for every UTC day for both products. Keep observation coverage separate from retrieval completeness.

For each defined season, fit the factor as the training sum of MODIS occupied cell-days divided by the training sum of VIIRS occupied cell-days over matched eligible months. Define the seasons, minimum support and pooled fallback before inspecting holdout results. If the pooled denominator is zero or the support requirement fails, leave the applicable factor unavailable. Hold the fitted factors fixed during validation. Compare adjusted and unadjusted VIIRS to MODIS using the same eligible holdout months and common cell-day units. Treat the comparison of native counts as a separate diagnostic. Record the acceptance rule before fitting and report unavailable calibration explicitly when evidence is insufficient or the rule fails.

| Output | Minimum contents |
| --- | --- |
| `monthly_comparison.csv` | AOI and month, both products' native counts and occupied cell-days, both products' retrieval completeness, applied factor and adjusted VIIRS value when eligible, split and calibration status. |
| `validation.json` | Method version, input snapshot identity and checksums, AOI, grid and product identifiers, training and holdout years, season rules, fitted factors, paired month counts and exclusions, unadjusted and adjusted holdout MAE and signed bias, and acceptance decision with reason. |

Add regression checks for missing versus zero detections, incomplete paired months, overlapping year lists and zero denominators. Verify the first scientific result on real held-out FIRMS observations. Report September 2024 as a held-out example only if its year was excluded from fitting.

Sources

- [NASA FIRMS Area API](https://firms.modaps.eosdis.nasa.gov/api/area/)
- [NASA FIRMS availability](https://firms.modaps.eosdis.nasa.gov/api/data_availability/)
- [NASA FIRMS archive and temporal coverage](https://firms.modaps.eosdis.nasa.gov/download/)

## Release ember-1 frozen evaluation

Before holdout examination: training 2020–2022, holdout 2023–2024, calendar quarters (Jan–Mar etc.). Seasonal ratios require six complete training months and 100 VIIRS cell-days, otherwise pooled training ratio. Overall requires at least three training and two holdout years. Accept only lower holdout monthly MAE and no increase in absolute signed bias on identical complete paired months. No uncertainty interval with only two holdout years. Derived native counts deduplicate identical product/platform/time/coordinates; raw files retain delivered counts. Calibration is limited to the study rectangle. Subarea medians and transfer are withheld. Alternate grid/confidence and platform diagnostics are required before treating transfer as robust outside this release domain.

## Complete-overlap release

After access recovery, all 60 paired months in 2020–2024 were acquired without changing the training years or holdout criteria. The 24 holdout months pass the fixed rule. The public selected-month comparison and aggregate export may show the seasonal adjusted NOAA-20 value only for the full rectangle, a complete month and the evaluated domain. Northern/southern filters retain separate sensor counts and withhold adjustment. The selected month now also filters the coordinate map. Detailed seasonal residuals remain published; no uncertainty interval or earlier legacy handoff is asserted.
