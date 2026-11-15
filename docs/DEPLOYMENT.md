# Vercel deployment

Production: https://ember-atlas-opal.vercel.app/ · /demo · /methods · /about · /pitch

Authoritative source/deployment identity, HTTP checks and public execution reports are in `submission/transition-release.json`. Branch `work`; PR #2 remains open. Git auto-deployment is not configured; authorized CLI production deployment is the established workflow.

## Architecture

Static English HTML/CSS and native modules, locally vendored Leaflet 1.9.4, output `web`, no build/install command or new backend. `vercel.json` preserves root/asset paths and rewrites `/demo`, `/methods` and `/pitch` to the same index; `/about` uses its static editorial document, with trailing slashes removed. Shared state/loaders/models/charts restore direct URLs and browser history.

Visitors load versioned regional SP/NRT snapshots from versioned release files and never supply a FIRMS key or contact FIRMS. OpenStreetMap supplies interactive raster tiles; local Natural Earth geography covers all eight extents if tiles fail. No offline OSM tile cache is included. Original snapshots and frozen validation remain available at existing paths.

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

The signed-out suite checks all eight SP and NRT presets on desktop and touch-enabled mobile: intended geometry fit, actual normalized observations, exact CSV records, map-cell sums and cell CSVs, source-change cutoff, benchmark state, full available MODIS calendar (309 months in the Pantanal expansion), early missing VIIRS, zero day, regional withholding, shared state and forced tile fallback. Presentation direct loads, refresh, world links, keyboard operation and nine-page printing are checked. Separate public checks verify source/asset hashes and anonymous video playback. Mobile remains emulation, not a physical-device claim.

HTTPS and hostnames use the system CA store. Chromium in this Cloud proxy uses only independently system-validated leaf-key pins, never a global certificate bypass; production has no such flags. The production alias is verified anonymously even if unique preview deployment URLs use provider authentication.

The actual 30-second silent recording is at `/assets/workflow-capture.mp4`; the nine-page PDF is `/assets/ember-atlas-pitch.pdf`. Neither establishes official demonstration-format acceptance. Current guide, eligibility, human roster/rehearsal, terms and final submission remain Team Owner actions.

## Selective reproducible update

`python scripts/source_archives.py unpack` restores preserved original and derived source files. `python scripts/build_regions.py --regions pantanal` rebuilds only Pantanal while retaining other published registry references. A full rebuild evaluates all available regional source windows. Publication gates stay separate from raw retrieval coverage. Acquisition progress files are temporary and excluded from commits.

## Expanded snapshot hosting

Large observation shards are pinned to a full public Git commit in the same repository. The browser allows only that exact repository/commit path and checks uncompressed SHA-256 before using a shard. Current metadata and the default September 2024 Pantanal case remain local on Vercel. Earlier published local data URLs remain served; a monotonic path catalog protects them. Unpublished superseded files stay in Git and are excluded from the constrained static upload. No visitor API key or live FIRMS call is used.

Publish the complete data commit first, then run `python scripts/pin_release_data.py FULL_DATA_COMMIT`, rebuild the coverage/evaluation documents, verify the actual upload size with Vercel's dry run, commit the pinned metadata/configuration and deploy that source commit. `data/pinned-data-release.json` records the immutable data commit and current registry. A failed external shard leaves observation occupancy unavailable, while local aggregate evidence and provenance remain usable.
