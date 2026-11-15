# Challenge traceability

Continuation input: branch `work`, release `3e28f40`; the existing eight-region app, /demo and /pitch worked. Static native modules, Leaflet, versioned snapshots and authorized Vercel CLI delivery remain. Release identities and actual public execution are recorded in [transition-release.json](../submission/transition-release.json).

| Requirement | Status and working evidence | Limits / remaining work |
| --- | --- | --- |
| Eight geographic presets | Implemented and publicly verified; all SP/NRT maps, actual bounds and matching CSVs | Study rectangles, not official biome/state masks |
| Matched history and local calibration | Implemented; 79 paired SP months per area; seven local inner choices and all independent gates reproduced from daily evidence | Fixed full-area factors; no transfer to subregions or NRT |
| Transparent three-method comparison | Verified from artifacts and browser recomputation; raw common grid, training-only scalar, quarterly factors; MAE/bias/residuals/peak-six | Existing holdout is evaluation evidence; no post-holdout method switch |
| Sensor transition replay | Implemented and verified; January 2023 scenario, source/factor per month, separate observed MODIS benchmark | MODIS actually continues; reference-version labels also differ across split |
| Reference-scale calendar | Implemented; month drives comparison, map, earlier-only context and exports | No seamless globally fused multi-decade record |
| Historical context | Implemented; complete prior same-month values, actual years/n; no target/future years | Descriptive reported activity; processing-vintage/type effects are not independently removed |
| Full-data spatial occupancy | Verified; all matching records, named product, cell-day sum equals export; sampled detections separate | No adjusted coordinates or burned-area inference |
| Source-field provenance | Implemented; literal version/type per point and monthly export; split audit and source SHA checks | Uniform reference vintage and VIIRS type semantics independently unverified |
| Missingness and recovery | Implemented; retrieved zero differs from missing/partial data and unavailable observation file | Usable swath/cloud coverage remains unknown |
| SP/NRT separation | Verified; captured availability shows zero same-sensor overlap; no join | Preserve NRT vintages; evaluate coincident SP re-extraction when available |
| Earliest MODIS | Verified Pantanal November 2000 start, through July 2026 | Pre-2020 archives outside Pantanal remain an open expansion item |
| Routes and presentation | /, /demo, /pitch; shared state; nine sections, keyboard navigation, eight world-map links and print/PDF | 50 public browser groups passed on source 1018c678; mobile is emulation |
| Demonstration asset | Actual English silent screen capture; anonymous playback and checksum checks | Official Project Demonstration format is separate from the local three-minute pitch |
| Source-version homogeneity | Unverified; exact 6.03 → 61.03 reported-label change is visible and exported | Confirm producer mapping or acquire a demonstrably homogeneous reference before causal attribution |
| Observation opportunity / ground truth | Missing; explicitly excluded from claims | Requires swath/cloud quality data and independent physical validation |
| Biome/custom polygons | Deferred; current masks explicitly bounded and reproducible | A new mask needs recomputation and separate evaluation |
| Official portal rules / submission | Owner action; official challenge/resources checks returned 503 | Owner confirms eligibility, media, roster, terms and final submission |

## Published coverage

