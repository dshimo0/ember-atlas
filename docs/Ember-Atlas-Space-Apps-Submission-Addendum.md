# Ember Atlas | NASA Space Apps 2026 submission addendum

Release note (2026-11-15): this planning document contains supplied event/deadline and fallback-format assertions that could not be independently reverified because official pages returned HTTP 503. Do not treat them as current verified rules. Follow [release-checklist.md](release-checklist.md), resource-check.json and the current portal/Local Lead guidance before final submission.

Use this English-language addendum alongside `Ember-Atlas-Codex-Cloud-Prompt.md` in the Codex Cloud workspace for [dshimo0/ember-atlas](https://github.com/dshimo0/ember-atlas). Apply this file to submission packaging and eligibility checks. The primary prompt governs the product, science and deployment. Carry out the preparation, create the artifacts below, verify their contents, and hand the Team Owner a paste-ready submission package. Leave acceptance of terms and the final portal submission to the Team Owner.

## Requirements audit

“Covered” means specified in the original prompt. It does not certify that the project, artifact or registration is complete.

| Requirement | Original prompt | Closeout evidence |
| --- | --- | --- |
| Respond to an official 2026 challenge | Covered. Harmonization of MODIS and VIIRS Hot Spots | Team page shows the challenge. Live app demonstrates the same-AOI calendar and sensor comparison, with measured validation wherever available. |
| Use at least one NASA data source or resource | Covered. NASA FIRMS and the SP sensor pair are specified | App and manifest show actual FIRMS observations, product names, geographic and date coverage, and version. Portal lists each NASA product actually used. |
| English project page and linked deliverables | Partial. English app and walkthrough were specified | Check the portal text, app, README and linked team-authored docs, slide text, captions, charts, labels, and exports. |
| English subtitles when a video uses another spoken language | Missing | Prefer English narration and reviewed English captions. For Portuguese or any other spoken language, verify synchronized English subtitles in the public player. |
| No photo, video or audio of people under 18 in demo or submission | Missing | Review every frame, thumbnail, background and audio track. Use screen capture and verified adult narration or silent English on-screen text. Remove uncertain clips. |
| Team registration, same event, no waitlist and Members tab | Missing | Team Owner checks each member's account and roster in the official portal. A public roster alone does not establish registration or waitlist status. |
| Local Event minimum of one, Universal Event minimum of two | Missing | Team Owner checks actual event type and count. The prior São Paulo team screen showed one member, which satisfies the Local Event minimum if still current. Official event page advises teams of no more than six. |
| Project Demonstration as a separate portal deliverable | Partial. Three-minute English walkthrough included, portal format absent | Test a separate public media URL that complies with the current guide. Verify runtime or slide count. |
| Public project and source links | Covered as requested, completion unverified | Validate the deployed HTTPS app, repository and any media or evidence links without login. |
| NASA and partner/other resource links, rights and credits | Partial. Attributions were requested generally | Build a complete resource inventory and copy named absolute URLs to the applicable fields. Check permissions and attribution for third-party materials. |
| Submit by deadline and explicitly enter judging | Partial. Original prompt leaves submission to owner | Owner confirms terms, submits for judging and captures the final portal state. |

## Verify the current portal and guide first

1. Open the team's **Project** tab for the current edition. Use the [official Resources page](https://www.spaceappschallenge.org/resources/) and the Project Submission Guide linked from the form. Record the confirmed labels, required fields, character limits, demo formats, link rules, any AI disclosure instructions, and any event-specific instructions from the São Paulo Local Lead. Follow the current official form and guide when they differ from this addendum.
2. Prepare a **30-second English video or up to seven English slides** as a practical fallback. These limits appear on a 2026 local organizer's schedule in [Kushimoto](https://www.spaceappschallenge.org/2026/local-events/kushimoto/?tab=schedule); confirm acceptance with the current guide or São Paulo form before marking compliant. The three-minute walkthrough in the primary prompt is for rehearsal or a local pitch if permitted. Verify São Paulo's actual pitch runtime and any separate deadline.
3. Confirm the current official portal deadline, applicable timezone and any earlier local judging cutoff with the current portal and São Paulo Local Lead. The planning date supplied with this document was not independently verified and must not be used as a current deadline. [Official event page](https://www.spaceappschallenge.org/2026/)
4. Check applicable rules for work done before the official start and reuse of existing material. Preserve original Git history, document actual dates and scope of repository scaffolding and any pre-existing Orbital Edge work, and ask the Local Lead for a ruling if eligibility is unclear. Use accepted work only in the judged submission. Never redate, conceal or relabel work as newly produced.

## Produce the submission package

Store the following deliverables under `submission/` in the project or in an equivalent directory. Put public citations and methodology in the repository. Keep any evidence containing registration details, private screenshots or permissions correspondence in a private handoff. Include the file paths and verified public URLs in the final summary.

### PROJECT-PAGE.md

Write English copy matched to the current form. Replace working placeholders before pasting. Verify final copy against the deployed release.

| Portal field or section | Ready-to-paste content |
| --- | --- |
| Project name, if requested | **Ember Atlas** |
| Summary | “Ember Atlas helps fire and land managers compare satellite-observed fire activity across MODIS and VIIRS. In the Pantanal, its interactive calendar links monthly activity and historical comparisons to downloadable NASA FIRMS observations.” Update to match actual released features and measured coverage. |
| Project Demonstration | One complete HTTPS URL to the public short video or slide deck that meets the current rules. Open it while signed out and test playback, English subtitles and permissions. |
| Project | Direct public HTTPS URL to the live application. Add the public repository URL in the appropriate field or Project Details, following form instructions. |
| Project Details | Explain the sensor shift problem, audience, calendar workflow, reproducible grid and calibration and independent evaluation if available. Include actual products, dates, metrics with units and sample sizes, limits and the anonymous steps to reproduce a result. If calibration is unavailable, state the actual level of comparability achieved. |
| Use of Artificial Intelligence, if present or required | Disclose the tools actually used, including Codex if used, what they assisted with, any specific generated assets and what the team verified. State that the observational data came from FIRMS if verified. Follow any required asset-level disclosures or markings in the current guide. Keep ordinary product UI focused on its use and data provenance. |
| NASA Data | Add one named Link Text and complete public HTTPS Link URL per NASA resource actually used. Use public product documentation or landing pages for exact products and versions. Never paste keyed FIRMS request URLs. |
| Space Agency Partner & Other Data | Add named public links for datasets, reused code, tools, text, images, map layers, assets, fonts, music and libraries that were actually used, as applicable to the current form. |
| Project Submission Verification | Owner verifies every condition and personally accepts the terms and submits for judging. |

### RESOURCES.md

Create a table with portal category, Link Text, complete public URL, exact version/product, where it appears, license or permission status, and required attribution. Generate entries from the release, not a speculative stack.

- NASA candidates include NASA Earthdata FIRMS, MODIS C6.1 Standard Processing and VIIRS NOAA-20 375 m Standard Processing. Keep entries only for what was used and find the exact official product pages. Add any other NASA resource actually used. Show how those observations drive the calendar, comparison and CSV.
- Other candidates include the actual basemap and tile provider, geographic boundaries, map/rendering libraries, reused code, documentation, uploaded images, fonts and audio. Credit openly available materials and verify permission for restricted ones. Keep existing attributions visible where the relevant terms require them. If permission or branding usage is uncertain, exclude the material or resolve it before submitting.
- Useful starting links are [NASA FIRMS](https://www.earthdata.nasa.gov/data/tools/firms), [FIRMS Archive](https://firms.modaps.eosdis.nasa.gov/download/) and [Participant Terms and Conditions](https://www.spaceappschallenge.org/legal/).

### DEMONSTRATION.md and public media

Create a storyboard tied to a real verified user flow. For a 30-second cut, use this pacing:

| Time | Show |
| --- | --- |
| 0–5 s | Open on the Pantanal and pose the sensor-change question. |
| 5–13 s | Select a real month in the calendar and show its historical comparison when available. |
| 13–23 s | Switch from native counts to a common grid. Show one verified holdout result if available. |
| 23–30 s | Export the selected observations and close on the product name. |

For slides, stay inside the verified cap and organize them around the decision, sensor difference, NASA data, method, empirical evidence, actual workflow and limits. If publishing media is blocked, provide a finished storyboard and recorded or rendered asset where feasible. State the remaining upload step and keep the public-link check pending.

### RELEASE-CHECKLIST.md

For each item, record status, owner, evidence and time checked. Use `Verified`, `Pending`, or `Not applicable` with a reason. Reserve final confirmation for observed evidence.

- [ ] Team Owner confirms the challenge, current event, member count, hackathon registration, same event, absence of waitlist status and correct Members tab.
- [ ] Actual NASA FIRMS input and visible derivation are verified. Observed dataset date range, sensor platforms, products and scientific limitations agree across the application, documentation and media.
- [ ] Project page and linked team materials are in English. English subtitles were verified if narration uses another language. All submitted media were checked for photos, videos or audio of individuals under 18.
- [ ] Showcase material meets current duration or slide count. Live product, demo, repository, validation page and source links open anonymously on mobile or in a clean browser. Every portal URL is complete and publicly accessible.
- [ ] NASA resources and all applicable third-party resources are listed with verified credits and permissions. Actual AI use is disclosed where required. Existing work and work done during the hackathon are accounted for accurately.
- [ ] Team Owner confirms the actual form field limits, local schedule and any local submission steps, then reads the guide, terms and privacy policy.
- [ ] After pasting fields, the Team Owner saves progress, checks the preview and opens links again from the portal. Saving progress alone does not enter judging.
- [ ] The Team Owner selects **Submit for Judging**, handles any prompts shown by the official form and verifies the success state explicitly confirms submission for judging. Keep a private screenshot or confirmation with timestamp and verify the project page remains accessible as intended.

## Final handoff

Return the project-page copy, demo format and verified public URL, live app and repository links, resource list and release checklist. Report which gates remain pending, who can close them and the next action. Status can be “technical scope mapped,” “submission package ready for owner review,” or “submission verified by owner,” depending on the evidence. Never assert registration, permissions, submission, eligibility or selection from a Markdown plan alone.
