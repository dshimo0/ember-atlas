# Presentation: sensor transition replay

[Live pitch](https://ember-atlas-opal.vercel.app/pitch) · [Exact benchmark state](https://ember-atlas-opal.vercel.app/demo?region=pantanal&view=replay&benchmark=1&month=2024-09) · [Evaluation](https://ember-atlas-opal.vercel.app/data/replay-evaluation.json)

The nine sections tell one story: differing sensors; a January 2023 source-change scenario; observed MODIS as the independent fitting-period holdout reference; the stronger scalar baseline; remaining peak-activity error; and actual evidence across eight study areas. Figures are generated from the same immutable registry, original validation and replay evaluation used by /demo. The world map links to each Explore selection and displays its observed SP evidence.

Previous/Next, arrow keys, slide URLs, optional fullscreen and hidden presenter notes work on desktop. Mobile presents sections in reading order and restores a selected slide on refresh. Print styling generates a nine-page landscape deck. Neither the nine slides nor the local approximately three-minute target is asserted to satisfy the official Project Demonstration format. Current official guide and human rehearsal remain owner checks.

Measured script timing: 444 words; synthesized English read at 180 wpm: **187.8 seconds**. This is measured synthesized audio duration, not human delivery, and excludes navigation. No timing audio is published. Human rehearsal and official format verification remain pending.

## Spoken script

### 1. Ember Atlas

Ember Atlas replays a change of satellite source in the Pantanal study area. We use observed MODIS before January twenty twenty-three and adjusted VIIRS afterward. MODIS actually continues through the holdout. We retain it as a separate benchmark to inspect its residual.

### 2. Different sensors record different activity

MODIS and VIIRS have different resolution, sensitivity and acquisition times. Native hotspot counts are not directly interchangeable. Both products are placed on the same globally anchored point zero five degree grid. A cell counts once per product per UTC day; monthly activity sums those cell-days. This metric is not burned area or a count of independent fires.

### 3. Replay the switch at 2023-01

The source changes at the start of the holdout, after the training period ends. The reference-scale calendar identifies the source and adjustment for every month. Before the cutoff it uses observed MODIS. Afterward it uses the frozen seasonal adjustment. Missing or incomplete periods remain unavailable. This scenario does not claim an actual MODIS service cutoff.

### 4. Reveal observed holdout MODIS

Reveal observed MODIS after the cutoff. September twenty twenty-four shows the sensor counts and the seasonal replay together. The replay remains sixteen point two percent below MODIS. This benchmark was excluded from fitting; independent ground-truth accuracy remains unmeasured.

### 5. A scalar is a stronger holdout baseline

All three methods use identical training and holdout months. Unadjusted monthly mean absolute error is 1,021.7 cell-days. A single training-only least-squares scalar gives 175.3. The existing seasonal factors give 199.7. The scalar is better on this evaluation. We report that result and retain the frozen published method; selecting a replacement requires separate evaluation.

### 6. Remaining error during active months

We stress-test the six holdout months with greatest observed MODIS activity. Selection uses reference activity, not residuals. Peak-month MAE is 404.6 for the scalar and 534.6 for the seasonal method. All monthly residuals remain downloadable, including worse months.

### 7. Explore the released evidence

Eight project-defined study areas open with real precomputed observations. The seven added regions have a matched September twenty twenty-four Standard Processing window; all eight have a separate recent NRT window. The world map links to each selected area. These are explicitly bounded study rectangles. Only the Pantanal has evaluated adjustment factors.

### 8. Inspect sources before extending the series

The Pantanal MODIS backfill extends the observed record to its verified earliest retrieval. Coverage is product-specific, and missing retrieval is distinct from recorded zero. Historical comparisons use earlier complete comparable months. NRT is a separate partial-period view; joining it to Standard Processing requires overlap and quality evaluation. Source-tagged monthly CSVs and checksums support reproduction.

### 9. Verify the next region before calibration

The next scientific step is independent regional evaluation. Each new region needs matched multi-year observations, local training and held-out evaluation before any adjusted series is enabled. Future method selection needs new outer evaluation data. The working product, exact replay state, source and evidence are linked. The Team Owner must confirm human contributions and current submission requirements.

## Likely scientific questions

- **Is this an actual sensor shutdown?** No. It is a replay scenario within observed overlap. MODIS continues and is explicitly shown as a benchmark after the January 2023 cutoff.
- **Why retain seasonal output when the scalar is better?** The scalar baseline improves holdout MAE to 175.3 versus seasonal 199.7 cell-days/month. This is disclosed. The existing holdout is evaluation evidence; selecting a replacement now requires a separate protocol and outer evaluation.
- **What happens at peaks?** The six highest observed MODIS holdout months have scalar MAE 404.6 and seasonal MAE 534.6. They were selected using reference activity, never residuals. All residuals are inspectable.
- **What was knowable then?** Calibration uses only 2020–2022. Replay baseline entries are earlier complete same-month values in the paired evaluation domain; target/future years are excluded. Older MODIS is archive context, not extra calibration evidence.
- **Are all regions harmonized?** All eight have real observed maps and exports; only the evaluated full Pantanal area has adjusted output. Seven regions still need multi-year overlap and local independent evaluation.
- **Can recent NRT be appended?** It is currently separate. A join requires matched processing revisions, masks/windows, duplicate handling and independent SP/NRT transition evaluation.
- **Does the map show adjusted locations?** No. It shows observed occupied days/cell, or an optional sample of actual detections. Monthly scale factors apply to monthly activity only.

Roster, current official submission/media requirements, eligibility, human delivery timing and final portal submission remain Team Owner actions. No fabricated interviews, savings, partnerships or ground-truth accuracy are claimed.
