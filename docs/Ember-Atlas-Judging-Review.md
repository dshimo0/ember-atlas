# Ember Atlas | Adversarial judging review

Use this internal rubric before recording or submitting. The weights are a team decision. Check the 2026 official guide and São Paulo instructions for actual judging and submission rules. [NASA Space Apps Resources](https://www.spaceappschallenge.org/resources/)

## Review protocol

Pin the release commit, snapshot ID, app URL and submission package. Run the workflow signed out on a phone and in a clean desktop browser. Record the path, expected and actual behavior, evidence link, reviewer and timestamp. For numerical claims, trace the number in the UI and pitch back to the same exported rows and validation artifact. Have a reviewer unfamiliar with the project try the workflow where available. Record solo review honestly.

| Score | Evidence |
| --- | --- |
| 0 | Missing or contradicted by the release. |
| 1 | Documented intent or unverified claim. |
| 2 | Partial execution or narrow evidence with material gaps. |
| 3 | Working and reproducible on the declared release and scope. |
| 4 | Independent repeat or a documented stress case supports the result and its limits. |

Multiply weight by score divided by four. Internal target is 80/100 with no release blocker. Scores do not waive submission requirements.

| Criterion | Weight | Judge's roast | Evidence that earns points |
| --- | ---: | --- | --- |
| Challenge fit | 12 | A fire map with a different logo is still a fire map. | Choose the Pantanal study area, select a period, open the calendar, inspect sensor differences and export the evidence. |
| NASA data | 10 | NASA in the footer is not a data pipeline. | Trace one displayed month and one CSV row to the FIRMS products and versioned raw manifests. Compare requested dates with actual retrieval. |
| Innovation and validity | 22 | You changed the unit and called the difference solved. Show me the holdout. | Show raw counts, common-grid cell-days, frozen split and factors, same-unit holdout MAE and signed bias before and after, and the calibration decision. Show sampling caveats and sensitivity where measured. |
| Working product | 16 | Your demo works perfectly on the machine that built it. | Signed-out HTTPS workflow from map and date filter through matching CSV. Check mobile, empty ranges, partial coverage, and continued service from the snapshot if FIRMS fails. |
| User and impact | 10 | Which decision gets better on Monday morning? | Name user, recurring task, evidence used and a decision they can make. Keep interviews and any timed task results distinct from hypotheses. |
| Documentation | 8 | If the number cannot be reproduced, it is decoration. | Pin inputs, commands and output artifacts. Confirm at least one reproducible result and version the methods, credits and limitations. |
| Presentation | 8 | Five charts and I still cannot tell which sensor changed. | Independent listener can repeat the problem, result and use case in one sentence. Use English and the same result across the app and media. |
| Submission | 8 | The draft is beautiful. Did it enter judging? | Link checks, team and form verification, correct media format, and Team Owner confirmation from the portal. |
| Execution ownership | 3 | Who can fix the release if the data refresh fails? | Record actual contributors, responsibilities and a short recovery path. A one-person team can name distinct responsibilities. |
| Geographic transfer | 3 | A new pin is not a validated new geography. | Explain the inputs, overlap, re-fit and validation required to apply the method to a second region. Show any tested transfer explicitly. |

## Release blockers

- **Evidence integrity** — Remove unsupported claims, synthetic observations in public views, hidden missing-window substitutions, and any suggestion that hotspots are unique fires or burned area. Withhold the calibrated series when the prespecified acceptance rule fails.
- **Scientific leakage** — Any holdout period used for tuning invalidates the claimed independent test. Reissue findings with a genuinely untouched split or mark the result exploratory. Compare common-grid MAE on identical paired months. Keep raw detection counts as a separate diagnostic.
- **User workflow** — Broken links, login walls, incorrect exports and failures on the selected judging path require a fix or an explicitly scoped release. A video cannot establish public app accessibility.
- **Submission integrity** — Verify current format, credits, permissions, language, roster and eligibility from the submission addendum. Team Owner must verify the actual submission status.
- **Security and reproducibility** — Check release artifacts for FIRMS keys and keyed URLs. Pin snapshot, AOI, UTC dates, method and calibration scope. Retain the last verified snapshot if ingestion fails.

## Verification cases

1. Select a month with a complete pair and reconcile displayed month totals, per-product rows and exported filter state with the snapshot.
2. Repeat with a zero-detection window, an absent window, and a partial month. Confirm the labels and aggregate behavior tell those conditions apart.
3. Inspect one holdout month manually. Verify the factor came from the training years and recalculate the residual. Check signed bias convention, sample sizes, same comparison units and seasonal results.
4. Change the AOI. Confirm the export changes and the Pantanal factor is unavailable outside its validated scope. Check transition handling and confirm VIIRS and MODIS estimates were not added together.
5. Open the public URL and repository in a clean session. Rebuild the reported output from pinned inputs. Review resource and AI attribution where applicable. Record the actual outcome.

## Triage and decision record

P0 covers evidence integrity, the primary public workflow and eligibility. Fix P0 first. P1 covers material scientific or product weaknesses. P2 covers polish. Every finding needs severity, observed evidence, user or judge consequence, specific fix, owner and retest.

Current review baseline is commit `0785c3e` on `main`. FIRMS ingestion and the common-grid daily baseline are in the repository. The app, real-data ingestion run, calibration metrics and submission confirmation have not been verified at this baseline. Reassess from the release commit before giving a score. [Repository baseline](https://github.com/dshimo0/ember-atlas/tree/0785c3e1cd225a6ffaf91c34d723b9a07cbcfc75)
