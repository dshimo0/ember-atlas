# Vercel deployment

Production: https://ember-atlas-opal.vercel.app/ · /demo · /pitch

Authoritative source/deployment identity, HTTP checks and public execution reports are in `submission/transition-release.json`. Branch `work`; PR #2 remains open. Git auto-deployment is not configured; authorized CLI production deployment is the established workflow.

## Architecture

Static English HTML/CSS and native modules, locally vendored Leaflet 1.9.4, output `web`, no build/install command or new backend. `vercel.json` preserves root/asset paths and rewrites `/demo` and `/pitch` to the same index, with trailing slashes removed. Shared state/loaders/models/charts restore direct URLs and browser history.

Visitors load versioned regional SP/NRT snapshots from the same deployment and never supply a FIRMS key or contact FIRMS. OpenStreetMap supplies interactive raster tiles; local Natural Earth geography covers all eight extents if tiles fail. No offline OSM tile cache is included. Original snapshots and frozen validation remain available at existing paths.

Root ingestion data, source archives, scripts, tests and `.env*` files are excluded by `.vercelignore`. Source evidence remains public in the repository. The existing Hobby project, team and infrastructure are unchanged; no paid service or server function is added.

## Repeat workflow

```sh
python -m unittest discover -s tests
node --test tests/test_*.mjs
python scripts/check_release_integrity.py
vercel project inspect ember-atlas --scope dscbest-1597s-projects --non-interactive
vercel deploy --dry --json --project ember-atlas --scope dscbest-1597s-projects
vercel deploy --prod --yes --project ember-atlas --scope dscbest-1597s-projects
BASE_URL=https://ember-atlas-opal.vercel.app python scripts/check_eight_regions.py
```

Attach the committed source SHA to deployment metadata. For local equivalent routing use `python scripts/serve.py`. Browser checks require Playwright, Chromium and pdfinfo; previous browser script names are compatibility entry points to the current eight-region suite.

## Executed evidence

The signed-out suite checks all eight SP and NRT presets on desktop and touch-enabled mobile: intended geometry fit, actual normalized observations, exact CSV records, map-cell sums and cell CSVs, source-change cutoff, benchmark state, 290-month MODIS calendar, early missing VIIRS, zero day, regional withholding, shared state and forced tile fallback. Presentation direct loads, refresh, world links, keyboard operation and nine-page printing are checked. Separate public checks verify source/asset hashes and anonymous video playback. Mobile remains emulation, not a physical-device claim.

HTTPS and hostnames use the system CA store. Chromium in this Cloud proxy uses only independently system-validated leaf-key pins, never a global certificate bypass; production has no such flags. The production alias is verified anonymously even if unique preview deployment URLs use provider authentication.

The actual 30-second silent recording is at `/assets/workflow-capture.mp4`; the nine-page PDF is `/assets/ember-atlas-pitch.pdf`. Neither establishes official demonstration-format acceptance. Current guide, eligibility, human roster/rehearsal, terms and final submission remain Team Owner actions.
