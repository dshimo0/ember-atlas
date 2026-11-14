# Ember Atlas | Evidence-led pitch and judge walkthrough

Open https://ember-atlas-opal.vercel.app/ in a signed-out browser. The actual landing screen asks **“Fire season, or sensor change?”**, presents the measured holdout improvement and opens on September 2024. All figures below refer to `snapshot-19621fa88d40.json.gz` and immutable `validation-ba55acfc7909.json`; they are not forecasts or independent ground-truth accuracy.

## Opening

“In September 2024, both satellites recorded more activity in our Pantanal study area than their own historical September medians. But they reported different amounts. Ember Atlas puts them on one grid and tests a local sensor adjustment on unseen years. Monthly disagreement with MODIS fell by 80.5%—and we show the error that remains.”

## Short judge walkthrough

1. Point to **80.5%** on the opening card: MAE **1,021.7 → 199.7 occupied cell-days/month**, fit on **2020–2022**, evaluated on **24 complete paired months in 2023–2024**. Read the full-area scope and MODIS reference caveat.
2. In September 2024, show the chart: **5,819 MODIS**, **8,809 VIIRS common grid**, **4,879.1 adjusted VIIRS**. The adjustment moved VIIRS closer but left it **939.9 cell-days, or 16.2%, below MODIS** that month.
3. Expand the baselines: **MODIS 2,532; VIIRS 4,782**, both from **2020–2023 (n=4)**. Their observed values are **129.8% and 84.2% above** the respective medians. Keep native detections separate at **23,396 / 101,659**.
4. Choose another month in the labeled TRAIN/HOLDOUT calendar. Select the northern half: its observations change, but no full-area factor is inherited. The notice sits beside the comparison.
5. Download the selected month's observations, then the selected-period aggregates. The default selection yields **125,055 observation records** and **120 aggregate rows** across the five-year calendar. Follow the provenance link to reproduce the comparison.

## Three-minute local pitch — use only if the local format allows

| Time | Actual screen/action | English narration |
| --- | --- | --- |
| 0:00–0:25 | First viewport: question, September finding and holdout card | “Was this an unusually active fire season, or did changing satellites change what we could detect? In our Pantanal study window, September 2024 was above the historical September median in both sensor records. The amount depends on which sensor we read.” |
| 0:25–0:55 | September common-unit chart and native-count detail | “NASA FIRMS reports thermal anomalies, not unique fires or burned area. MODIS and NOAA-20 VIIRS have different footprints, sensitivity and observation times. We count occupied cells once per UTC day on the same 0.05-degree grid. Here MODIS records 5,819 cell-days and VIIRS 8,809. Native detection counts remain separately inspectable.” |
| 0:55–1:30 | Opening validation card, frozen JSON and selected residual | “We fit quarterly VIIRS-to-MODIS factors using 2020 through 2022, then held them fixed for all 24 matched months in 2023 and 2024. Monthly mean absolute error against MODIS fell from 1,021.7 to 199.7 cell-days, a reduction of 80.5%. This is agreement with a reference, not ground truth. Average adjusted bias remains minus 124.0 cell-days per month.” |
| 1:30–2:00 | September chart, then expand both baseline breakdowns | “The adjusted September value is about 4,879 cell-days—still 16.2% below MODIS. Separately, each product is above its own prior September median: 2,532 for MODIS and 4,782 for VIIRS, using four complete prior years. This is evidence for a seasonal review, not proof of a trend or a cause.” |
| 2:00–2:30 | Full historical calendar, another month, north selector and notice | “The five-year calendar makes the training and holdout years visible. We can inspect a smaller area, but the full-area adjustment is withheld there. It would require a new fit and independent validation. Country boundaries orient the map; the rectangle is our study window, not a biome boundary.” |
| 2:30–3:00 | Observation and aggregate downloads; methods/provenance links | “A regional analyst can choose which months deserve deeper investigation and export the exact evidence for that review. The map and observation export share the selected month, area and sensors; the aggregate export covers the chosen calendar period. Every figure links to a versioned NASA-derived snapshot. We have not yet measured time saved or prevented fires.” |

## Skeptical questions and defensible answers

| Question | Answer from this release |
| --- | --- |
| “Does 80.5% mean you measure fires 80.5% more accurately?” | No. It is a reduction in monthly MAE against MODIS on the same occupied cell-day scale, over the 24 frozen holdout months. MODIS is not independent ground truth. |
| “Why is September still different after adjustment?” | A seasonal empirical ratio does not remove cloud, overpass, detectability or sampling differences. The remaining September residual is -939.9 cell-days; overall bias remains -124.0/month. |
| “Did you fit on your showcase month?” | No. Factors use 2020–2022 only. September 2024 belongs to the held-out 2023–2024 period. No acceptance thresholds were changed for the redesign. |
| “What exactly is the historical median?” | Each sensor's complete prior years for that calendar month, excluding the selected year. September 2024 uses 2020–2023, n=4; the underlying values are expandable. |
| “Can you apply this in a smaller area tomorrow?” | Not without regional matched overlap, refitting and independent evaluation. The northern/southern views explicitly withhold adjustment and anomalies. |
| “What does zero mean?” | Successful retrieval with no detections recorded. Missing retrieval remains unavailable/blank; partial selected months retain their clipped dates and receive no adjustment. Observation coverage remains unknown even after complete retrieval. |
| “What can a land manager decide?” | Which unusually active months deserve a closer seasonal review. We have not established causal fire severity, unique fires, burned area, commercial demand or measured workflow impact. |

## Separate media and owner gates

This three-minute script is for a local pitch only if permitted. The official Project Demonstration portal format is a separate requirement. A proposed 30-second cut or up-to-seven-slide fallback from the addendum is not confirmed compliant until the Team Owner checks the current official guide and São Paulo instructions. Do not substitute the three-minute pitch for that verification.

The public screen recording was refreshed from the actual production interface: 30 seconds, silent, English application text, no people or audio. Before submitting media, confirm the official runtime/format requirements and inspect the final player/thumbnail. Final terms and submission for judging remain the Team Owner's responsibility. If the live network fails, show a capture of the same pinned release and state the issue.

Rehearse with a timer and an independent listener if available. Match the screen, CSV and narration to the same frozen artifacts; do not claim that the engineering self-review establishes independent usability or event eligibility.
