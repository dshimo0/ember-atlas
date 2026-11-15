# Pitch: comparable observations with inspectable evidence

[Live presentation](https://ember-atlas-opal.vercel.app/pitch) · [Guided case](https://ember-atlas-opal.vercel.app/demo?region=pantanal&month=2024-09&view=replay&benchmark=1) · [Methods & data](https://ember-atlas-opal.vercel.app/methods)

Nine sections follow the measurement problem, observed September case, continuity replay, independent evaluation, working workflow, eight local study areas, demonstrated scope and next pilot. All figures come from the same versioned artifacts used by the app. The scalar comparison, peak errors and MODIS version limitation remain visible.

Desktop uses a 16:9 stage with Previous/Next, keyboard navigation, optional fullscreen, hidden notes and print/PDF. Mobile scroll updates the counter and shareable slide URL. The regional world map remains on slide 7, with individually accessible study-area links and separate text alternatives.

The current English presenter notes contain 407 words. The prior 395-word script had a 176.2-second synthesized read at 180 wpm. The calendar-first revision changes the workflow narration; that earlier timing is historical and must not be presented as a new human rehearsal. Timing audio is not published. The three-minute local target is separate from the official Project Demonstration format, whose current guidance remains unverified.

## Spoken script

### 1. See the fire. Understand the past.

An analyst comparing seasons needs to understand changes in both activity and instruments. Ember Atlas connects a real Pantanal case, geographic map and historical calendar to source-tagged evidence exports.

### 2. The instrument changes what gets reported.

MODIS and VIIRS have different resolution, sensitivity and acquisition times. A native detection count is therefore not automatically comparable across instruments. We retain the raw records, but also count occupied cells on one globally anchored point zero five degree grid per UTC day. Monthly activity sums those cell-days.

### 3. Same month. Different reported activity.

September twenty twenty-four has 5,819 MODIS cell-days and 8,809 common-grid VIIRS cell-days. Quarterly adjustment gives 4,879.1, still about sixteen percent below the reference. The comparison supports investigation of measurement differences. It does not identify independent fires or establish ground-truth accuracy.

### 4. Replay a source change. Keep an observed benchmark.

The replay changes source in January twenty twenty-three, immediately after training ends. It uses observed MODIS beforehand and adjusted VIIRS afterward. MODIS actually continues, so we can reveal its holdout observations as a separate benchmark. Every exported month records the source, adjustment and factor. Missing values stay unavailable.

### 5. Lower error. Remaining bias.

All three methods use twenty twenty through twenty twenty-two for training and the same twenty-four separate holdout months. MAE is 1,021.7 raw, 175.3 scalar and 199.7 quarterly. The scalar is stronger there. We retain the frozen method and expose peak errors and bias. Reported MODIS version labels change across the split, limiting sensor-only interpretation.

### 6. Move from place and time to reproducible evidence.

Start with the selected month in the calendar, then inspect the map and sensor comparison. Region and month selection keep the CSV synchronized. Earlier complete same-month values provide historical context with explicit years and sample sizes. Inspect full grid occupancy or sampled detections, then download observations, aggregates and provenance. Visitors need no API key.

### 7. One workflow. Local evidence.

Eight explicitly bounded study areas share this workflow. Each opens real source observations and exports, with local coverage and evaluation evidence. New regional methods use an inner selection period, fixed refitting and separate outer and fresh gates. Full-area factors never transfer to another region, a smaller mask or near-real-time products.

### 8. Published today. What still needs evidence.

Today the application provides source-tagged comparisons and independently evaluated local adjustments. Pantanal retains its frozen twenty twenty through twenty twenty-four domain. The nineteen later months are an audit below its extension gate. Usable observation opportunity, homogeneous reference processing and ground truth remain unverified. Recent products stay separate from Standard Processing.

### 9. See the fire. Understand the past.

We invite a fire-monitoring team to review the seasonal evidence and define an observation-coverage validation pilot. The product, source and methods are public. Diego Shimohama created Ember Atlas for the NASA Space Apps challenge.

## Likely judge questions

- **Why keep quarterly factors if the scalar is better on the Pantanal holdout?** Its 2020–2024 publication rule was frozen. The already observed holdout is evaluation evidence, not a replacement-selection set. New methods or extensions require a separate registered evaluation protocol.
- **What does 80.5% measure?** Reduction in monthly MAE relative to unadjusted common-grid VIIRS, against observed MODIS, on 24 full-Pantanal holdout months in 2023–2024. It is not detection accuracy.
- **What remains at peak activity?** The six months ranked by observed MODIS have scalar/quarterly MAE 404.6/534.6 cell-days per month. September 2024 quarterly output remains 16.2% below MODIS.
- **Are the source versions homogeneous?** Unverified. Reported MODIS labels change from 6.03 in training to 61.03 in evaluation. Results measure agreement with the delivered MODIS_SP archive without isolating sensor effects.
- **Are regions interchangeable?** No. Each new area has its own registered inner selection, fixed refit and outer/fresh gates. Factors do not transfer to subregions or NRT. Pantanal keeps its original publication domain.
- **Is the imagery an analytical layer?** No. Blue Marble is a credited 2007 editorial composite. The Pantanal context image is MODIS Terra true color dated September 1, 2024. Both have local source/hash metadata and are separate from FIRMS occupancy.
- **What remains for the owner?** Confirm official eligibility/media rules, portal roster and contribution wording; rehearse on a physical device, accept terms and submit for judging. No registration, partnership or operational impact is inferred from the product.

## Presentation controls

The nine-section rail selects the same shared slide state as Previous/Next and keyboard navigation. It remains usable on mobile, is omitted from print and does not autoplay. Self-hosted typography has a system fallback; reduced-motion preferences disable entry effects. The current PDF is generated from the actual route, with nine pages. About's eight-area atlas is dated editorial context, separate from analytical fire measurements.

## Evidence workspace revision

The measurement slide uses the selected-month common-axis dot plot; the validation slide pairs all three MAEs with actual monthly residuals. The continuity slide uses the versioned monthly series with a visible cutoff. English and Portuguese presentation text are selectable, with dark/light palettes. The English script remains the submission reference; earlier synthesized timing applies to that unchanged English script, not the Portuguese translation. Each language was checked for nine-page print output.

## Calendar-first walkthrough

Start with September 2024 in Pantanal: read the selected result, locate the month in the calendar, inspect the map, then expand the historical trend and reveal observed holdout MODIS. Show raw, scalar and frozen seasonal errors and peak residuals. Link to /demo?month=2024-09&view=replay. The 3-minute local pitch is distinct from official submission media rules. No new backfill or orbital correction result is claimed.
