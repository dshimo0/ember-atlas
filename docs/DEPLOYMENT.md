# Deployment runbook

Architecture: static English dashboard + versioned gzip snapshot. Python 3.10+ standard library ingestion is separate; the browser has no FIRMS credentials, backend or live NASA dependency. No third-party runtime libraries, fonts or tiles are used. CI runs Python tests. No paid resources were created.

## Vercel (preferred)

Import https://github.com/dshimo0/ember-atlas, select the release branch, use Framework Other, output `web`, and no build/install command. `vercel.json` records these settings. Disable authentication for the production domain. Do not add FIRMS_MAP_KEY to the web project. Verify anonymous HTTPS in a fresh browser and repeat the local flow in submission/browser-check.json before declaring deployed.

Observed blocker: Vercel team `team_dtsjqnxFZUPzltgqfxVNqXJ2` returned 403 on project creation. No Vercel CLI credentials were present. Owner must import this repository or grant create/deploy permission to the connection.

## Existing DigitalOcean host alternative

Only an existing n8n host was visible; no SSH credential was available. With authorized SSH access and a DNS name, upload `web/` to a new isolated static document root and serve with Caddy or nginx + TLS. Do not replace n8n configuration. Switch a release symlink atomically after local checks. The public web root contains only `web/`; raw ingestion secrets belong in a separate chmod-600 runtime environment file, outside the document root. No new paid Droplet is required for the static site. Any new resource requires an explicit budget under the execution instructions.

## Ingestion recovery

The scoped FIRMS key initially worked, then requests returned HTTP 400 `Invalid MAP_KEY.` After the environment configuration was published, availability and ingestion worked again with the configured secret. The cause of the earlier interruption is unconfirmed. `python scripts/resume_matched.py` requests only uncovered UTC days in the fixed 2020–2024 domain, with pacing and existing bounded retries. It does not overlap the previously acquired pilot. Never send keys in chat or commit them. Rebuild the snapshot and rerun the frozen split after resumption; read submission/RESULTS.md for actual completeness and acceptance.
