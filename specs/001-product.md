# Product requirements

An environmental analyst selects an area and date range, sees burning activity by month and year, and downloads the observations behind the analysis.

| ID | Acceptance criterion |
| --- | --- |
| P1 | A bounding box or preset and a UTC date range filter every view and export consistently. First preset is a Pantanal demo rectangle, explicitly labeled as approximate. |
| P2 | A calendar shows historical seasonality, highest activity months, and the selected month against a same-month historical median. Missing periods render separately from zero recorded detections. |
| P3 | A comparison view shows MODIS and VIIRS raw counts, occupied cell-days and, after validation, the harmonized series. Processing level and sensor transitions are visible. |
| P4 | CSV export includes coordinates, acquisition time, platform, product, confidence, FRP where present, and source provenance. An aggregate export includes metric, method version and coverage status. |
| P5 | A documented command rebuilds the demo from a pinned data extract. The web app runs without a FIRMS key in the browser. |
| P6 | The historical view aims to extend from the early 2000s to the latest available standard product. Recent NRT observations are provisional and labeled separately. |

Hotspots represent satellite detections of thermal anomalies. A detection can come from agricultural burns and other heat sources. Coverage and cloud limitations must be visible where relevant.

## Snapshot UI acceptance (2026-11-14)

Use the name Pantanal study area for the approximate rectangle. A static English dashboard provides north/south subwindows, UTC range and month selection, sensor comparison and selected-month observation export. Require three complete prior same-month years for an unadjusted sensor-specific median. With no snapshot, show Data unavailable and disable export. No synthetic observations enter the public build. Calibration display remains gated pending real evidence and full diagnostics. Aggregate export, calibrated view, and real-data browser acceptance remain open.
