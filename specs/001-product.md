# Product requirements

The dashboard supports regional review of satellite-observed fire activity in the Pantanal study rectangle, WGS84 `-59,-23,-54,-15`. Released coverage is 2020–2024. Earlier MODIS history, NRT layers, geographic transfer and a calibrated legacy handoff are outside this release.

| ID | Acceptance criterion |
| --- | --- |
| P1 Landing | English title “Pantanal fire activity, 2020–2024,” compact validation result, study-area/sensor/date controls and September 2024 selected. No rhetorical hero or promotional headings. |
| P2 Validation | The percentage is derived from the unchanged unrounded validation metrics. Holdout size, years and full-area geographic scope appear beside it. Detailed factors, bias and limitations are in Methods & data. |
| P3 Layout | Desktop places the interactive geographic map beside the selected-month comparison. Mobile places the map directly after the selected month and its finding. The full calendar follows the dashboard. |
| P4 Map | An attributed OpenStreetMap basemap supplies rivers, settlements and boundaries. Zoom, pan, metric scale and fit-to-study-area work by pointer/keyboard and touch-compatible controls. |
| P5 Fallback | Failed or stalled external tiles activate a locally served Natural Earth map with country boundaries, rivers and settlements. Navigation, FIRMS overlays and exports continue to work. |
| P6 Geometry | The actual study rectangle remains visible and distinct from geographic boundaries. A selected half has its own outline. No biome boundary is shown without verified attributed geometry; the current release omits it. |
| P7 Observations | The sensor legend, active month and sampling disclosure stay beside the map. Up to 4,000 points are shown; exports contain all matching observations. Map pan/zoom do not change the filter scope. |
| P8 Comparison | MODIS, common-grid VIIRS and eligible adjusted VIIRS use occupied cell-days. Native detection counts are separate. The selected-month finding is stated once beside the evidence. Prior baseline years, n and underlying values are accessible. |
| P9 Scope | Full-area factors never apply to a subregion or partial month. The comparison gives a concise reason when adjustment is unavailable. Historical comparisons require three complete prior same-month years. |
| P10 State | Month, area, sensor and selected UTC interval remain synchronized across the map, comparison and observation export. Date controls determine calendar/aggregate coverage. Stale asynchronous responses cannot replace a newer selection. |
| P11 Observation CSV | Located beside the map; covers selected month intersected with dates, area and sensors. Includes coordinates, UTC acquisition time, product/platform, confidence, FRP, original source and snapshot identity. |
| P12 Aggregate CSV | Located beside the calendar; covers the entire selected period with one row per month/product. Includes exact dates, native/grid counts, retrieval status, method, units and eligible adjustment. |
| P13 Missingness | Missing retrieval has blank numeric values and unavailable observation export. Retrieved zero detections are numeric zero; partial months are labeled and receive no adjustment. |
| P14 Calendar | All 60 released months are available, with text labels for training and holdout years, visible/accessible selected states and keyboard month navigation. Mobile months wrap without document overflow. |
| P15 Copy | Plain labels such as Study area, Sensor comparison, Monthly calendar and Methods & data. Limitations appear where they affect interpretation; complete methodology is in details. |
| P16 Reproduction | Original snapshot, validation, frozen split, acceptance rules and export calculations remain unchanged. Locally vendored Leaflet and geographic inputs have licenses/source checksums. No FIRMS credentials are served. |
| P17 Verification | Signed-out desktop/mobile checks cover initial load, zoom/pan/scale/fit, month/area/sensor changes, both CSVs, subregion withholding and forced tile failure. One displayed grid total and downloaded records reconcile with the pinned source. |
