# Scientific and product release review

[Explore](https://ember-atlas-opal.vercel.app/) · [Replay](https://ember-atlas-opal.vercel.app/demo?region=pantanal&view=replay&benchmark=1&month=2024-09&start=2020-01-01&end=2024-12-31) · [Pitch](https://ember-atlas-opal.vercel.app/pitch)

The continuation preserves branch `work`, the existing static/Leaflet stack and every original frozen scientific file. [Release identity](../submission/transition-release.json) records the tested source/data commits and actual deployment. Documentation is not used as implementation proof.

| Finding | Current implementation | Executed / pending evidence |
| --- | --- | --- |
| Seven areas had one SP month | All eight now have 79 complete paired SP months; Pantanal MODIS extends to November 2000 | Full snapshot/native/grid/type/version reconciliation; current coverage inventory |
| Calibration could leak between masks | Each new region has its own registered inner choice and fixed refit; all three independent gates passed | Protocol and regenerated regional artifacts; subarea/NRT withholding checks |
| Scalar comparison could be hidden | All three candidates and every residual remain visible, including stronger alternatives in some evaluation periods | Artifact/browser metric reconciliation; no outcome-based method switch |
| Implicit source continuity | Explicit January 2023 replay and actual continuing MODIS benchmark | Cutoff fields/CSV, URL restoration and benchmark toggle |
| Source metadata was lost in normalized rows | Literal version/type restored from original CSVs, preserving all original fields and counts | SHA/identity joins; 25 Python tests; source-field verification artifact |
| Uniform reference label was not established | Training reports 6.03, holdout/fresh 61.03; split audit is beside the headline | Native counts by label and split; physical vintage homogeneity remains unverified |
| Thermal records could be read as fire events | All reported types remain in the frozen metric; source flags and native counts are accessible | Point CSV/tooltips, monthly source fields; independent classification remains unavailable |
| Loading failure could resemble zero | Unavailable observation files leave occupancy blank/unavailable; aggregates and provenance remain usable | Forced-shard-failure browser check, distinct from actual retrieved zero |
| Maps and exports could diverge | Shared region/mask/UTC/product filters; full-data occupied days/cell | Point identity, row counts, cell sums and CSV/manifest hashes |
| World-map SVG links were fragile | Native href extraction supports SVG keyboard activation | All eight links exercised on desktop/mobile |
| First screen was crowded | Compact header/controls; selected result precedes map on mobile; geography and comparison share desktop row | Desktop/mobile screenshots and first-viewport map measurement |
| Pitch lacked evidence | Same frozen figures, eight-area coverage/status, all candidate results, peak residuals and source-version qualification | Keyboard/direct loads, nine-page print and actual recording |

Pantanal remains 80.5% lower MAE versus unadjusted common-grid VIIRS on 24 holdout months: 1,021.7 → 199.7. The scalar is stronger there at 175.3. September 2024 seasonal output is 4,879.1 versus MODIS 5,819, 16.2% below the reference. The 19 fresh months give raw/scalar/seasonal MAE 399.4/89.7/70.8; seasonal bias +67.4. The original 2020–2024 publication domain remains unchanged.

[Regional results](../submission/regional-evaluation.md) record each area's distinct fit and actual gates. All are agreement against the MODIS_SP archive as delivered, not ground-truth accuracy or isolated sensor effects. Source labels change across the split; all reported thermal types remain included. Current source-vintage interpretation, usable observation opportunity, pre-2020 history outside Pantanal, physical-device testing and human rehearsal remain open.

Full archive reconciliation covers 16 region/processing datasets and all eight regional evaluations. Public workflow results must be checked in the current executed report after deployment. Official pages returned HTTP 503; media-format/eligibility/roster/terms/final submission remain Team Owner actions. No winning, operational-impact or partnership claim is made.

Production verification: source `1018c678d7be5efb97efce5aaf221e155c6a8e24`, deployment `dpl_fuwGKU7pkWJASYCuEaUXCVkwPj3i`, registry `c06212509a51`; 50 public desktop/mobile browser groups passed across all eight SP/NRT views and January 2025 historical shards. All 16 datasets and eight evaluations were reconciled. Three direct routes, public media and registry bytes match the release; initial map placement was measured on desktop/mobile. Python: 25 passing tests; JavaScript: five passing modules; both PR CI workflows passed. [Executed report](../submission/transition-release.json) records evidence and remaining limits.

## P0/P1 experience follow-up

The subsequent visual audit confirmed numerical overflow, mobile navigation overlap, a buried guide, an anchor-only methodology section, stale mobile pitch progress, undersized detail targets and interactive-SVG semantics. The redesign addresses these with compact labels, a reflowing shared header, five early guide scenes, dedicated `/methods`, scroll-aware pitch state, minimum touch targets and grouped SVG links. About and Pitch use credited, dated NASA imagery; no measurement is fabricated. Scientific code and data remain unchanged. See `submission/experience-release.json` for the actual tested source and public acceptance results; do not infer verification from this description alone.

## P2/P3 presentation follow-up

Self-hosted typography, optional brief transitions, a dated eight-area NASA context atlas and a direct pitch section rail extend the prior fixes. Imagery retains visible clouds/swath gaps and is explicitly separate from monthly thermal activity. Exact queries, extents and hashes are public. Executed evidence is recorded in `submission/visual-release.json`; unavailable Windows backfill material is not claimed as reviewed. Physical-device and assistive-technology checks remain unresolved.

## Evidence-first composition and bilingual interface

The next revision replaces progress-style selected-month bars with a shared-axis dot plot, brings actual holdout scatter and three-method residuals to the Methods introduction, and makes monthly time-series marks select the existing application month. Explore gives the map more width; the guide introduces the same evidence with a compact rail. The pitch now shows a residual time series rather than only three summary bars. About presents the eight dated geographic images at readable scale.

Dark/light and EN/PT-BR controls are available across routes. English remains the submission reference and original artifacts/export schemas remain canonical. Translation is presentation-only, with byte-identical observation exports checked across languages. Public execution identity is recorded in `submission/workspace-release.json`. Human Portuguese scientific copy review and physical-device checks remain visible limitations.

## Calendar continuity revision

Calendar-first layout and shareable activity/anomaly colour modes reuse released observations. Backfill review exposed unverified inputs and unsupported intervals; generators are blocked and no experimental result is deployed. Current run evidence is recorded in submission/calendar-continuity-check.json. Translation and physical assistive-technology review remain separate checks.

## Discover and map-first revision

The new home has an attributed NASA Earth image, live observed comparison, real monthly calendar links and artifact-derived validation. `/explore` separates analytical controls from the entry narrative; legacy root selection links migrate. Before/after captures and executed route/state/accessibility checks are stored under `submission/discover-*`. Original social/hero artwork and approved logo files are absent; no invented substitute or NASA endorsement is used. Official portal rules, human Portuguese copy review and physical assistive-technology checks remain unresolved.

Verified deployed source: `4cc39d2a8e2b6307f0abb0be76402e91f5b9a5af`. The static-root precedence issue was reproduced and fixed by serving Discover from `index.html` and analytical routes from `workspace.html`. Anonymous route refresh, migrated state, real CSV matching, all eight bounds, separate NRT, local tile recovery and targeted automated accessibility passed. See `submission/discover-release.json`. Visual screenshots are recorded; no claim of measured judge comprehension or human assistive-technology conformance is made.

## Annotated review revision — spec 009

Owner comments 1/8: cryptic calendar glyphs removed; full product labels and exceptional coverage text. 2: basemap selector moved above map, attributed satellite option added, occupied-day cells use stronger colours at fixed absolute days. 3/5/6/7: decorative Earth opening replaced by actual product capture, counting explanation, month/year headings and comparative MAE chart. 4/17/19: common zero-based bars and full-sized error comparison. 9/15: labeled progress controls. 10–14: equations, visible scientific methods, monthly evidence retained; redundant tiny residual chart hidden. 16: product definitions presented as a measurement table. 18: product playback inside the slide and PDF still. 20: concrete pilot purpose, creator, limitations and public URL.

These are implemented changes, not a claim of subjective design acceptance. Logo/photo originals remain unavailable as filesystem attachments. Scientific source artifacts and model fitting are unchanged. Fresh verification is recorded in `submission/refinement-release.json` when completed.

Verified production source: `d3ac2d0c9305829cd93a07d7a735620fdcd0b31b`, Vercel `dpl_4xPNeCDkFZRmhDra8RCBEre5AoS4`. Twelve anonymous route/refresh cases plus two selection/export flows passed; six light/PT layout checks passed. Satellite and forced local fallback passed on desktop/mobile, with September CSV 125,055 rows. Fifteen public routes/assets match deployed bytes. 26 Python tests and six Node modules passed. Selected axe rules found zero violations; this does not certify full accessibility. Seven English PDF pages, fourteen EN/PT frame-fit checks, actual silent capture 27.466667 seconds. Frozen models/data unchanged; credential scan found no patterns and checked the configured key. Logo/photo originals and human/submission review remain open.
