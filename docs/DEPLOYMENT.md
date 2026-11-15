# Vercel deployment

Public application: https://ember-atlas-opal.vercel.app/

Final application source, production deployment ID, anonymous route checks and asset hashes are recorded in [transition-release.json](../submission/transition-release.json). Branch: `work`. PR #2 remains open; production uses explicit authorized CLI deployment, independently of merge status.

## Architecture

Static English frontend, Framework Other, output `web`, no build/install command. Leaflet 1.9.4 is locally vendored. OpenStreetMap supplies normal interactive raster tiles; locally stored Natural Earth country boundaries, rivers and settlements provide the fallback. No tile prefetch or offline tile cache is implemented.

The versioned FIRMS snapshot, daily summaries and monthly observation shards are served from the same deployment. Ingestion scripts, raw inputs and credentials are excluded by `.vercelignore`. The public frontend does not require live FIRMS access. The existing Vercel Hobby project is unchanged; no paid add-ons or server functions were added.

## Repeat deployment

Project `ember-atlas` belongs to `dscbest-1597s-projects`. Verify the target before deploying:

```sh
python -m unittest discover -s tests
node --test tests/test_*.mjs
node --check web/app.js
node --check web/geographic-map.mjs
vercel project inspect ember-atlas --scope dscbest-1597s-projects --non-interactive
vercel deploy --dry --json --project ember-atlas --scope dscbest-1597s-projects
vercel deploy --prod --yes --project ember-atlas --scope dscbest-1597s-projects
```

Git auto-deployment is not configured. Git push alone does not update production. Keep FIRMS_MAP_KEY in the separate ingestion environment.

## Executed checks

Signed-out desktop and touch-enabled mobile emulation passed initial load, map zoom/pan/scale/fit, month/date/area/sensor changes, CSV reconciliation, subregion adjustment withholding and missing/zero/partial data checks. Separate contexts aborted tile requests and confirmed that the local map, FIRMS overlays and downloads remained available.

The default September observation export contains 125,055 rows; the full-period aggregate export contains 120 rows. Northern MODIS September contains 18,038 rows. Public assets match repository bytes. The original scientific snapshot, validation, fitting rules and export model are byte-for-byte unchanged.

HTTPS and hostname validation used the system CA store. Chromium automation used the independently validated leaf-key pins for the application and tile provider to accommodate the Cloud proxy; no global certificate-error bypass was used. Mobile checks use browser emulation, not a physical device.

Actual screen recording: https://ember-atlas-opal.vercel.app/assets/workflow-capture.mp4 . Runtime is 29.64 seconds, with no people/audio. Public playback is recorded in `submission/media-check.json`. Official portal media format and final submission remain Team Owner checks.

## Route and presentation release

`vercel.json` rewrites `/demo` and `/pitch` to the same `index.html` and removes trailing slashes. Existing root, data and asset URLs are preserved. Native modules handle query-state restoration and browser history; no new backend or framework was added. For equivalent local direct-route behavior run `python scripts/serve.py`.

Run both `scripts/check_judging_flow.py` and `scripts/check_routes.py` with `BASE_URL` set to the actual production origin. The latter verifies direct loads/refreshes for all routes, guided steps, share state, manifest hashes and pitch controls/print. The public route report rejects unexpected HTTP errors and JavaScript exceptions. Deployment includes only web assets/configuration. The published presentation screenshot is an actual screen capture; timing audio is temporary and not deployed.

## Eight-region replay release

The current source identity and public checks are in submission/transition-release.json and submission/eight-region-check-public.json. The frontend lazily loads checksum-verified regional SP/NRT snapshots from the same static deployment. Visitors never contact FIRMS. Earlier MODIS source archives remain in the repository, excluded from Vercel upload; public normalized month shards remain reproducible from their archive/member hashes. No regional calibration or NRT/SP join is inferred by deployment.

Use `python scripts/serve.py` and `BASE_URL=… python scripts/check_eight_regions.py` for current browser acceptance. Previous browser script names are compatibility entry points for that same suite. The suite verifies every preset on desktop/mobile, source-change cutoff, full 290-month Pantanal calendar, missing VIIRS history, SP/NRT separation, cell/observation/monthly CSVs, manifest hashes and fallback geography. Screenshot and print artifacts are actual browser outputs. HTTPS proxy pins are confined to the test runner.
