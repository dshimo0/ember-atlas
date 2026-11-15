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

Executed source/deployment identity, tests and remaining limits will be recorded in `submission/experience-release.json` after production verification. Existing scientific evidence remains in `submission/transition-release.json`; it is not replaced by screenshots or design claims. No new ground-truth, uncertainty, observation-coverage or causal sensor claim is introduced. Official submission compliance, physical-device testing and human rehearsal remain separate owner checks.
