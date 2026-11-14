# Vercel deployment

Public application: https://ember-atlas-opal.vercel.app/

Application source: `4d665138201c4941cd9dc7e61e18311d8a5957cc`, branch `work`. Production deployment: `dpl_GgmKyKszTUz6ycwty9NeKmfxYdnC`. Verification: `submission/judging-release.json` and `submission/judging-check-public.json`. Subsequent evidence/documentation commits do not change the hosted application. The PR remains open.

## Architecture

Static English frontend, Framework Other, output `web`, no build/install command. Leaflet 1.9.4 is locally vendored. OpenStreetMap supplies normal interactive raster tiles; locally stored Natural Earth country boundaries, rivers and settlements provide the fallback. No tile prefetch or offline tile cache is implemented.

The versioned FIRMS snapshot, daily summaries and monthly observation shards are served from the same deployment. Ingestion scripts, raw inputs and credentials are excluded by `.vercelignore`. The public frontend does not require live FIRMS access. The existing Vercel Hobby project is unchanged; no paid add-ons or server functions were added.

## Repeat deployment

Project `ember-atlas` belongs to `dscbest-1597s-projects`. Verify the target before deploying:

```sh
python -m unittest discover -s tests
node tests/test_model.mjs
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
