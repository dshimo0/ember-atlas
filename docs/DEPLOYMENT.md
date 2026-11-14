# Vercel production release

Public application: https://ember-atlas-opal.vercel.app

Verified on 2026-11-14 UTC. Vercel reports deployment `dpl_2fBKriwNqyNARh73kgMedjB5yazX` READY in production. Application source commit: `6ce87d3790ec6c9ae1ba1c9a1e0d92da9d9a729a`, branch `work`. Subsequent evidence/documentation commits do not change the hosted application. The PR remains open; no merge was performed.

## Architecture and account

Static English dashboard + versioned gzip snapshot, Framework Other, output `web`, no build/install command. Production alias opens anonymously; preview/deployment authentication settings were not weakened. Ingestion remains separate. No FIRMS key, raw CSVs, ingestion scripts or private runtime configuration were uploaded. `.vercelignore` and a dry run restricted upload to the web directory and Vercel configuration. No paid add-ons or Droplets were created; the project uses the existing Hobby team.

CLI 65.16.0 is installed and authenticated as `dscbest-1597`. Project `ember-atlas` (`prj_69e3y1AOgoBBplTu6CwizTkMSoEb`) belongs to `dscbest-1597s-projects` (`team_dtsjqnxFZUPzltgqfxVNqXJ2`). The existing Vercel plugin's documentation search and authenticated team listing succeeded. A separate Codex CLI MCP entry could not be added because `/home/agent/.codex` is read-only; the managed MCP connection remains available. CLI login resolved the earlier project-creation 403.

## Repeat a release

From the repository root, review the exact branch and commit, run tests and inspect the explicit target:

```sh
python -m unittest discover -s tests
node --check web/app.js
vercel project inspect ember-atlas --scope dscbest-1597s-projects --non-interactive
vercel deploy --dry --json --project ember-atlas --scope dscbest-1597s-projects
vercel deploy --prod --yes --project ember-atlas --scope dscbest-1597s-projects
```

Only CLI deployment is configured. Git push alone does not update production; no Git auto-deployment connection was enabled. Inspect the deployment after release and repeat the browser flow against its production URL. Do not add FIRMS_MAP_KEY to the web project. Keep prior snapshots available for audit and publish a new index only after validation.

## Executed public checks

Anonymous HTTPS returned HTTP 200 with the expected application. Fresh headless Chromium exercised September 2024 selection, the 5,819 MODIS cell-day reference, northern MODIS observation export (18,038 records), matching aggregate export, full-area supported adjustment, mobile width and absence of JavaScript exceptions. See `submission/browser-check.json`. TLS and hostname were verified with the system CA store. This Cloud runtime's Chromium did not trust its local proxy CA; its scripted check used the exact leaf public-key pin obtained from that independently system-CA-validated HTTPS connection. No global certificate-error bypass was used and the app's TLS configuration was not changed.

Public media: https://ember-atlas-opal.vercel.app/assets/workflow-capture.mp4 . A downloaded copy matches the committed media checksum. Browser playback evidence is in `submission/media-check.json`; official portal format compliance remains an owner gate.

The deployment used a basic build machine, with a six-second build and five-second post-build stage. There are no server functions or ingestion jobs in this Vercel project. No paid observability add-on was configured.

## Ingestion recovery

The configured FIRMS key initially worked, then requests returned `Invalid MAP_KEY.` After the environment configuration was published, ingestion worked again; the cause of the interruption is unconfirmed. `python scripts/resume_matched.py` fills only uncovered UTC days in 2020–2024, preserving successful extracts and applying pacing and bounded retries. All days for the paired products are now retrieved. Rebuild and rerun the frozen split before any future snapshot release. NASA credentials remain restricted to the ingestion environment, outside the public web project.
