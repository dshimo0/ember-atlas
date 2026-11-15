# Ember Atlas release review

Public application: https://ember-atlas-opal.vercel.app/ · [Guided demo](https://ember-atlas-opal.vercel.app/demo) · [Pitch](https://ember-atlas-opal.vercel.app/pitch)

Inspected input branch `work`, commit `6fb056e95e11c4a0668e9a73431c0c2f68b76662`. Scientific snapshot: `snapshot-19621fa88d40.json.gz`, uncompressed SHA-256 `19621fa88d408fb5d9aa87482de1bb219e8dd7ed67128c1147d1a63fb087e677`. Validation: `validation-ba55acfc7909.json`. Source/deployment identity and public retest timestamp are recorded in [product-release.json](../submission/product-release.json).

## Findings after implementation and retesting

| Finding | Result | Evidence |
| --- | --- | --- |
| Root map and compact first screen | Preserved and verified; English selected-month finding before map on mobile | judging-check-public.json; desktop/mobile screenshots |
| /demo and /pitch returned 404 | Fixed; shared native modules and static host rewrites | All three direct loads and refreshes in routes-check-public.json |
| Harmonization visible only as one monthly bar | Fixed; explicit adjusted-VIIRS MODIS-reference calendar/time series, raw toggle, source/value table and scope labels | 60-month calendar; referenceRows tests; route checks |
| Subregion history withheld despite available totals | Fixed; independently computed own-mask medians with prior years/n; factors remain withheld | Independent regional daily-total oracle; both subregion checks |
| Aggregate claim obscured residuals | Fixed; MAE/bias/RMSE recomputed from frozen factors; all holdout residuals and worse months exposed | 13 Node tests and immutable validation |
| Navigation and selection not shareable | Fixed; query state, direct refresh, back/forward, shared nav and reset | routes-check-public.json |
| Map overlap and provenance | Circle/diamond shapes, partial opacity, display-only layer toggles and source/time/FRP/confidence tooltips | Signed-out layer checks and desktop/mobile captures |
| Evidence export disconnected from release | Exact CSV hash manifest added; original exporters preserved | Both downloaded CSV hashes reconcile with downloaded manifest |
| Pitch and print | Nine slides, keyboard controls, counter, fullscreen, optional notes and mobile scroll; nine-page PDF | Route suite, pitch screenshots and ember-atlas-pitch.pdf |
| Presentation duration | 454-word script; synthesized read measured 3:05 | pitch-timing.json; human rehearsal pending |
| Official format / eligibility / owner submission | Unresolved | Official pages returned 503; no roster or portal acceptance inferred |

## Scientific evidence

The committed raw-manifest pipeline reproduced the released daily CSV byte-for-byte and validation JSON exactly. No refit or holdout-based method selection was introduced. There are 36 complete paired training months in 2020–2022 and 24 holdout months in 2023–2024. MAE against MODIS is 1,021.7083333333334 → 199.6997313847094 cell-days/month: 80.45433076451603% reduction. Signed bias is +1,021.7083333333334 → −123.96830007041311; RMSE is 1,334.5145965231452 → 317.66603826320306. February and March 2023 have larger absolute residuals after adjustment.

September 2024: MODIS 5,819; VIIRS common grid 8,809; adjusted VIIRS 4,879.0529915213565 cell-days, 16.1531% below MODIS. Prior September medians are 2,532 and 4,782 from four complete 2020–2023 months; native observations are 23,396 / 101,659. MODIS is a comparison reference, not independent ground truth. Retrieval completeness does not establish usable cloud/swath observation coverage.

## Executed acceptance checks

Nine Python tests and 13 Node tests cover pipeline rules, missing/zero, daily aggregation, baseline exclusions, fixed masks, calibration limits, URL parsing and recomputed metrics. Two browser suites exercise fresh signed-out desktop (1440×1000) and touch-enabled mobile (390×844) contexts. They reconcile all default observation records and full-area monthly aggregates with the original snapshot, inspect partial/missing/zero periods, navigate map/calendar/filters, exercise the walkthrough and shared URLs, inspect downloaded manifests, operate pitch controls and count PDF pages. Normal-route checks reject JavaScript exceptions and HTTP errors; separate tile-abort contexts verify local fallback and working exports. Mobile evidence is emulation, not a physical-device claim.

- [Analytical workflow report](../submission/judging-check-public.json)
- [Route/presentation report](../submission/routes-check-public.json)
- [Guided desktop](../submission/demo-desktop.png) / [mobile](../submission/demo-mobile.png)
- [Pitch desktop](../submission/pitch-desktop.png) / [mobile](../submission/pitch-mobile.png)
- [PDF](../submission/ember-atlas-pitch.pdf)
- [Official/source link checks](../submission/resource-check.json)

HTTPS is validated using the system CA store. Browser automation uses independently system-validated leaf-key pins for the Cloud proxy, rather than a global certificate bypass. Production code includes no such flags. Remaining limits are a single validated rectangle, five years, no independent ground truth, no regional calibration, no swath/cloud masks, no seamless source-transition history and no precise confidence intervals. Full owner gates remain in [release-checklist.md](release-checklist.md).
