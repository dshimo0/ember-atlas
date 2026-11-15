# Guided exploration

Public route: https://ember-atlas-opal.vercel.app/demo

The walkthrough uses the root dashboard's loader, daily summary, observation shards, map, comparison, calendar, baselines and exports. It opens on the full Pantanal study rectangle and September 2024. The header states actual UTC coverage. Five inline steps preserve free exploration; Back, Next, numbered steps and Reset walkthrough are available without a modal overlay.

| Step | Working evidence |
| --- | --- |
| Select area and month | Full/northern/southern presets; selected-month control; dates define calendar and aggregate period |
| Compare common support | MODIS and NOAA-20 VIIRS on the same 0.05° WGS84 / UTC-day basis; native detections remain separate |
| Inspect adjusted VIIRS | Accepted full-area quarterly adjustment and explicit reference-scale history; subregions show the limitation and a full-rectangle action |
| Compare prior years | Each sensor's own fixed-mask same-month median; complete prior years only, at least three; selected/future years excluded |
| Export evidence | Selected-month observations, selected-period aggregates, checksum manifest and share link |

Month, area, product, dates, history view and walkthrough step are represented in URL parameters. Browser refresh and back/forward restore the state. A changed sensor updates calendar, time series, map and both CSVs. Map layer checkboxes change display visibility only, as stated next to the sample disclosure. Pan/zoom also leave the analytical mask unchanged.

Desktop places the map at about 60% of the analytical row, beside the comparison. Mobile stacks the selected-month result, map and comparison, with a collapsible filter toolbar and compact stepper. The month grid wraps to four columns; a monthly source/value table is also available. Charts have text labels, missing gaps and an accessible table. Focus outlines, 44-pixel primary controls, keyboard month navigation and native form controls support keyboard and touch use.

The global validation strip and residuals always describe the full study rectangle, regardless of selected subregion. Regional historical medians are descriptive sensor-specific comparisons; they never inherit a calibration factor. No official biome geometry is implied. OpenStreetMap and Natural Earth are attributed on the map and in Methods & data.

Acceptance evidence: [route checks](../submission/routes-check-public.json), [filter/export checks](../submission/judging-check-public.json), [desktop capture](../submission/demo-desktop.png), [mobile capture](../submission/demo-mobile.png). Mobile checks use browser emulation, not a physical device. The release checklist records deployment and owner gates.
