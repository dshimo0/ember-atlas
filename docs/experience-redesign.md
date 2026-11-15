# P0/P1 experience release

This release implements the accepted UX audit priorities on the existing static/Leaflet application. It preserves the scientific products, source shards, calibration, chronological split and exports.

| Priority | Change | Acceptance evidence |
| --- | --- | --- |
| P0 | Header reflow, touch targets, compact numerical labels | `scripts/check_experience.py`, three viewport captures, accessibility checks |
| P0 | Mobile pitch progress and SVG link semantics | Manual-scroll/URL regression, world-map keyboard checks |
| P0 | Five-scene guided journey | Actual shared calendar, raw product comparison, supported replay/benchmark, reset and keyboard navigation |
| P0 | Pitch opening, evidence and closing | Nine sections from release artifacts; source/scope and stronger scalar remain visible |
| P1 | Dedicated Methods & Data | Direct load/refresh, legacy-anchor compatibility, source cards, transformation, residuals and reproducibility |
| P1 | Map/calendar hierarchy | Region/month controls, quantitative occupancy key, overlay opacity, map fullscreen and labeled calendar intensity |
| P1 | Editorial About and NASA imagery | Verified creator and personal site; dated local NASA assets with SHA-256/attribution |

Explore opens on Pantanal/September 2024; the guide introduces the problem before asking visitors to inspect the workflow. Scientific detail is progressive and URL-restorable. The same analytical instances and selected mask/UTC scope drive every mode.

Image provenance: [editorial-imagery.json](../web/assets/editorial-imagery.json). The global Blue Marble is explicitly a 2007 editorial composite. The Pantanal photograph is September 1, 2024 true color, separate from monthly FIRMS counts and occupancy. No current incident or physical validation is inferred.

Source `5df68c7ddfb8d5586c92c330c9ee20caf52fa902` was deployed and anonymously verified at https://ember-atlas-opal.vercel.app. [Executed identity](../submission/experience-release.json) records the deployment and immutable data registry. All 50 public regional browser groups, 15 route/viewport groups, three About viewport groups, 25 Python tests and five Node test modules passed. The targeted axe checks found zero violations of the selected WCAG rules across the five pages at three sizes; this is not accessibility certification. The nine-page PDF and actual 30.0-second silent recording were fetched anonymously and matched local release bytes.

The public retest exposed a queued mobile pitch scroll callback replacing an in-flight Explore URL. The callback now checks the active route; the regression explicitly opens all eight SVG links with the keyboard.

Original science remains in `submission/transition-release.json`. No new ground-truth, uncertainty, observation-coverage or causal sensor claim is introduced. Physical-device and assistive-technology checks, a human timed rehearsal and official submission compliance remain owner actions. The 395-word notes have a measured 176.2-second synthesized read at 180 words/minute, not a human rehearsal.

Current visual release: [P2/P3 executed report](../submission/visual-release.json). The P0/P1 identity above remains historical evidence.
