# Pitch: comparable historical fire activity

[Presentation](https://ember-atlas-opal.vercel.app/pitch) · [Explore September](https://ember-atlas-opal.vercel.app/explore?month=2024-09&benchmark=1) · [Guided case](https://ember-atlas-opal.vercel.app/demo) · [Science](https://ember-atlas-opal.vercel.app/methods)

Seven frames use the same versioned observations, replay and evaluation as Explore. Keyboard navigation, presenter notes, mobile scroll and print/PDF are available. The final frame links all eight study areas and the creator. The public PDF is English; native print uses the selected interface language.

This product presentation is separate from official submission media rules, which remain independently unverified. No new human rehearsal is claimed. Earlier nine-frame timing evidence does not apply to this script. Official submission and acceptance of terms remain with the Team Owner.

## Spoken script

### 1. The same Earth.Different sensors.

An analyst comparing seasons needs to understand changes in both activity and instruments. Ember Atlas connects a real Pantanal case, geographic map and historical calendar to source-tagged evidence exports.

### 2. The instrument changeswhat gets reported.

MODIS and VIIRS have different resolution, sensitivity and acquisition times. A native detection count is therefore not automatically comparable across instruments. We retain the raw records, but also count occupied cells on one globally anchored point zero five degree grid per UTC day. Monthly activity sums those cell-days.

### 3. Replay a source change.Keep an observed benchmark.

The replay changes source in January twenty twenty-three, immediately after training ends. It uses observed MODIS beforehand and adjusted VIIRS afterward. MODIS actually continues, so we can reveal its holdout observations as a separate benchmark. Every exported month records the source, adjustment and factor. Missing values stay unavailable.

### 4. Same month.Different reported activity.

September twenty twenty-four has 5,819 MODIS cell-days and 8,809 common-grid VIIRS cell-days. Quarterly adjustment gives 4,879.1, still about sixteen percent below the reference. The comparison supports investigation of measurement differences. It does not identify independent fires or establish ground-truth accuracy.

### 5. Move from place and timeto reproducible evidence.

Start with the selected month in the calendar, then inspect the map and sensor comparison. Region and month selection keep the CSV synchronized. Earlier complete same-month values provide historical context with explicit years and sample sizes. Inspect full grid occupancy or sampled detections, then download observations, aggregates and provenance. Visitors need no API key.

### 6. Lower error.Remaining bias.

All three methods use twenty twenty through twenty twenty-two for training and the same twenty-four separate holdout months. MAE is 1,021.7 raw, 175.3 scalar and 199.7 quarterly. The scalar is stronger there. We retain the frozen method and expose peak errors and bias. Reported MODIS version labels change across the split, limiting sensor-only interpretation.

### 7. Investigate a season.Inspect the evidence.

Today the application provides source-tagged comparisons and independently evaluated local adjustments. Pantanal retains its frozen twenty twenty through twenty twenty-four domain. The nineteen later months are an audit below its extension gate. Usable observation opportunity, homogeneous reference processing and ground truth remain unverified. Recent products stay separate from Standard Processing. We invite a fire-monitoring team to review the seasonal evidence and define an observation-coverage validation pilot. The product, source and methods are public. Diego Shimohama created Ember Atlas for the NASA Space Apps challenge.

Script length: 357 English words. Allow time for navigation and rehearse with a human presenter before calling this a measured three-minute delivery.

## Evidence and likely judge questions

- Why not add counts? Sensors differ in resolution, sensitivity and sampling; raw detections are not deduplicated fires.
- What is harmonized? Complete monthly occupied cell-days on a MODIS reference scale, within each evaluated full-area domain.
- Is MODIS ground truth? No. Agreement and residual error are measured against continuing MODIS observations.
- Why retain quarterly factors if scalar is stronger? The original method is frozen; replacing it needs a separate selection/evaluation protocol.
- What happens at peak activity? The six holdout months selected by observed MODIS activity have scalar/quarterly MAE 404.6/534.6 cell-days/month.
- Is the record 2000–present fused? No. Older observed MODIS is archive context; the January 2023 source change is a replay scenario.
- Does the new backfill validate orbital correction? No. Inputs and independent evidence remain missing; research generation is blocked.

Sources: [methodology](methodology.md), [versioned three-method evidence](../web/data/replay-evaluation-7d4268256831.json), [source and product requirements](../specs/002-data.md), [Marina traceability](../specs/006-marina-challenge.md), [current experience contract](../specs/008-discover-explore.md).
