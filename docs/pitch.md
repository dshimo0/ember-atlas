# Pitch: evidence across changing sensors

[Seven-page English PDF](https://ember-atlas-opal.vercel.app/assets/ember-atlas-pitch.pdf) · [Presentation](https://ember-atlas-opal.vercel.app/pitch?lang=en)

The owner-supplied submission guide permits seven slides including title/intro, or a video of at most 30 seconds. The online guide returned 503 during review. This deck uses seven sections; the product section plays a real recording inline and prints an actual workspace still. English is the submission version. Team Owner confirms current portal rules, event eligibility and terms.

## Spoken script

### 1. Fire history across changing sensors.

An analyst comparing seasons needs to understand changes in both activity and instruments. Ember Atlas connects a real Pantanal case, geographic map and historical calendar to source-tagged evidence exports.

### 2. The instrument changeswhat gets reported.

MODIS and VIIRS have different resolution, sensitivity and acquisition times. A native detection count is therefore not automatically comparable across instruments. We retain the raw records, but also count occupied cells on one globally anchored point zero five degree grid per UTC day. Monthly activity sums those cell-days.

### 3. Replay a source change.Keep an observed benchmark.

The replay changes source in January twenty twenty-three, immediately after training ends. It uses observed MODIS beforehand and adjusted VIIRS afterward. MODIS actually continues, so we can reveal its holdout observations as a separate benchmark. Every exported month records the source, adjustment and factor. Missing values stay unavailable.

### 4. Same month.Different reported activity.

September twenty twenty-four has 5,819 MODIS cell-days and 8,809 common-grid VIIRS cell-days. Quarterly adjustment gives 4,879.1, still about sixteen percent below the reference. The comparison supports investigation of measurement differences. It does not identify independent fires or establish ground-truth accuracy.

### 5. Select a month. Inspect its evidence.

The product works without a visitor API key. Select a month and study area, inspect occupied-day cells, compare the sensors and download the matching records. The historical baseline uses earlier complete same-month observations. Every export retains source and coverage.

### 6. Lower error.Remaining bias.

All three methods use twenty twenty through twenty twenty-two for training and the same twenty-four separate holdout months. MAE is 1,021.7 raw, 175.3 scalar and 199.7 quarterly. The scalar is stronger there. We retain the frozen method and expose peak errors and bias. Reported MODIS version labels change across the split, limiting sensor-only interpretation.

### 7. A reproducible seasonal review.

Today the application provides source-tagged comparisons and independently evaluated local adjustments. Pantanal retains its frozen twenty twenty through twenty twenty-four domain. The nineteen later months are an audit below its extension gate. Usable observation opportunity, homogeneous reference processing and ground truth remain unverified. Recent products stay separate from Standard Processing. We invite a fire-monitoring team to review the seasonal evidence and define an observation-coverage validation pilot. The product, source and methods are public. Diego Shimohama created Ember Atlas for the NASA Space Apps challenge.

Script length: 342 words. No new human rehearsal has been timed. Three minutes is a local delivery target, not the official demonstration video limit.

## Likely questions

- **Is this accuracy?** No. It is agreement with MODIS_SP as delivered; independent ground truth and observation opportunity remain unmeasured.
- **Why retain quarterly factors when scalar wins?** The holdout is evaluation evidence, not a new selection set. All candidates are disclosed.
- **Are these unique fires?** No. They are reported thermal detections and common-grid occupied cell-days.
- **Can the calibration transfer?** Only to the evaluated full area and permitted complete SP months. No transfer to subregions or NRT.
- **What remains uncertain?** MODIS reference-version continuity, cloud/swath observation opportunity and physical impact.
