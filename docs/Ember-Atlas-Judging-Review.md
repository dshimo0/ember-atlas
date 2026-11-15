# Scientific and product release review

[Explore](https://ember-atlas-opal.vercel.app/) · [Pantanal replay](https://ember-atlas-opal.vercel.app/demo?region=pantanal&view=replay&benchmark=1&month=2024-09) · [Pitch](https://ember-atlas-opal.vercel.app/pitch)

Input branch `work` at `f695d77`. The release retains static native modules, Leaflet, the existing host and original frozen scientific inputs. Tested source/deployment identity is recorded in [transition-release.json](../submission/transition-release.json).

| Finding | Implemented result | Verification |
| --- | --- | --- |
| No explicit continuity exhibit | January 2023 replay; observed MODIS before and frozen adjusted VIIRS after; separate observed holdout benchmark | Cutoff source/table/CSV and toggle restoration checks |
| Seasonal only compared with unadjusted | Training-only scalar baseline, identical area/months, MAE/bias/monthly residuals and peak-six test | Python/JS cross-recomputation and immutable evaluation |
| Better scalar could be hidden | Explicit scalar MAE 175.3 versus seasonal 199.7; no holdout-based method reselection | First validation card, methods table and pitch |
| Map was a sampled point layer | Full-data occupied days/cell for named sensor; optional sampled points | Cell CSV sum equals map and common-grid totals |
| One observed study area | Eight ordered presets with actual geometry and source-specific SP/NRT snapshots | All eight bounds, observations and matching CSVs on desktop/mobile |
| No older public MODIS | Full requested November 2000–December 2019 backfill combined with unchanged 2020–2024 inputs | 1,400 retrieved windows; MODIS 8,827 retrieved days through 2024-12-31 |
| Processing-level ambiguity | Separate NRT UTC window, retrieval time and partial-month view; no join | Product suffix, clipped dates and unsupported calibration checks |
| Historical hindsight | Replay baseline uses earlier complete matched-domain months only; target/future excluded | Source-tagged prior entries and model regression cases |
| Regional calibration leakage | Seven new regions and Pantanal subareas remain raw; no factor without local multi-year evaluation | Model and browser withholding checks |
| Pitch lacked the scientific transition story | Replay → independent fitting-period benchmark → scalar comparison → peak error → eight-area world map | Direct slide links, eight Explore links and nine-page print |

The scalar is a stronger baseline on the existing holdout, which is evaluation evidence. Seasonal remains the frozen publication rule. Six peak months are selected by observed MODIS activity, not residuals. Their scalar/seasonal MAE is 404.6/534.6 cell-days/month. September seasonal replay remains 16.2% below MODIS. No result is global, ground-truth or detection accuracy.

New source inputs are stored in 35 deterministic archives containing 3,032 original CSV/manifest files. Member hashes and refusal to overwrite changed inputs preserve provenance and a reviewable Git diff. Dataset summaries, shards, registry and evaluation are versioned. The original snapshot, validation, daily fit input and factors remain unchanged.

Execution evidence: [eight-region local checks](../submission/eight-region-check-local.json), [public checks](../submission/eight-region-check-public.json), [coverage](../submission/eight-region-coverage.md), [integrity](../submission/integrity-check.json), and screenshots named `region-…-desktop/mobile.png` plus `transition-demo/pitch/calendar-…png`. Fifteen Python tests and nineteen Node model cases cover the pipeline, scalar protocol, replay source, missingness, grid reconciliation and source archive recovery. Mobile is touch/viewport emulation. HTTPS uses system CA validation and system-validated proxy leaf pins for Chromium automation; production code includes no certificate bypass.

Remaining open items: multi-year SP archive and independent regional calibration for seven areas; new outer evaluation for method selection; usable observation masks; ground truth; SP/NRT transition validation; arbitrary polygons/biome mask; physical-device testing; human roster/rehearsal and current official guide/media acceptance. Final terms and portal submission remain Team Owner responsibilities.

## Pantanal expansion retest

The added Pantanal SP source window is January 2025–July 2026: 19 complete paired months. Unadjusted/scalar/frozen-seasonal MAE is 399.4/89.7/70.8 cell-days/month; seasonal signed bias is +67.4. These diagnostic outputs do not extend the 2020–2024 adjustment domain. The registered requirement is 24 fresh complete months. All released observations and daily grid/native totals were reconciled against monthly shards; the evaluation was recomputed from daily evidence. The browser suite additionally checks the new January 2025 shard, sensor filtering, clipped manual dates and missing adjustment. See the current regional-artifact and browser reports for execution identity. Other regional matched histories are still being acquired and are not represented as completed evaluation.
