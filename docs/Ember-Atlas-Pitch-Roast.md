# Presentation review and walkthrough

Start with the Pantanal map and September 2024 evidence. MODIS records 5,819 occupied cell-days; common-grid VIIRS 8,809; frozen seasonal VIIRS 4,879.1, or 16.2% below MODIS. These are occupied cell-days, not native hotspot counts or burned area.

1. Open [/demo](https://ember-atlas-opal.vercel.app/demo?region=pantanal&view=replay&benchmark=1&month=2024-09&start=2020-01-01&end=2024-12-31). Show the selected study rectangle, UTC month and observed map layer.
2. Follow the source-labeled calendar across December 2022 and January 2023. Explain that the cutoff is a replay scenario. Reveal continuing observed MODIS as the separate benchmark.
3. Compare the three methods on identical holdout months. Raw/scalar/frozen-seasonal MAE is 1,021.7/175.3/199.7 cell-days/month. The headline's 80.5% reduction compares seasonal against raw VIIRS, not against the stronger scalar baseline.
4. Inspect every monthly residual and the six most active MODIS-selected months. Peak scalar/seasonal MAE is 404.6/534.6. Agreement with MODIS is not ground-truth accuracy.
5. Inspect the separate January 2025–July 2026 Pantanal audit: n=19; raw/scalar/seasonal MAE 399.4/89.7/70.8; seasonal bias +67.4. Keep the published adjustment domain at 2020–2024 until its registered extension gate is met.
6. Open the eight-area world map. Follow a region link and inspect its actual source coverage and independent adjustment status. Export the selected observations, aggregates, occupied-day cells and provenance.

The [route script and judge questions](pitch.md) are the presentation source of truth. Its synthesized read is measured at 183.0 seconds; human delivery remains unmeasured. The nine-section pitch and local three-minute target do not establish compliance with the official Project Demonstration media format. Current official guidance remains an owner check after HTTP 503 responses.
