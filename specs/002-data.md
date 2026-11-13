# FIRMS data and harmonization

## Ingestion

- Pilot region uses WGS84 bbox `-59,-23,-54,-15` in west, south, east, north order. The demonstration starts with August–September 2024. Use FIRMS availability before requesting additional dates.
- Use MODIS C6.1 SP for the legacy series and VIIRS NOAA-20 SP for the continuation. Consider S-NPP SP as a bridge from 2012 and NOAA-21 SP as an additional sensitivity check. Validate each platform transition independently. NASA's archive lists S-NPP coverage ending on 2 November 2026.
- API requests cover at most five inclusive dates. Persist raw CSV and a manifest with product, bbox, date window, download UTC, byte hash and row count. Keep NRT files in a separate directory and track their processing level.
- Use the bulk regional FIRMS archive for the long history. It requires Earthdata or email authentication. Verify the processing level of delivered files before incorporating them.

## Common metric

Retain all original fields in raw CSV. Normalize coordinates, UTC acquisition timestamp, platform and sensor-specific confidence in the next stage. An exact duplicate within a product should contribute once to the raw comparison, using source platform, time and coordinates. Preserve the raw delivered count for auditing. The current baseline counts delivered records and unique occupied cells on a globally aligned 0.05-degree WGS84 grid per UTC day and product. Grid cells have latitude-dependent physical area and edge sensitivity. Aggregate occupied cell-days monthly within a fixed AOI. Keep the number of retrieved UTC days as a separate completeness indicator. A retrieved day with zero detections leaves actual observation coverage unknown without swath and quality masks.

## Calibration and acceptance

1. Compare raw monthly counts against occupied cell-days on aligned complete months. Test sensitivity to grid size, confidence selection and MODIS Terra versus Aqua sampling changes.
2. Fit a robust VIIRS-to-MODIS scale on matched complete months from training years. Compute the ratio from seasonal totals with a documented fallback for sparse seasons. Use blocked holdout years and keep each platform's results visible. Quantify seasonal error and transition discontinuity, and report uncertainty via year-block resampling if enough years exist.
3. Compare against both raw concatenation and the uncalibrated grid baseline. Report holdout MAE, signed bias and seasonal behavior. If calibration fails to improve the grid baseline or overlap is insufficient, ship sensor-specific lines and flag the harmonized series as unavailable.
4. Compute anomalies against the historical median for the same month using only complete comparable years, excluding the target year. Emit absolute deviation and omit percent when the median is zero. Keep partial current months provisional.

Sources

- [NASA FIRMS Area API](https://firms.modaps.eosdis.nasa.gov/api/area/)
- [NASA FIRMS availability](https://firms.modaps.eosdis.nasa.gov/api/data_availability/)
- [NASA FIRMS archive and temporal coverage](https://firms.modaps.eosdis.nasa.gov/download/)
