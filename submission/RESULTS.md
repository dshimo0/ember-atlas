# Measured evidence — ember-1

NASA availability was successfully queried on 2026-11-14. The first paired 2024-08-01–2024-09-30 extract completed. Subsequent historical acquisition obtained 514 canonical window manifests and 945,163 deduplicated observations spanning requested windows between 2020-01-01 and 2024-12-31, with substantial gaps. This is not five complete years. See the snapshot manifests for exact successfully retrieved dates. Standard processing only: MODIS_SP (C6.1 Terra/Aqua pooled) and VIIRS_NOAA20_SP (375 m).

Frozen fit: 36 complete paired training months, January 2020–December 2022. Frozen holdout: 2023–2024, of which only January–March 2023 and August–September 2024 are complete paired months. Nineteen holdout months are excluded (missing or partial retrieval). Training seasonal factors (MODIS / VIIRS cell-day totals): Q1 0.5093553, Q2 0.4825479, Q3 0.5538714, Q4 0.4888942.

| Metric, identical five holdout months | Unadjusted common grid | Candidate adjustment |
| --- | ---: | ---: |
| Monthly MAE, occupied cell-days | 1382.20 | 388.02 |
| Signed bias, VIIRS minus MODIS cell-days/month | +1382.20 | −340.53 |

**Calibration unavailable for publication:** numerical improvement does not satisfy the predeclared requirement of 24 matched holdout months across two years. Candidate errors are exploratory partial-holdout evidence. Public adjusted series are null. No confidence interval is supported with two incomplete independent holdout years. There is no measured legacy/VIIRS handoff because no harmonized transition is published.

| Holdout month | MODIS native | NOAA-20 native | MODIS cell-days | NOAA-20 cell-days |
| --- | ---: | ---: | ---: | ---: |
| 2023-01 | 357 | 1583 | 248 | 720 |
| 2023-02 | 147 | 256 | 135 | 167 |
| 2023-03 | 239 | 448 | 201 | 251 |
| 2024-08 | 24224 | 105056 | 5880 | 9247 |
| 2024-09 | 23396 | 101659 | 5819 | 8809 |

Native-unit differences diagnose sensitivity; they are not errors on the common-grid scale. MODIS is a comparison reference, not ground truth. The 0.05-degree grid has latitude-dependent area. Diagnostics JSON includes 0.025/0.05/0.1-degree grids, sensor-specific high confidence, platform and day/night counts. These are descriptive checks, not independent transfer validation. Swath/cloud coverage is unknown; successful empty retrieval means no detections recorded, never proof of no fire.

Acquisition blocker: NASA later returned `Invalid MAP_KEY.` No credential appeared in logs, artifacts or public code. Replacing/reactivating the scoped ingestion secret is required for the remaining holdout windows. Existing downloads are checksum verified and resumable. Public deployment and official portal rule checks are separately pending; see RELEASE-CHECKLIST.md.

September 2024 compared with the three complete prior September values (2020–2022): MODIS median 3,791 cell-days, observed 5,819 (+53.50%); NOAA-20 median 6,893, observed 8,809 (+27.80%). These small, sensor-specific baselines support a descriptive comparison, not a climate trend or causal attribution. The difference between sensor anomalies itself illustrates why native counts should not be spliced.
