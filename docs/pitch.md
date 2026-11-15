# Three-minute presentation

Public deck: https://ember-atlas-opal.vercel.app/pitch

Nine slides use the same pinned release and metric calculations as Explore and Guided demo. Previous/Next, arrow keys, Page Up/Down, Home/End, optional fullscreen and hidden presenter notes are available. A slide query parameter supports sharing and browser navigation. Mobile shows the nine sections in reading order. Print / PDF produces nine landscape A4 pages. The [PDF](../submission/ember-atlas-pitch.pdf) is a presentation export, not a verified official submission format.

## Script and timing

The script begins with the actual Pantanal map and September observation, then explains the decision, sensor problem, product, method, validation, use case and pilot. It contains 454 words. A synthesized English read at 180 wpm measured **184.646 seconds (3:05)**. This is measured audio duration, not a human rehearsal or a word-count estimate; navigation pauses are excluded. The generated timing audio stayed in temporary storage and is not submission media. [Timing record](../submission/pitch-timing.json) records the script hash. The Team Owner must rehearse the human delivery and confirm the actual local event duration.

### 1. Ember Atlas

This map shows real NASA FIRMS observations in the Pantanal study rectangle for September twenty twenty-four. Both sensors recorded activity above their own prior September medians. Ember Atlas links this map to a historical activity calendar and downloadable evidence for seasonal review.

### 2. The user and decision

A regional land-management analyst needs a consistent historical comparison when deciding which months deserve deeper investigation. The implemented workflow selects a region and month, compares prior years, inspects sensor disagreement and exports evidence for a seasonal report. We have not measured customer demand or time saved.

### 3. Different sensors, different observations

MODIS and VIIRS observe at different spatial resolutions and times, and their sensitivity differs. Hotspot counts can differ over the same area and dates. We retain native thermal-anomaly counts alongside a shared spatial and temporal basis. Clouds and usable observation coverage are still unmeasured in this release.

### 4. The working product

The application serves a versioned snapshot covering twenty twenty through twenty twenty-four. The map, calendar and exports share area, month and sensors. A locally stored geographic layer keeps the map useful if external tiles fail. The calendar distinguishes training and holdout years, while missing retrieval remains separate from recorded zero detections.

### 5. Adjusted VIIRS on the MODIS-reference scale

Each occupied grid cell counts once per product per UTC day. We sum those daily counts into monthly cell-days. Quarterly factors use the ratio of training MODIS totals to training VIIRS totals. Factors remain fixed for the holdout. The output is adjusted VIIRS on the MODIS-reference scale, without summing sensors.

### 6. Holdout evidence

Across the twenty-four holdout months, monthly mean absolute error against MODIS falls from 1,021.7 to 199.7 occupied cell-days, a reduction of 80.5 percent. Adjusted bias remains minus one hundred twenty-four cell-days per month. Adjustment is worse in two holdout months. MODIS is the comparison reference; ground-truth accuracy is unmeasured.

### 7. Investigate an unusually active month

In September twenty twenty-four, both sensor records exceed their own prior September medians. Adjusted VIIRS is about four thousand eight hundred seventy-nine cell-days, still sixteen point two percent below MODIS. The product supports investigation of that difference. Fire severity, causes and burned area remain unmeasured. The selected observations and period aggregates can be downloaded with provenance.

### 8. Pilot and expansion

A practical next step is one pilot seasonal review with a regional land-management team. Measure preparation time and whether another analyst can reproduce its evidence. Expansion to another region requires matched observations, local fitting and independent evaluation. Monitored areas and scheduled reports are a possible service hypothesis; there are no claimed contracts, partnerships or monetary savings.

### 9. Project ownership and next milestone

The public application, source, methods and NASA resources are linked here. Git history records the implementation work; the Team Owner still needs to confirm the human roster and submission eligibility. We are seeking a regional analyst to repeat one seasonal review and evaluate the workflow. That pilot is the next milestone before broader operational or commercial claims.

## Judge questions

- **What was trained?** Quarterly VIIRS-to-MODIS ratios fit on complete 2020–2022 monthly occupied cell-days. No language model or fire prediction is trained. The 2023–2024 holdout was excluded from fitting.
- **What does 80.5% mean?** Lower monthly MAE against MODIS on 24 complete paired holdout months in the full rectangle: 1,021.7 → 199.7 cell-days/month. It is not detection or ground-truth accuracy.
- **Where does adjustment fail?** Absolute residual increases in February and March 2023. September 2024 remains 16.2% below MODIS. Bias and all monthly residuals are inspectable.
- **What is harmonized?** Adjusted VIIRS on a MODIS-reference scale. Separate source series remain visible; there is no fused multi-decade record, source transition or adjusted point geometry.
- **Can I select a subregion?** Fixed northern/southern masks have raw activity and own-mask historical medians. Full-area calibration is withheld; independent regional fitting/evaluation is future work.
- **What is not measured?** Unique fires, burned area, usable swath/cloud observation coverage, ground-truth accuracy and operational impact. The map is a display sample; CSVs contain all matching records.
- **Who is on the team?** Repository ownership and Git contributions are verifiable. The human roster and roles require Team Owner confirmation; no names or interviews are invented.

## Official format and credits

The three-minute target is a strategic presentation choice. Current official challenge/resources/guide access was blocked by HTTP 503 on 2026-11-15. Nine slides must not be submitted as an officially compliant demonstration without owner verification. Existing silent screen recording and its verification are described in [DEMONSTRATION.md](../submission/DEMONSTRATION.md); that recording predates these routes. No people or audio appear in the authored public visuals. NASA FIRMS observations, OpenStreetMap, Natural Earth and Leaflet are credited in [RESOURCES.md](../submission/RESOURCES.md). Actual Codex use is disclosed in the portal copy.
