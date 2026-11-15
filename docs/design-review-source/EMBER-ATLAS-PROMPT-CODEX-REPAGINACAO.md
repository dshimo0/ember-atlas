# CODEX: EMBER ATLAS — UX/UI PROFESSIONAL REDESIGN WITH EVIDENCE INTEGRITY

**Context:** Production: https://ember-atlas-opal.vercel.app · public repo https://github.com/dshimo0/ember-atlas · original workspace `C:\Users\dscbe\Documents\Codex\2026-11-13\new-chat\ember-atlas`.

**Act as:** senior geospatial UX architect, frontend designer, visualization engineer, scientific software reviewer and NASA Space Apps submission QA lead.

**NON-NEGOTIABLE:** Implement real improvements, not just a plan. Keep validated data, reproducibility and exports intact. Do not manufacture fire hotspots, validation gains, burns, forecast scores, badges or NASA affiliation. Do not turn an occupied-cell grid into an unlabeled "heatmap". Do not turn sampled observations into full-data densities. Do not move the calibration learned on Pantanal to eight other regions without separate validation.

## STEP 0 — Locate truth before coding
1. Inspect the entire local workspace and AGENTS.md. Read `EMBER-ATLAS-AUDITORIA-UX-UI-2026-11-15.md` alongside repo `specs/001-product.md`, `specs/002-data.md`, `docs/Ember-Atlas-Judging-Review.md`, and release evidence.
2. Run `git status`, `git remote -v`, `git log -5 --oneline`; identify actual frontend root and logo assets. Compare with GitHub `main` and the deployed Vercel project source/commit. **Public GitHub main currently appears to contain Python pipeline + docs only, not frontend.** Resolve provenance without destructive resets or push --force.
3. Take real desktop/mobile screenshots of all pages using Playwright. Audit viewports 1440×900 and 390×844; console/network/ARIA checks; record actual before screenshots and failure cases. Do not treat static HTML "Loading..." placeholders as proof of a production failure until browser checks confirm it.
4. Verify product data contracts, frontend routes and the real contents of `validation.json` / manifests / CSV. Confirm whether `/pitch`, `/methods`, `/demo`, `/about` are proper routes or client-side fallbacks.

## STEP 1 — REDESIGN THE INFORMATION ARCHITECTURE
Top nav `Ember Atlas | Discover | Explore | Guided Demo | Science | Pitch | About`. `/` becomes a low-complexity storytelling homepage; `/explore` owns analytical controls; `/demo` owns guided 4-step journey; `/methods` stays deep scientific evidence; `/pitch` is full-screen presentation. Add usable keyboard/mobile layout. Use real logo from workspace. No fake NASA logo. Label project as independent challenge entry.

## STEP 2 — MAKE THE MAP THE PRODUCT
Desktop 70% viewport map, floating compact left panel (Region, Month, Sensor, Mode, Export), compact on-map legend, bottom expandable calendar/timeline. Mobile: map first, bottom sheet filters. Default on a COMPLETE, verified Pantanal month. Choose visually legible satellite/Blue Marble imagery or an appropriate dark terrain basemap with explicit time/context attribution; dark vector fallback if imagery fails. Preserve map scale, zoom, pan and geographic reference; never use empty gradients instead of geographic evidence.

Map display modes:
1) `Thermal detections` actual positions (sampled marks labeled with subset size; clustering is display-only).
2) `Occupied cell-days` full-data 0.05° WGS84 grid, summed once per product per UTC day; a **discrete choropleth/grid**, not spatial burned area.
3) `Smoothed density` derived from all applicable records, optional and explicitly labeled smoothing, not equivalent to cell-days or fires.
4) `Sensor comparison` MODIS vs NOAA-20 VIIRS in same AOI/time/metric, side-by-side or swipe, same legend scale.
5) `Validated adjustment` only for approved AOI, months and methods. If none passes the frozen rule, show a clear unavailable state and original observations.

Legend MUST show metric, unit, numeric breaks or domain, retrieval/quality status, sample disclosure and zero vs missing vs partial states; fixed scale for comparisons. Sensor-specific native counts must never be added as if deduplicated events.

## STEP 3 — TURN THE CALENDAR INTO A SIGNATURE FEATURE
Build a year × month grid with hover/click, explicit sensor/product, value and unit. Show baseline only with ≥3 prior complete comparable years; mark incomplete windows. Provide a paired sensor story in the same month and a short explanation of the historical gap. Show time series + validation chart below. Do not exaggerate record length beyond actual retrieved data. Make raw-vs-adjusted selector available only where defensible.

