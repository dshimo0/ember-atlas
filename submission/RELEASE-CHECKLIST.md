# Release and judging gates

Checked 2026-11-14 UTC in Codex Cloud. No final submission was performed.

| Status | Owner | Gate and evidence |
| --- | --- | --- |
| Verified | Engineering | Existing branch `work` clean at start; original Git history retained. No work redated. |
| Verified | Engineering | Real SP pilot acquired for both sensors, August–September 2024. Raw CSVs/manifests and snapshot checksums preserved. |
| Verified | Engineering | 36 complete training months and 24 complete holdout months acquired after access recovery. RESULTS.md and validation.json record the frozen acceptance decision. |
| Verified | Engineering | English app, CSV fields and package authored; no people or audio in authored media. |
| Verified | Engineering | Anonymous production HTTPS https://ember-atlas-opal.vercel.app; complete public browser workflow and matching CSV exports passed. docs/DEPLOYMENT.md and browser-check.json record evidence. |
| Pending | Owner | Current official Project Demonstration duration/slide limit and separate local pitch limit. Resources/challenge fetch returned 503. Proposed fallback is not verified compliant. |
| Verified / Pending | Engineering / Owner | Actual silent English-screen recording is public at https://ember-atlas-opal.vercel.app/assets/workflow-capture.mp4 (20.24 s), with no people/audio. Anonymous playback is recorded in media-check.json. Owner must confirm official format acceptance and any final edit/caption requirements. |
| Pending | Owner | Verify NASA product documentation links, third-party rights and required portal credits. RESOURCES.md distinguishes observations actually used. |
| Pending | Owner | Challenge, São Paulo Local Event, actual member count, registration, Members tab, same event and no waitlist. No private roster accessed. |
| Pending | Owner / Local Lead | Eligibility of pre-existing scaffolding and actual development dates; retain original history and obtain ruling if unclear. |
| Pending | Owner | Current form labels, character limits, AI instructions, local schedule and deadline. Addendum's stated Nov 15 23:59 São Paulo deadline was not independently verified. |
| Pending | Owner | Use the verified app/media links, confirm media format, supply human contributions, paste portal copy, save, preview and reopen every link. |
| Pending | Owner only | Read terms/privacy, personally accept, select Submit for Judging and capture explicit success state privately. Saving is insufficient. |

Public browser verification evidence is recorded in browser-check.json; media-check.json records anonymous video playback. HTTPS and hostname were verified with the system CA store. Chromium used the validated leaf pin to accommodate the Cloud runtime proxy, as documented in docs/DEPLOYMENT.md.

Verified public browser checks: month buttons, September 2024 primary grid value (5,819 MODIS cell-days), north/MODIS/month observation export (18,038 rows), mobile width and no JavaScript exceptions. Nine Python tests pass, JavaScript syntax check passes, and raw-source credential scan passes. Actual screen captures and a silent video are included; public app and media checks passed. The public flow also verifies that selected aggregate CSV agrees with the observation export and that any supported adjustment is limited to the full area.
