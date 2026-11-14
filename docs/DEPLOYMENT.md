# Deployment runbook

Architecture: static English dashboard + versioned gzip snapshot. Python 3.10+ standard library ingestion is separate; the browser has no FIRMS credentials, backend or live NASA dependency. No third-party runtime libraries, fonts or tiles are used. CI runs Python tests. No paid resources were created.

## Vercel (preferred)

Import https://github.com/dshimo0/ember-atlas, select the release branch, use Framework Other, output `web`, and no build/install command. `vercel.json` records these settings. Disable authentication for the production domain. Do not add FIRMS_MAP_KEY to the web project. Verify anonymous HTTPS in a fresh browser and repeat the local flow in submission/browser-check.json before declaring deployed.

Observed blocker: Vercel team `team_dtsjqnxFZUPzltgqfxVNqXJ2` returned 403 on project creation. No Vercel CLI credentials were present. Owner must import this repository or grant create/deploy permission to the connection.

## Existing DigitalOcean host alternative

Only an existing n8n host was visible; no SSH credential was available. With authorized SSH access and a DNS name, upload `web/` to a new isolated static document root and serve with Caddy or nginx + TLS. Do not replace n8n configuration. Switch a release symlink atomically after local checks. The public web root contains only `web/`; raw ingestion secrets belong in a separate chmod-600 runtime environment file, outside the document root. No new paid Droplet is required for the static site. Any new resource requires an explicit budget under the execution instructions.

## Ingestion recovery

The scoped FIRMS key initially worked, then NASA returned HTTP 400 `Invalid MAP_KEY.` Availability later returned 401. Reactivate/replace FIRMS_MAP_KEY in the execution environment secret store, then run availability and resume bounded fetches. Never send the key in chat or commit it. Cache checksums allow resumption. Freeze a new input snapshot and rerun the same split before publishing an adjustment. Current release has gaps; do not label 2023 or 2024 as complete years.
