# Challenge traceability

## Inspection baseline

Input branch: `work`, commit `6fb056e95e11c4a0668e9a73431c0c2f68b76662`. Stack: static HTML/CSS, native JavaScript modules and locally vendored Leaflet 1.9.4. Deployment: Vercel project `ember-atlas`, explicit CLI production deployments from `work`; Git auto-deployment is disabled.

| Requirement | Initial status | Observed evidence |
| --- | --- | --- |
| Root map, filters and CSV | Implemented and verified | Existing signed-out reports; root HTTP 200; preserved source and snapshot |
| 2020–2024 paired SP observations | Implemented and verified | Snapshot SHA, daily manifests, 60 paired months |
| Holdout claim | Implemented and verified | Reproduced daily CSV and validation JSON exactly from raw manifests |
| /demo and /pitch | Missing | Both public routes returned 404 during inspection |
| Selected-month adjusted VIIRS | Implemented and verified | Existing three-series comparison and model tests |
| Explicit reference-scale calendar/time series | Missing | Existing calendar contained separate unscaled sensor counts |
| Regional historical comparison | Missing | Code explicitly withheld subregion baselines despite complete regional daily summaries |
| Regional calibration | Deferred | Full-area factors are not independently validated on either subregion |
| Monthly holdout residuals | Precomputed but not exposed | Source supports all residuals; adjustment worsens February/March 2023 |
| Guided state, share URLs, slide navigation | Missing | No route/state controller |
| Sensitivity diagnostics | Implemented but presentation unverified | Existing diagnostics JSON; no concise UI summary |
| Arbitrary polygons / earlier record | Deferred | Fixed preset workflow and validated 2020–2024 domain take priority |

## Method contract before presentation changes

Target quantity: monthly occupied cell-days. Each globally anchored 0.05° WGS84 cell counts once per UTC day and product, then daily occupied counts are summed. Reference: MODIS C6.1 SP (Terra/Aqua pooled). Candidate: NOAA-20 VIIRS SP multiplied by the frozen quarterly training ratio MODIS / VIIRS. Training: 2020–2022, 36 complete paired months; holdout: 2023–2024, 24 complete paired months. Acceptance requires lower monthly MAE and no worse absolute bias on identical holdout months, with unchanged minimum support. Applicability is the full Pantanal study rectangle, complete months only.

The reference-scale output is adjusted VIIRS on the MODIS-reference scale. MODIS and VIIRS are not summed or averaged. There is no source transition or fused multi-decade record. Missing retrieval remains null; partial months have no adjustment. Raw point coordinates are never adjusted. Subregion baselines may be descriptive within-sensor comparisons on their own fixed masks; regional calibration remains withheld.

## Official guidance check

On 2026-11-15 UTC the official challenge URL and resources page returned HTTP 503. The current guide, deadline, event eligibility and official demonstration format were not verified. The three-minute pitch is a product presentation target, not a confirmed portal rule. Existing owner submission gates remain in submission/RELEASE-CHECKLIST.md. Final implementation and execution evidence will be recorded in docs/release-checklist.md.

## Delivery evidence

| Requirement | Final status | Working evidence |
| --- | --- | --- |
| Three public routes and shared state | Implemented and verified | Native shared loader/model/charts; Vercel rewrites; direct-load/refresh/back/forward checks |
| Five-step guided case | Implemented and verified | Actual controls, reset, raw/reference history, prior-year breakdown and downloads |
| Explicit harmonized quantity | Implemented and verified | Adjusted VIIRS on MODIS-reference scale; 60-month calendar and time series; no product sum or source handoff |
| Reproducible validation claims | Implemented and verified | Exact pipeline reproduction; all 24 residuals recomputed; MAE/bias/RMSE and two worse months |
| Regional descriptive history | Implemented and verified | Full-data summaries; own fixed mask, complete prior years and minimum n=3; independent oracle tests |
| Regional calibration | Deferred with reason | No independent regional fit/holdout evidence; full-area adjustment remains unavailable |
| Map and evidence consistency | Implemented and verified | Same month/area/product mask; exact CSV equality; display-only layers; local fallback |
| Export provenance | Implemented and verified | Immutable source refs and exact downloaded CSV SHA-256 values in manifest |
| Interactive and printable pitch | Implemented and verified | Nine desktop slides; mobile scroll; keyboard, counter, notes, fullscreen; nine-page PDF |
| Human delivery timing | Implemented script, human read unverified | Measured synthesized read 3:05; Team Owner must rehearse human delivery with navigation |
| Official challenge/media compliance | Unverified / owner action | Current official pages return 503; no old deadline or slide cap treated as verified |
| Multi-decade transition, ground truth, arbitrary polygons | Deferred with reason | Current matched five-year rectangle supports defensible overlap evaluation; broader claims require new inputs/evaluation |
| Final submission | Deferred to Team Owner | Roster/eligibility, terms and Submit for Judging remain owner responsibilities |

Reports: [routes](../submission/routes-check-public.json), [analytical workflow](../submission/judging-check-public.json), [release identity](../submission/product-release.json), [resources](../submission/resource-check.json). Current challenge ambition exceeds the released five-year overlap: no multi-decade fused continuation or validated sensor handoff is claimed.
