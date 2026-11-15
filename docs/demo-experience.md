# Sensor transition exploration

Default: https://ember-atlas-opal.vercel.app/demo?region=pantanal&view=replay&month=2024-09

The primary Pantanal calendar and time series replay observed MODIS before January 2023 and frozen seasonal VIIRS afterward. The cutoff is a scenario. Toggle observed holdout MODIS as a separate benchmark; select December 2022 and January 2023 to verify the source change. Each month/table/CSV retains source and adjustment. The selected-month comparison remains real sensor evidence.

The ordered eight-region selector loads immutable source-specific SP or separate NRT snapshots. Full available archive selection exposes older MODIS and missing periods. Dates bound the calendar/period export, while the selected month bounds observations and map cells. Area/sensor/month/processing changes use the same mask and invalidate stale asynchronous responses. URLs preserve the complete selection and benchmark state.

The map retains OSM, attribution, pan/zoom/scale/fit and a global local Natural Earth fallback. Its primary analytical layer uses all observations for occupied UTC days/cell and a named sensor. Optional sampled detections and sensor visibility controls are under Map inspection layers. They affect display only. Cells and observations have separate CSVs; cell occupancies sum to common-grid totals. Monthly factors never modify spatial coordinates or occupancy.

Reference-scale historical context uses complete earlier same-month entries in the matched 2020–2024 domain, with n/years/source exposed and a minimum of three. Older MODIS is observational context. Missing, partial and zero retrieval states remain distinct; NRT is not joined to SP or compared against entire historical months.

The five inline exploration steps remain available after the analytical row. Free exploration and reset remain available. Mobile uses compact region/data controls, collapsible detailed filters and a readable month/table alternative. Independent full-area validation stays clearly labeled as Pantanal evidence when another study area is selected.

Verification: submission/eight-region-check-public.json records desktop/touch-emulated mobile direct loads, refresh, all eight geometries/observations/CSVs, SP/NRT separation, replay cutoff, filter state, cell reconciliation and forced tile fallback. No physical-device verification is implied.
