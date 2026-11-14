# Measured evidence — completed overlap

NASA FIRMS acquisition resumed successfully after the environment configuration was published. All UTC days from 2020-01-01 through 2024-12-31 are retrieved for MODIS_SP (MODIS C6.1 Terra/Aqua pooled) and VIIRS_NOAA20_SP (375 m). The canonical snapshot contains 1,213,587 deduplicated observations and 737 original window manifests. Earlier invalid-key responses are recorded as a recovered access interruption; their cause is unconfirmed.

## Frozen evaluation

Training: 36 complete paired months, 2020–2022. Holdout: 24 complete paired months, 2023–2024. Grid: globally anchored 0.05° WGS84 per UTC day. Factors were fit only to training data; no thresholds or seasonal settings were tuned on the expanded holdout. Publication is supported within the full study rectangle and evaluated 2020–2024 domain.

| Monthly metric, same 24 holdout months | Unadjusted grid | Candidate adjustment |
| --- | ---: | ---: |
| MAE, occupied cell-days | 1021.71 | 199.70 |
| Signed bias, VIIRS minus MODIS cell-days/month | +1021.71 | -123.97 |

## Seasonal holdout results

| Quarter | n | Baseline MAE | Adjusted MAE | Baseline bias | Adjusted bias |
| --- | ---: | ---: | ---: | ---: | ---: |
| Q1 | 6 | 374.50 | 75.45 | +374.50 | -30.69 |
| Q2 | 6 | 724.50 | 118.97 | +724.50 | -32.10 |
| Q3 | 6 | 1801.33 | 365.44 | +1801.33 | -232.27 |
| Q4 | 6 | 1186.50 | 238.94 | +1186.50 | -200.81 |

## September 2024

| Product | Native detections | Occupied cell-days | Prior September median | Prior years (n) | Difference |
| --- | ---: | ---: | ---: | --- | ---: |
| MODIS_SP | 23396 | 5819 | 2532.0 | 2020–2023 (4) | +129.82% |
| VIIRS_NOAA20_SP | 101659 | 8809 | 4782.0 | 2020–2023 (4) | +84.21% |

Native-unit differences are diagnostics, not common-grid errors. The prior-year median is sensor-specific; the adjusted estimate is a MODIS-reference comparability measure. Neither identifies unique fires, burned area or ground truth. Two independent holdout years do not support a precise uncertainty interval; none is published. The release presents overlap and does not claim a validated legacy-to-VIIRS transition outside 2020–2024.

Descriptive diagnostics include 0.025/0.05/0.1-degree grids, high confidence using sensor-specific thresholds, platform mix and day/night. These are not independent validation for another AOI. Physical cell area varies with latitude. Swath/cloud observation coverage remains unknown even though daily retrieval is complete. Raw extracts and checksum manifests remain committed; the public app requires no FIRMS key.

Anonymous production HTTPS is verified at https://ember-atlas-opal.vercel.app after CLI authentication resolved the earlier Vercel creation blocker. The full public browser flow and CSV exports passed; see browser-check.json and docs/DEPLOYMENT.md. Official Space Apps resources still return HTTP 503; portal demonstration format must be verified by the Team Owner.
