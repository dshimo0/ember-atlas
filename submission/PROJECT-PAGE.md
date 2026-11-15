# Portal copy — English

Project name: Ember Atlas

Summary: Ember Atlas makes a satellite sensor transition inspectable. A Pantanal replay changes from observed MODIS to adjusted VIIRS, reveals independent fitting-period MODIS holdout observations, and exports source-tagged evidence. Eight study-area presets provide real observed maps and data downloads.

Project URL: https://ember-atlas-opal.vercel.app/

Guided exploration: https://ember-atlas-opal.vercel.app/demo?region=pantanal&view=replay&benchmark=1&month=2024-09

Presentation: https://ember-atlas-opal.vercel.app/pitch

Source: https://github.com/dshimo0/ember-atlas

Project Details:

The primary Pantanal calendar replays a source change at January 2023, after the frozen 2020–2022 training window. It uses observed MODIS beforehand and seasonally adjusted NOAA-20 VIIRS on the MODIS-reference scale afterward. MODIS actually continues: its 2023–2024 observations are a separate benchmark excluded from fitting. Every exported replay month records source, adjustment, factor, UTC scope and snapshot identity.

On the same 24 complete paired holdout months and study area, common-grid monthly MAE against MODIS is 1,021.7 cell-days unadjusted, 175.3 with a training-only scalar, and 199.7 with the existing frozen seasonal factors. The scalar is better on this evidence; no replacement was selected on the same holdout. For the six months with greatest observed MODIS activity, scalar/seasonal MAE is 404.6/534.6 cell-days/month. All residuals are published. MODIS is a comparison reference, not ground truth.

The observed MODIS archive spans November 2000–December 2024 for the same Pantanal study geometry. Calibration remains evaluated only in 2020–2024. Southern Amazon, Cerrado, Gran Chaco, California, Southeastern Australia, Iberian Peninsula and Siberia have real matched September 2024 SP snapshots and no inherited calibration. All eight have a separate recent NRT window. Each explicitly bounded study area has an interactive map, source/coverage labels and matching exports.

Map occupancy uses full matching observations: occupied UTC days per 0.05° cell for a named sensor. Sampled detections are optional. NRT stays separate from Standard Processing. Retrieval completeness does not establish usable satellite observation; thermal anomalies and cell-days are not unique fires or burned area.

Project Demonstration: the current silent screen recording is https://ember-atlas-opal.vercel.app/assets/workflow-capture.mp4 . It shows the actual replay, observed benchmark, region change and eight-area world map. The Team Owner must verify the current official demonstration format and choose or update the compliant asset. The nine-slide pitch is separate and is not asserted to meet an official cap.

Use of Artificial Intelligence:

OpenAI Codex assisted with implementation, scientific analysis code, tests and English documentation. NASA FIRMS observations are real. Product figures are computed from versioned data or actual screen captures. Temporary synthesized English speech measured script duration; no generated audio is published. Human review, current portal AI wording and actual team contributions require Team Owner confirmation.

NASA and third-party resources: use the named public links and product list in RESOURCES.md. Human roster, eligibility, media format, terms and final submission remain owner actions.
