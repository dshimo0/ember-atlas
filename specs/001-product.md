# Product acceptance contract

English static application with shared Explore, Guided demo, Pitch and Methods & data navigation. Preserve root and existing data/media links; `/`, `/demo`, `/methods`, `/about`, `/pitch` support direct load, refresh and browser history. No framework migration, authentication or visitor-supplied FIRMS key.

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

Source flags are one click from the selected comparison and present in observation tooltips and exports. Literal version strings and reported type counts are labeled as source metadata. Counts by type describe native detections, not additive grid-cell-day contributions. Observation loading/network failure leaves map occupancy unavailable rather than zero, while aggregate exports and a provenance manifest remain usable.

## About the team

`/about` identifies Diego Shimohama as the sole creator, as confirmed by the owner. Main navigation and the final pitch section link to it. The creator card links to the owner-provided personal website, https://dshimo.vercel.app/, alongside GitHub and the project repository. The page has direct-load/refresh support, keyboard-accessible links, responsive layout and source/data credits. It makes no claim of additional members, credentials, partners or NASA affiliation. About content remains readable without JavaScript or loading analytical snapshots. Adding a supplied visual requires its original accessible asset; no substitute logo or portrait is fabricated.

## P0/P1 experience redesign

- P14 Navigation: primary links are Explore, Guided demo, Methods & data, About, Pitch. Mobile header height follows wrapped content; tap targets cannot overlap the page title. Direct `/methods` and legacy `/#methodology` preserve analytical selection.
- P15 Guided journey: five source-backed scenes explain place, history, instruments, adjustment and evidence. Progress precedes the workspace; named steps, Previous/Next, keyboard arrows, restart, independent exploration and methods links are available. The same calendar moves into the historical scene; no independent calculation tree or synthetic measurement is introduced.
- P16 Progressive detail: Explore opens on map/month/comparison, with extra filters and validation detail disclosed on demand. Scientific detail restores through `detail=scientific` and exposes existing metadata, tables and validation.
- P17 Calendar: activity intensity is derived from the maximum currently displayed value, with a labeled scale. Compact display rounds numerical labels only; full export precision remains unchanged. Zero, unavailable, partial and unsupported adjustment retain distinct semantics.
- P18 Methods: a separate experience presents acquisition, verification, aggregation, training-only adjustment, independent evaluation and historical context. Source dates come from the same selected registry entry; MAE, bias, residuals, factors, source flags and manifests remain inspectable.
- P19 Pitch: nine sections use the same release artifacts, opening/closing editorial imagery, actual selected-month evidence, all three candidates and remaining peak error. Desktop uses a 16:9 stage; mobile scroll updates slide counter, navigation and URL. The regional map uses group semantics with individually accessible links.
- P20 Imagery: local NASA editorial assets have source URLs, SHA-256, date/context and credits. Blue Marble is labeled a 2007 composite; the Pantanal true-color image is dated 2024-09-01 and never overlaid with synthetic detections or represented as the monthly metric. Other regions do not inherit Pantanal imagery.
- P21 Verification: capture all five experiences at 375, 768 and 1440 px, all guide scenes, pitch evidence/closing, and a nine-page PDF. Test the audited navigation, number overflow, touch targets, semantic and scroll-progress defects, plus the established eight-region data/export suite. Automated accessibility checks do not establish complete WCAG conformance.

## P2/P3 visual refinement

- P22 Typography: self-host licensed Manrope with system fallback and `font-display: swap`; keep numerical evidence tabular and readable. Font failure cannot hide text or controls. Exports and metrics remain unchanged.
- P23 Motion: brief feedback on navigation, focus and selected guide/pitch scenes; no autoplay, looping decoration, animated map measurements or delayed access. Reduced-motion mode disables transitions and animations. Print is static.
- P24 Regional visual context: About contains eight dated NASA true-color study-area cards in registry order. Images have source links, SHA-256, explicit bounds and date; imagery is contextual and never a fire-activity metric or biome geometry. Each card links to the corresponding real Explore state.
- P25 Presentation navigation: a labeled nine-section rail reflects the same pitch state and supports direct section selection, keyboard focus, mobile overflow within the rail and print exclusion. The pitch scroll callback cannot restore a pitch URL after Explore navigation begins.
- P26 Verification: review actual desktop/mobile captures, reduced-motion and font-failure states, eight gallery links and image hashes, section navigation, nine-page print and unchanged scientific output. Local Windows-only backfill material requires an accessible copy before review; no inferred inventory or data integration.

## Evidence-first redesign and bilingual presentation

- Map-dominant analytical composition, with selected-month evidence and time-series selection using the existing shared state.
- Quantitative time series with axes, missing-data gaps, selectable months and replay cutoff; holdout scatter with identity line and three-method residual diagnostic from existing validation rows.
- Explicit dark/light appearance and English/Português (Brasil) controls, persistent locally; English remains initial/default submission language. Scientific source identifiers, raw artifacts and CSV schema remain canonical English. Translation must not change numbers, factors or data scope.
- Responsive analytical and editorial layouts; both themes need readable controls, chart labels, map attribution and print. User visual preferences are independent of analytical filter state.

## Calendar-first continuity

Explore and Guided demo prioritize the selected month, takeaway and monthly calendar before the map/comparison. Activity/anomaly encoding restores from URLs. Time series and monthly source table are expandable. See [spec 007](007-calendar-backfill.md) and [Marina traceability](006-marina-challenge.md). This supersedes earlier map-first ordering criteria.
