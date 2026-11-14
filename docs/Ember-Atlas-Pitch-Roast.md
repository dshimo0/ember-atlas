# Ember Atlas | Pitch script and roast

Rehearse in English. This three-minute script is for a local presentation if allowed. Verify the São Paulo pitch time and official submission media format independently. For the latter, follow the [submission addendum](Ember-Atlas-Space-Apps-Submission-Addendum.md). Replace bracketed fields with verified release evidence before recording. Use the fallback wherever a result is unavailable.

## Three-minute script

| Time | Show | Say |
| --- | --- | --- |
| 0:00–0:25 | Pantanal study area and two native sensor traces | “Imagine reviewing a fire season in the Pantanal. The record jumps around the time a different satellite sensor is introduced. Did fire activity change, or did the instrument change what we could see? That question affects which months a land manager investigates.” |
| 0:25–0:55 | Same date range, different counts, then common grid | “Ember Atlas starts with real NASA FIRMS observations. MODIS and VIIRS report thermal anomalies at different spatial resolutions and observe at different times. We put the detections on the same grid and count each occupied cell once per UTC day, separately for each product. This gives us one unit for comparing monthly activity.” |
| 0:55–1:35 | One holdout chart, with dates and units on-screen | “We estimated the seasonal adjustment on [training years] and kept [holdout years] separate. On [N] matched months, monthly mean absolute error against the MODIS reference went from [A] to [B] occupied cell-days. Signed bias went from [C] to [D]. [State the actual acceptance decision and a measured or documented limitation.]” |
| 1:35–2:15 | Live month click, baseline and CSV | “Here is [verified month] in our Pantanal study area. The calendar shows [actual metric] against [actual same-month baseline and years]. A reviewer can see coverage, inspect the original sensor series and download the same selection I’m showing.” |
| 2:15–2:40 | One concrete decision and geographic context | “A land-management analyst can use this view to choose which unusually active months or areas deserve deeper review before the next season. The workflow can be repeated for a new region by retrieving overlapping observations and testing the calibration there.” |
| 2:40–3:00 | App, repository and evidence links | “The public app, source code and data provenance are linked in our submission. Pick a month, export the evidence and check our calculation.” |

## Fallback lines

- **No defensible calibration** — “We aligned the instruments on a common grid and measured the remaining difference. [Explain the actual result or sample limitation.] The app shows the sensor-specific series for this area.”
- **No eligible historical baseline for the chosen month** — Choose a verified month with a baseline. If none exists, show the verified sensor comparison and say the historical baseline is unavailable for the published coverage.
- **Live network or projector fails** — Use a pre-recorded capture of the same verified release and keep exported evidence on hand. State the actual issue and retain direct public links.
- **No verified real observations or deploy** — Say what was implemented and what remains blocked. Any captured artifacts must reflect the actual state.

## Questions a skeptical judge will ask

| Roast | Defensible answer or evidence |
| --- | --- |
| “Why should I open this when FIRMS and INPE already exist?” | Show the exact comparison and export task. Describe observed workflow differences and cite the tools. Avoid claims about competitor capabilities you did not test. |
| “A grid reduces duplicate pixels. How does that correct orbit timing and clouds?” | It standardizes the analytical unit. A local empirical transfer is evaluated out of sample. State remaining timing, coverage and detectability limits. |
| “Where did those error numbers come from?” | Show validation.json, the tested periods and paired month count. Recalculate one residual. Confirm the unscaled and scaled errors are in the same unit. |
| “Did the factor learn your showcase year?” | Show the frozen year split. If the showcased year was used for fitting, identify it as a workflow illustration and show independent evaluation separately. |
| “Can I use that adjustment in Australia tomorrow?” | The method can be run there after gathering inputs and testing it on independent regional overlap. Show the current geographic scope. |
| “Did your tool prevent a fire?” | Show the specific review decision the tool supports. Report any measured workflow effect within its scope. |
| “What does zero mean?” | Zero recorded detections in a retrieved window. A missing window and unknown observation coverage are handled explicitly. |
| “What did your team actually deliver?” | Name contributions and release artifacts. Disclose actual AI assistance where required and use the commit history to distinguish prior work. |

## Rehearsal checklist

- Run the script twice with a timer and once with the backup recording. Start the live walkthrough from a signed-out browser.
- Freeze the release, the selected month and the validation figures before recording. Match all on-screen units, dates and numbers to the actual exports.
- Ask a listener to state the decision, the scientific comparison and its limitation. Rewrite the specific sentence if they cannot.
- Keep the pitch, formal submission media and submission status independently tracked. Trim content to the confirmed format before publishing.
