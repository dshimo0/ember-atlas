# Ember Atlas | Pantanal map and sensor comparison

Public application: https://ember-atlas-opal.vercel.app/

## Opening

“This map shows NASA FIRMS observations in the Pantanal study area for September 2024. Both sensors recorded activity above their own September medians from 2020–2023. The comparison beside the map uses a common grid to express monthly activity in occupied cell-days.”

## Walkthrough

1. Start on the Pantanal map and September 2024. Show the study rectangle, rivers, settlements and sensor legend. Pan or zoom to inspect the observations, then use Fit study area.
2. Show the comparison: MODIS 5,819, VIIRS common-grid 8,809 and adjusted VIIRS 4,879.1 occupied cell-days. The adjusted estimate remains 16.2% below MODIS that month.
3. Show the measured validation result: monthly MAE against MODIS decreased from 1,021.7 to 199.7 cell-days, an 80.5% reduction over 24 paired months in 2023–2024. Factors were fit only on 2020–2022, and apply to the full study rectangle.
4. Show the September baselines: MODIS median 2,532 and VIIRS median 4,782, each using four complete prior Septembers. Native detections remain separately available at 23,396 and 101,659.
5. Change the month or sensor, then the study-area half. The map and downloads change together; subregions have no inherited adjustment. The observation CSV covers the selected month, while the aggregate CSV covers the chosen calendar period.

## Three-minute local presentation

| Time | Screen | Narration |
| --- | --- | --- |
| 0:00–0:30 | Pantanal map, September 2024 | “Ember Atlas displays fire activity from NASA FIRMS in a fixed Pantanal study window. These points are thermal-anomaly observations from MODIS and NOAA-20 VIIRS. In September 2024, both records were above their own historical September medians.” |
| 0:30–1:00 | Zoom, pan, scale and study rectangle | “The basemap provides rivers, settlements and boundaries. The dashed rectangle defines the analysis area. The map samples points for visibility; the CSV retains every matching observation. The local geographic layer keeps the map available when external tiles fail.” |
| 1:00–1:40 | Sensor comparison and validation strip | “On a common 0.05-degree grid, September totals are 5,819 MODIS and 8,809 VIIRS cell-days. A quarterly adjustment fitted on 2020–2022 was evaluated on all 24 paired months in 2023–2024. Monthly mean absolute error against MODIS decreased by 80.5%, from 1,021.7 to 199.7 cell-days.” |
| 1:40–2:10 | Residual and baseline values | “Adjusted VIIRS is 4,879.1 cell-days in September, still 16.2% below MODIS. The comparison measures agreement with a satellite reference. Average adjusted bias is minus 124.0 cell-days per month; clouds, observation timing and sensitivity remain relevant.” |
| 2:10–2:35 | Calendar, subregion filter | “The monthly calendar covers 2020–2024 and labels training and holdout years. Northern and southern views retain their own observations but do not inherit the full-area factor.” |
| 2:35–3:00 | Downloads and Methods & data | “A regional analyst can use the record to prioritize months for seasonal review. The observation export matches the selected month, dates, area and sensors. The aggregate export covers the full chosen period. The snapshot, validation and provenance files support reproduction.” |

## Media format

The local presentation and the official Project Demonstration are separate deliverables. The current official portal format and São Paulo pitch duration require Team Owner confirmation. The hosted screen recording is at https://ember-atlas-opal.vercel.app/assets/workflow-capture.mp4 . Its runtime and interface version are recorded in `submission/media-check.json` and `submission/DEMONSTRATION.md`.

All scientific figures refer to `snapshot-19621fa88d40.json.gz` and `validation-ba55acfc7909.json`. The study rectangle is not a verified biome boundary. The release does not measure burned area or unique fires, and has no observation-quality masks or ground-truth accuracy assessment.
