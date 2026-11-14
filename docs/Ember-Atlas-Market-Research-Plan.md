# Ember Atlas | Market discovery and pilot design

Start with one question. Does a reproducible multi-sensor history improve a recurring fire-season review enough for an organization to adopt and fund the workflow?

## Initial positioning and hypotheses

The initial user is an analyst or land manager responsible for the Pantanal or a defined conservation area. The task is reviewing seasonal activity, investigating unusual months and sending traceable evidence to decision-makers. An operational sponsor may be a protected-area manager, environmental agency, NGO or land-management lead. Procurement authority and budget may sit elsewhere. Treat each as a role to verify.

| Hypothesis | Evidence to collect | What would weaken it |
| --- | --- | --- |
| A recurring seasonal review is slow or hard to reproduce. | Ask for the latest report and walk through tools, elapsed time, handoffs and corrections. | A trusted, repeatable report already runs automatically. |
| Sensor comparability affects a decision. | Ask for a real comparison that crossed a sensor or product transition and what could change in the report. | Users already rely on a fit-for-purpose stable reference series and see no unmet need. |
| The evidence export removes manual work. | Run the same task with the current workflow and Ember Atlas. Compare time, errors and reproducibility. | Faster task time comes at the expense of verifiable results, or the team needs a different output. |
| There is a viable purchase path. | Identify the sponsor, payer, procurement route, existing spend and conditions for a scoped pilot. | Users express interest but cannot name a sponsor, budget path or next meeting. |

## Desk research started

Use the same task, area and date range where the tools support it. Record what you can reproduce, runtime, exports, versioning, user and documented limits. “To verify” is the default for features not tested.

| Alternative | Verified starting point | Test next |
| --- | --- | --- |
| NASA FIRMS | Official active-fire map and observation data access. | Can an analyst perform the same historical comparison and take the evidence into a monthly report? [Map](https://firms.modaps.eosdis.nasa.gov/map/) · [Area API](https://firms.modaps.eosdis.nasa.gov/api/area/) |
| INPE Programa Queimadas | Active-fire data, historical statistics from its reference satellite, maps and downloads. | Compare its reference-series workflow, geographic levels and time to export. Treat it as a serious incumbent. [INPE](https://data.inpe.br/queimadas/) |
| MapBiomas Fogo | Historical burned-area products for Brazil. | Ask when users need burned-area evidence alongside hotspot activity. Keep these metrics distinct. [MapBiomas Fogo Collection 5](https://doi.org/10.58053/MapBiomas/WIOJ3R) |
| Internal QGIS, spreadsheets and scripts | Workflow hypothesis. | Observe a user building the last report. Capture steps, manual joins and review costs. |

## Start the research

1. **Desk work today.** Time-box the first benchmark to 90 minutes. Record each attempted workflow and publish source links and dates in a research log. The three source rows above are a starting point. Confirm capabilities before making comparative claims.
2. **Recruit for discovery.** Build an initial list of 12 contacts across protected areas, environmental agencies, NGOs and land-management operations. Prefer analysts who prepared a recent seasonal review and managers who approved it. Aim for six conversations with at least two decision or budget owners. Use public professional contact channels. Have the Team Owner approve and send any outreach.
3. **Interview before showing the product.** Ask “Walk me through the last seasonal review”, “What was the hardest comparison?”, “What did you export and to whom?”, “Where did the team disagree about the numbers?”, “How long did that take?”, and “Who would approve a change in the workflow?” Then ask for a short, anonymized task benchmark.
4. **Run a matched task.** Ask participants to identify an unusual month within a fixed AOI, explain the baseline and export the evidence. Measure elapsed time, completion, whether the conclusion is supported and whether a second person can repeat it. Alternate tool order when feasible. Report counts and limits for a small sample. Do not extrapolate to response times or avoided losses.
5. **Test a pilot.** Propose one AOI, one reporting cycle, one standardized export and a review at the end. Define starting metrics with the sponsor. Ask for data access, a named owner and a scheduled review. A sponsor who commits time or procurement work is stronger evidence than a compliment.

Recruiting copy for owner review:

> I’m researching how teams review seasonal fire activity and compare satellite records across years in the Pantanal. Could you walk me through a recent report in a 20-minute call? I’m interested in the steps you use today, where the work gets difficult, and what evidence the report needs.

## Evidence and go/no-go

Capture date, organization type, role, workflow, tool, observed pain, exact evidence, time and units, buyer, procurement path, objection, consent for quotations and next action. Keep contact information and candid interview notes in private records. Publish anonymous findings and cite public sources.

Working pilot criteria to agree with the sponsor: at least two organizations independently describe the same recurring problem, one supplies a real workflow for a benchmark, and one names a sponsor and next meeting. For a timed pilot, target a 25% median reduction in time to produce a traceable review, with no loss in task accuracy or reproducibility. These are decision thresholds, not results. If the reporting task is already solved, investigate narrower audit or sensor-transition needs before broadening the product.

Build a bottom-up market estimate only after mapping addressable organizations and actual procurement paths. Use number of realistically reachable organizations multiplied by a tested annual contract range. Separate geography, buyer segment and payer. Record base, conservative and upside scenarios with sourcing and uncertainty. Validate pricing through existing spending, approval limits and a specific pilot offer. Start with managed AOIs and reproducible reporting as service hypotheses around the public analysis. Present actual evidence, unresolved assumptions and the next decision in a one-page memo.
