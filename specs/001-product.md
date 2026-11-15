# Product acceptance contract

English static application with shared Explore, Guided demo, Pitch and Methods & data navigation. Preserve root and existing data/media links; `/`, `/demo`, `/pitch` support direct load, refresh and browser history. No framework migration, authentication or visitor-supplied FIRMS key.

| ID | Acceptance criterion |
| --- | --- |
| P1 Presets | Explore and /demo list Pantanal, Southern Amazon, Cerrado, Gran Chaco, California, Southeastern Australia, Iberian Peninsula and Siberia in that order. Default to Pantanal and September 2024. |
| P2 Scope | Display actual dataset/product coverage, processing class, UTC window, retrieval time and explicit rectangle extent. Selected geography is called a study area, not an official biome. |
| P3 Calendar | Reference-scale sensor-transition replay is the primary Pantanal view. Raw comparison and adjusted-only views remain available; unsupported region/processing/mask disables adjustment. Month selection synchronizes map, comparison, context and exports. |
| P4 Replay | Show January 2023 scenario cutoff and selected month source/adjustment. Reveal observed holdout MODIS with a separate toggle. Per-month source and adjustment appear in calendar/table/CSV. |
| P5 History | Earlier complete matched-domain baseline years, n and values are inspectable. Full available MODIS archive can be selected; missing retrieval is distinct from zero and not converted to calibrated history. |
| P6 Map | Preserve attributed OSM basemap, zoom/pan/scale/fit and accurate local fallback for all eight extents. Show full-data occupied days/cell for a named sensor and optional sampled detections. No spatial relocation or adjusted-point claim. |
| P7 State | Region, SP/NRT, dates, month, sensor, area, view, benchmark and route progress restore from URLs. Stale async requests cannot overwrite another region or re-enable mismatched exports. |
| P8 Evidence | Observation CSV, period aggregates, occupied-day cells, source-tagged replay months and provenance manifest match selected scope. Cells reconcile to grid totals; zero-record retrieved CSV is exportable; missing observation CSV unavailable. |
| P9 Recent | Separate NRT partial-period view with real products/window/last retrieval. No unsupported SP/NRT join or whole-month historical comparison. |
| P10 Validation | Full Pantanal validation is visibly scoped, including the stronger scalar baseline, all residuals and peak-six results. Show seasonal remaining bias; no accuracy/ground-truth/global claim or holdout-based reselection. |
| P11 Pitch | Nine concise interactive sections tell sensor change → continuity replay → observed benchmark → scalar comparison → peak residual → eight-region evidence. Exact demo-state/evidence links, keyboard controls, notes, mobile scroll and readable print. |
| P12 Access | Keyboard focus, native form controls, readable table alternative, touch targets and no document overflow. Desktop map beside comparison; mobile selected-month result before map. Compact introductory copy. |
| P13 Verification | Test all eight bounds, real observations and matching CSV on deployed desktop/mobile; direct loads, refresh, filters, replay cutoff, map fallback, missing/zero and print. Report actual commit and unresolved datasets/calibration gaps. |

## Regional expansion interaction criteria

The selected region's own validation artifact controls adjustment availability. The global evidence card names its region and SP scope, independently of a selected subregion or NRT view. A withheld adjustment leaves raw maps, calendars, historical comparisons and exports usable. External-evaluation months have a textual split label. The UI exposes inner selection, all candidate metrics, independent gate outcomes and fresh monthly residuals. Recent NRT opens on the last seven released UTC days; an explicitly shared date range takes precedence. Large pinned observation shards must pass the same integrity checks as local shards before any metrics or downloads are displayed.

The transition replay requires both source products. Selecting MODIS alone switches to raw MODIS; selecting VIIRS alone switches to its reference-scale view when supported. A single-sensor filter cannot silently export the other sensor as part of a replay. Raw historical takeaway text uses each sensor's own baseline years/sample size and does not attribute the longer MODIS baseline to VIIRS.