<!-- COVERAGE:START -->
| Study area (W/S/E/N) | Observed SP coverage | Recent NRT UTC window | Adjustment |
| --- | --- | --- | --- |
| Pantanal (-59, -23, -54, -15) | MODIS_SP: 2000-11-01–2026-07-31 (9404 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2026-07-31 (2404 retrieved days) | MODIS_NRT: 2026-09-01–2026-11-14 (75 retrieved days); VIIRS_NOAA20_NRT: 2026-08-01–2026-11-14 (106 retrieved days) | Evaluated full area, SP 2020–2024 only |
| Southern Amazon (-65, -13, -48, -5) | MODIS_SP: 2020-01-01–2026-07-31 (2404 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2026-07-31 (2404 retrieved days) | MODIS_NRT: 2026-09-01–2026-11-14 (75 retrieved days); VIIRS_NOAA20_NRT: 2026-08-01–2026-11-14 (106 retrieved days) | Evaluated seasonal, full area SP through 2026-07-31 |
| Cerrado (-55, -20, -44, -8) | MODIS_SP: 2020-01-01–2026-07-31 (2404 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2026-07-31 (2404 retrieved days) | MODIS_NRT: 2026-09-01–2026-11-14 (75 retrieved days); VIIRS_NOAA20_NRT: 2026-08-01–2026-11-14 (106 retrieved days) | Evaluated seasonal, full area SP through 2026-07-31 |
| Gran Chaco (-66, -32, -57, -17) | MODIS_SP: 2020-01-01–2026-07-31 (2404 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2026-07-31 (2404 retrieved days) | MODIS_NRT: 2026-09-01–2026-11-14 (75 retrieved days); VIIRS_NOAA20_NRT: 2026-08-01–2026-11-14 (106 retrieved days) | Evaluated seasonal, full area SP through 2026-07-31 |
| California (-125, 32, -114, 42.5) | MODIS_SP: 2020-01-01–2026-07-31 (2404 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2026-07-31 (2404 retrieved days) | MODIS_NRT: 2026-09-01–2026-11-14 (75 retrieved days); VIIRS_NOAA20_NRT: 2026-08-01–2026-11-14 (106 retrieved days) | Evaluated seasonal, full area SP through 2026-07-31 |
| Southeastern Australia (140, -44, 154, -28) | MODIS_SP: 2020-01-01–2026-07-31 (2404 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2026-07-31 (2404 retrieved days) | MODIS_NRT: 2026-09-01–2026-11-14 (75 retrieved days); VIIRS_NOAA20_NRT: 2026-08-01–2026-11-14 (106 retrieved days) | Evaluated seasonal, full area SP through 2026-07-31 |
| Iberian Peninsula (-10, 35, 4, 44.5) | MODIS_SP: 2020-01-01–2026-07-31 (2404 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2026-07-31 (2404 retrieved days) | MODIS_NRT: 2026-09-01–2026-11-14 (75 retrieved days); VIIRS_NOAA20_NRT: 2026-08-01–2026-11-14 (106 retrieved days) | Evaluated seasonal, full area SP through 2026-07-31 |
| Siberia (60, 50, 140, 72) | MODIS_SP: 2020-01-01–2026-07-31 (2404 retrieved days); VIIRS_NOAA20_SP: 2020-01-01–2026-07-31 (2404 retrieved days) | MODIS_NRT: 2026-09-01–2026-11-14 (75 retrieved days); VIIRS_NOAA20_NRT: 2026-08-01–2026-11-14 (106 retrieved days) | Evaluated seasonal, full area SP through 2026-07-31 |
<!-- COVERAGE:END -->

## Regional evaluation

<!-- REGIONAL-EVALUATION:START -->
| Study area | Inner choice | Outer MAE: raw → choice (n) | Fresh MAE: raw → choice (n) | Fresh signed bias | Published adjustment |
| --- | --- | ---: | ---: | ---: | --- |
| Pantanal | seasonal | 1,021.7 → 199.7 (24) | 399.4 → 70.8 (19) | 67.4 | frozen seasonal through 2024-12-31 |
| Southern Amazon | seasonal | 4,584.5 → 567.5 (24) | 1,428.4 → 168.7 (19) | 61.5 | seasonal through 2026-07-31 |
| Cerrado | seasonal | 3,826.8 → 506.5 (24) | 2,641.7 → 322.1 (19) | 116.5 | seasonal through 2026-07-31 |
| Gran Chaco | seasonal | 3,941.8 → 405.8 (24) | 2,923.7 → 213.9 (19) | 97.5 | seasonal through 2026-07-31 |
| California | seasonal | 945.1 → 124.1 (24) | 977.7 → 146.0 (19) | 124.9 | seasonal through 2026-07-31 |
| Southeastern Australia | seasonal | 1,453.3 → 228.9 (24) | 1,604.0 → 147.8 (19) | 13.8 | seasonal through 2026-07-31 |
| Iberian Peninsula | seasonal | 738.9 → 71.5 (24) | 794.6 → 123.0 (19) | -72.8 | seasonal through 2026-07-31 |
| Siberia | seasonal | 5,521.3 → 824.5 (24) | 5,080.4 → 850.0 (19) | 303.9 | seasonal through 2026-07-31 |

Units: occupied cell-days/month; full named study rectangle, SP only. Inner choice uses 2022 after fitting 2020–2021; refit uses 2020–2022. Outer: 2023–2024, including the previously published September 2024; the artifact also reports the sensitivity excluding that month. Fresh: January 2025–July 2026, excluded from fitting and selection. Pantanal retains the original publication regardless of the new audit. A failed regional gate withholds adjustment. MODIS is the comparison reference, not ground truth.
<!-- REGIONAL-EVALUATION:END -->

## Creator and About page

The owner confirmed **Diego Shimohama** as the sole creator. `/about` is linked from every shared header and the final pitch section. Public direct loads/refresh, keyboard navigation, desktop/mobile widths, browser-back analytical state and no-JavaScript rendering passed. [Executed About release](../submission/about-release.json) records the source and deployment. No additional members, professional credentials or partners are asserted. The supplied emblem preview has no accessible original asset in the workspace; it has not been substituted or published.

## P0/P1 presentation release

Shared navigation now includes a dedicated `/methods` route. The legacy methodology anchor remains compatible. Five guide scenes reuse the existing analytical components; compact heatmap labels, explicit intensity and progressive scientific detail improve exploration. Pitch opening/closing use credited NASA editorial imagery; all three candidate metrics, peak error, reference-version limits and publication domains remain visible in the evidence path. Mobile navigation, touch targets, world-map semantics and scroll progress have explicit regression checks. See [experience-redesign.md](experience-redesign.md) for actual execution status.

## P2/P3 visual release

The owner chose deeper presentation, not expanded science scope. Eight dated NASA true-color context cards link to the existing regional evidence; the pitch adds nine-section direct navigation. Local licensed typography and reduced-motion behavior improve readability without changing validation, data coverage or export calculations. See [visual-refinement.md](visual-refinement.md) and the executed `submission/visual-release.json`. The requested Windows-only backfill folder is unavailable here and remains an open review item pending accessible files.

## Evidence workspace and bilingual presentation

Actual holdout scatter, three-method residuals, interactive monthly history and common-axis selected-month comparison expose the existing evidence. Light/dark and EN/PT-BR settings support exploration without changing analytical state or raw exports. Public verification: `submission/workspace-release.json`. Canonical scientific artifacts and English submission materials remain authoritative. Portuguese domain review, physical devices and inaccessible owner backfill files remain open checks.

## Marina and continuity requirements

The timestamped owner-supplied video transcript is mapped in [spec 006](../specs/006-marina-challenge.md). Calendar-first acceptance and experimental publication gates are in [spec 007](../specs/007-calendar-backfill.md). Historical continuity remains partial: observed archive context and evaluated replay are available, but a validated 2000–present multi-platform fused series is not claimed. Backfill source Parquets/manifests and audiovisual verification remain open.

## Discover / map-first delivery

Spec 008 supersedes the calendar-first route composition following owner approval. Discover explains the sensor problem; Explore retains the common-grid/replay workflow and reproducible exports. Methods remains `/methods` under the Science navigation label. Four guide scenes and seven pitch frames preserve the held-out comparison, stronger scalar baseline, bias and peak limitations. Smoothed density and swipe remain deferred to separately tested cartographic work. Source/artifacts stay unchanged.

## Owner feedback and supplied guidance, 2026-11-15

Spec 009 tracks the 20 annotated presentation/map comments. Map base selection is visible; occupancy has an absolute day scale; calendar cells name their sensor; shared comparisons are zero-based bars. Methods expose counting/evaluation equations and monthly residual evidence. The pitch embeds a real product recording and retains a static product view in its seven-page PDF. Public `/credits.html` and `/ai-disclosure.json` expose attribution and AI assistance.

The owner-supplied guide and Pitch101 specify <=7 slides or <=30 seconds, English and publicly accessible links. The live guide URL returned 503 on this review. The winners PDF is generated commentary, not verified winner research. Logo/photo originals and logo provenance remain outstanding; no substitute was fabricated. Terms, team-event eligibility and final submission are owner actions.
