# Presentation: sensor transition replay

[Live pitch](https://ember-atlas-opal.vercel.app/pitch) · [Exact benchmark state](https://ember-atlas-opal.vercel.app/demo?region=pantanal&view=replay&benchmark=1&month=2024-09&start=2020-01-01&end=2024-12-31) · [Evaluation](https://ember-atlas-opal.vercel.app/data/replay-evaluation.json)

Nine sections follow the sensor change, continuity replay, observed holdout MODIS benchmark, scalar comparison, peak-activity residuals and actual evidence across eight study areas. Charts use the same versioned artifacts as /demo. The world map links to each region; coverage and publication status come from the registry.

Previous/Next, keyboard navigation, slide URLs, optional fullscreen, hidden notes and print/PDF are available. Mobile uses a scroll presentation. The local three-minute target is separate from the official Project Demonstration format, which remains unverified because current official pages return HTTP 503.

Measured synthesized English read: **406 words, 184.1 seconds**, eSpeak NG at 180 wpm, from the actual route notes. This is measured audio duration, not human rehearsal, and excludes navigation. Timing audio is not published. The Team Owner must rehearse and confirm the current official format and eligibility.

## Spoken script

### 1. Ember Atlas

Fire-monitoring analysts need comparable seasonal activity. Ember Atlas replays a satellite-source change in the Pantanal study area. This actual interface opens on September twenty twenty-four, with a geographic map, a source-labeled calendar, sensor comparison and matching evidence exports.

### 2. Different sensors record different activity

MODIS and VIIRS differ in resolution, sensitivity and acquisition time. We aggregate both onto the same globally anchored point zero five degree grid. A cell counts once per product per UTC day; monthly activity sums those cell-days. Native detections, cell-days, independent fires and burned area are different quantities.

### 3. Replay the switch at 2023-01

The replay switches in January twenty twenty-three, after training ends. It uses observed MODIS before the cutoff and frozen seasonal VIIRS on the MODIS reference scale afterward. MODIS actually continues. Its observations remain a separate benchmark. Missing months stay unavailable; the transition date is a scenario.

### 4. Reveal observed holdout MODIS

Reveal that benchmark. September has 5,819 MODIS cell-days and 8,809 unadjusted VIIRS cell-days. The seasonal replay gives 4,879.1, approximately sixteen percent below MODIS. These are sensor-agreement results. Ground-truth accuracy and usable satellite observation coverage remain unmeasured.

### 5. A scalar is a stronger holdout baseline

All three methods fit twenty twenty through twenty twenty-two and use the same twenty-four holdout months in twenty twenty-three and twenty twenty-four. Monthly mean absolute error is 1,021.7 unadjusted, 175.3 for the training-only least-squares scalar, and 199.7 for frozen seasonal factors. The scalar is stronger here; the frozen method stays. MODIS version labels change across the split, limiting sensor-only interpretation.

### 6. Remaining error during active months

Peak activity remains difficult. Rank the six most active holdout months by observed MODIS, never by candidate errors. Scalar peak MAE is 404.6; seasonal MAE is 534.6 cell-days per month. Every residual is inspectable, including months where adjustment is worse.

### 7. Explore the released evidence

Eight explicitly bounded study areas open from this world map. Each has real precomputed source observations, date selection and CSV export. Product-specific coverage is visible. New regional factors require local training and independent evaluation. A factor is never transferred to another region or a smaller mask.

### 8. Inspect sources before extending the series

The older Pantanal MODIS archive remains observed context. Earlier complete comparable months define each historical baseline, with exact years and sample size. New out-of-time evidence is reported separately. Recent NRT stays separate from Standard Processing because current availability provides no same-sensor overlap for evaluating a join.

### 9. Check independent regional evidence

Regional method selection uses twenty twenty-two only, followed by a fixed refit. Outer and fresh periods evaluate that choice; any failed gate withholds adjustment. Pantanal keeps its frozen publication domain. We invite a fire-monitoring team to review the source-tagged comparisons and define an observation-coverage validation pilot.

## Likely judge questions

- **Why retain seasonal factors if the scalar has lower holdout MAE?** The Pantanal method was frozen before that comparison. The observed 2023–2024 holdout is evaluation evidence, not a new selection set. Its 19-month later audit favors seasonal on MAE but does not meet the registered 24-fresh-month extension gate.
- **What is being fitted?** Transparent VIIRS-to-MODIS monthly scale factors, not a fire detector or ground-truth prediction model. The scalar minimizes training squared monthly residuals through the origin; quarterly factors preserve training-quarter totals with a documented pooled fallback.
- **Do factors transfer between areas?** No. New regions require their own inner selection, fixed refit and independent gates. Subregions and NRT do not inherit full-area SP calibration.
- **Is the source transition real?** No. January 2023 is a labeled replay scenario derived from training end. Observed MODIS continues and supplies a separate benchmark.
- **Does a retrieved zero mean no fire?** No. It means no reported detections in the retrieved source window. Usable swath/cloud coverage, independent fire events and burned area are unmeasured.
- **Can NRT and SP be joined?** Current same-sensor availability has zero overlap. Preserve NRT vintages and later retrieve coincident SP windows before independent processing-transition evaluation.
- **What remains for the Team Owner?** Human roster/contributions, rehearsal, current portal/media/eligibility checks, terms and final submission. No completed partnership, interview or operational impact is asserted.

Reported MODIS versions differ across the registered split (6.03 training, 61.03 holdout). The headline measures agreement with the as-delivered reference; isolated sensor effects and processing-vintage continuity remain unverified. The global source-field audit is linked beside the headline and in monthly exports.
