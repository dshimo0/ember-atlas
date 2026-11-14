# Portal copy — English

Project name: Ember Atlas

Summary: Ember Atlas helps regional fire and land managers inspect sensor changes in NASA FIRMS observations. A Pantanal study-area calendar links native MODIS and NOAA-20 VIIRS detections, common-grid activity, historical same-month comparisons and downloadable evidence.

Project URL: https://ember-atlas-opal.vercel.app

Source: https://github.com/dshimo0/ember-atlas

Project Demonstration URL: https://ember-atlas-opal.vercel.app/assets/workflow-capture.mp4

This is an actual 30-second silent screen recording. The Team Owner must confirm acceptance under the current official guide before using it in the portal; the separate three-minute pitch does not establish compliance.

Project Details:

Was a season unusually active, or did a different satellite detect more? Ember Atlas puts both products on the same globally anchored 0.05-degree WGS84 grid, counting each occupied cell once per UTC day. Analysts select the full Pantanal study rectangle or its northern/southern halves, choose dates and a month, inspect both products and export matching observations with provenance. Complete prior same-month years support sensor-specific medians; unsupported baselines are withheld.

The release uses real MODIS C6.1 SP and VIIRS NOAA-20 SP observations. Training was frozen at 2020–2022 and holdout at 2023–2024. All 24 paired holdout months are now retrieved. Common-grid monthly MAE was 1021.71 cell-days, versus 199.70 after the frozen seasonal adjustment. Adjustment publication is supported within the full study rectangle and evaluated 2020–2024 domain. Exact periods, sample sizes and errors are in RESULTS.md and the machine-readable validation output. Hotspots are thermal anomalies, not burned area or independent fires. Clouds and overpass sampling remain unmeasured without usable-observation masks.

Reproduce: serve the pinned web directory, select September 2024, inspect native detections and occupied cell-days, then download the selected month's observations. The complete flow was verified on the anonymous public HTTPS application.

Use of Artificial Intelligence:

OpenAI Codex assisted with implementation, scientific analysis code, tests and English documentation. Automated tests and browser checks were run; team review remains required. Satellite observations were acquired from NASA FIRMS. No synthetic observations or generated imagery are included in the product. This disclosure must be checked against the current portal's AI requirements.

NASA Data and Other Resources: use named absolute links from RESOURCES.md, retaining only products actually used. Team contributions: Codex-assisted engineering is documented here; Team Owner must provide the actual human roster and contributions before submission.
