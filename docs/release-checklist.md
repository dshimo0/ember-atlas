# Product and presentation release checklist

Scientific input: `snapshot-19621fa88d40.json.gz`; validation: `validation-ba55acfc7909.json`. Input source branch `work` at `6fb056e95e11c4a0668e9a73431c0c2f68b76662`. Deployment source and final public evidence are recorded in [product-release.json](../submission/product-release.json).

| Status | Requirement | Evidence |
| --- | --- | --- |
| Verified | Preserve science and stack | Static native modules/Leaflet; original input/validation bytes retained; daily calendar and validation reproduced exactly from committed manifests |
| Verified | Recompute claim without refitting | 24 holdout residuals recomputed from frozen quarterly factors; MAE, bias and RMSE reconcile; 13 Node tests |
| Verified | Routes and state | `/`, `/demo`, `/pitch` direct loads/refreshes; shared nav; URL/back/forward tests |
| Verified | Complete guided case | Five actual-state steps, reset, raw/reference history and matching exports |
| Verified | Regional analysis | Own-mask prior-year medians; no inherited adjustment; north/south tests |
| Verified | Map | OSM, source/time/FRP/confidence tooltips, circle/diamond markers, display-only layer switches, fit/scale/pan/zoom; forced failure activates local geography |
| Verified | Evidence downloads | 125,055 September observations; 120 full-period aggregate rows; record and cell-day equality with pinned observations; manifest hashes equal actual downloaded CSV bytes |
| Verified | Missingness | Retrieved zero, partial September interval and missing December 2019 remain distinct |
| Verified | Presentation | Nine sections, previous/next, keyboard, slide URLs, notes, fullscreen, mobile scroll, nine-page print PDF |
| Verified | Desktop/mobile execution | Fresh signed-out Chromium contexts; screenshots and JSON reports in submission/; mobile is touch/viewport emulation |
| Verified | Pipeline checks | Nine Python tests; exact reproduction; frozen source hashes and credential checks recorded in product-release.json |
| Verified | Timed script | 454 words; synthesized English read 184.646 seconds at eSpeak NG 1.51, 180 wpm; no audio published |
| Pending — Team Owner | Human pitch rehearsal | Time delivery with slide navigation and adapt pacing to the permitted event format |
| Pending — Team Owner | Official submission guidance | Current challenge, resources, event and legal pages returned 503; do not infer deadline or official media duration/slide count |
| Pending — Team Owner | Roster, eligibility and rights | Confirm human contributions, member/event registration, pre-existing-work eligibility, repository license and required portal resource wording |
| Pending — Team Owner only | Terms and submission | Review current guide, confirm demonstration format, accept terms and personally submit for judging; verify success state |

The three-minute pitch and nine-page PDF are presentation materials. Neither is asserted to satisfy the official Project Demonstration format. [Resource check](../submission/resource-check.json) records actual HTTP outcomes and the current unresolved guidance. Existing [submission gates](../submission/RELEASE-CHECKLIST.md) remain applicable.

Re-run locally with `python scripts/serve.py`, `python -m unittest discover -s tests`, `node --test tests/test_*.mjs`, `BASE_URL=http://127.0.0.1:8000 python scripts/check_judging_flow.py`, and `BASE_URL=http://127.0.0.1:8000 python scripts/check_routes.py`. Browser checks require Playwright, Chromium and pdfinfo. Use the deployed HTTPS origin for the release retest. Intentional tile aborts are isolated from normal network checks.