## STEP 4 — PAGE-BY-PAGE VISUAL EXECUTION
**Discover**: Cinematic Earth image, official challenge name as informative text, hero copy `THE SAME EARTH. DIFFERENT SENSORS.`, short explanation, CTA `Explore the evidence`, scroll sequence `The problem → How it works → Calendar → Evidence → Open the data`. Use supplied images `ember-atlas-hero-1920x1080.png`, replace temporary typographic wordmark with actual approved logo. No fake burning hotspots on hero. No parallax that ruins performance.

**Explore**: Strong visual map hierarchy, two-level filters, labeled icon controls and loading states with clear failure recovery. All charts from live snapshot. Remove technical dissertations from the visible fold; progressive disclosure via info/drawer.

**Guided Demo**: 4 steps, <90 sec, real stateful controls, replay/reset/skip, deep link to selection, subtitles/text in English.

**Methods**: visual pipeline, data source, adjustment, independent holdout, limitations, reproduce; explain what counts, what doesn't, product/processing versions, zero/missing and attribution. Holdout MAE/bias only from recorded evaluation; preserve failures.

**About**: Editorial mission, human creator and clear author attribution, 8-region atlas **with per-region coverage and validation badges**, technology and open research. Replace DS placeholder with real approved profile image if exists; otherwise premium typographic identity. Correct claims about repository containing frontend until verified.

**Pitch**: 7 full-screen frames, no dense dashboards: sensor issue, NASA data/AOI, common support, observed comparison, interactive calendar, independent validation, useful decisions & limitations. Keyboard navigation, 90-second judge path, export/share. Ensure final official submission media follows current 2026 portal requirements rather than assuming live deck is sufficient.

## STEP 5 — BRAND & COMPONENTS
Independent Ember Atlas brand: Deep Blue `#07173F`, Electric Blue `#0042A6`, Blue Yonder `#2E96F5`, White `#FFFFFF`, Neon Yellow `#EAFE07` as restrained CTA accent; thermal-orange/red only for scientific activity map. Build coherent token-based spacing, font scale and accessibility (minimum 4.5:1 text contrast, ≥44px touch targets). Use one icon set (Phosphor or Lucide), 20–24px with consistent stroke/labels, no tiny unlabeled decorative icons. Avoid generic card overload, giant empty areas, decorative radial gradients that hide geography or imply measurements.

For event logos, follow https://www.spaceappschallenge.org/brand/ and the official guide. Use unmodified NASA Space Apps art; DO NOT use NASA meatball/worm or suggest NASA endorsement. Event: 2026 NASA International Space Apps Challenge · `The Next Frontier` · Nov 14–15, 2026 · Challenge `Harmonization of MODIS and VIIRS Hot Spots` · São Paulo, Brazil. Credit NASA FIRMS data and imagery separately; Earth hero is NASA Blue Marble editorial image, not the observation date.

## STEP 6 — SOCIAL ASSETS AND SEO
Include supplied:
- `ember-atlas-hero-1920x1080.png` (web)
- `ember-atlas-linkedin-1200x627.png` (horizontal LinkedIn)
- `ember-atlas-linkedin-1080x1350.png` (LinkedIn feed portrait)

Ensure actual logo is used instead of placeholder wordmark, edit og:image / Twitter preview / OpenGraph metadata / alt text / descriptions. Test share cards. Never embed a heatmap made of fabricated points in social art; use actual map screenshot from validated release as a second asset if available.

## STEP 7 — TEST & SHIP
- Run screenshots on home, explore, demo, methods, about and pitch on mobile/desktop and compare before/after.
- Validate month/region/sensor consistency with exports, provenance and holdout evidence. Ensure missing/zero/partial distinct.
- Test map tile failover and absent data; check contrast, focus, navigation and controls.
- Run `python -m unittest discover -s tests`, frontend tests/lint/build and Playwright smoke tests, document actual failures.
- Prepare a Git branch, commit reviewed changes and push if configured. Do not overwrite uncommitted local work or deploy to production before tests. Confirm project/commit/target before deploying. Update README architecture and release links, no FIRMS key leaked.
- Produce a short release summary: real changes, proof screenshots, links, measured build/test status and remaining risks. If submission portal requirements are unconfirmed, mark that as pending rather than claiming completion.

**FINAL PASS/FAIL:** New visitor understands the sensor comparability problem in 10 seconds; map has readable geography, layer and legend; calendar is unmistakable and independently inspectable; comparison cannot trick viewers with inconsistent scales; source code/provenance matches production; all public routes work; mobile readable; no invented numbers or official affiliation.

Implement P0 immediately. If time is constrained, sacrifice animation and decorative polish before sacrificing correctness, map usability or submission evidence.
