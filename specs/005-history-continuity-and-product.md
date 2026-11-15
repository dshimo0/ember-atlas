# Historical continuity, source review and product presentation

Status: accepted direction; individual implementation gates remain pending.
Reviewed 2026-11-15. Extends spec 004; does not overwrite frozen results or the
registered regional evaluation protocol. Read this before implementing new acquisition,
heatmaps, platform bridges or observation-time adjustments.

## Product promise

Preserve historical fire-activity context across the transition from MODIS to VIIRS.
Estimate a comparable activity series on an explicitly chosen reference scale, while
retaining native VIIRS spatial detail for inspection. This is cross-sensor continuity,
not a forecast of future fires or reconstruction of small fires MODIS never observed.
MODIS and VIIRS are instruments carried by multiple platforms; retain platform identity.

## Review of the Qwen recommendations

| Recommendation / assertion | Decision and correction |
| --- | --- |
| Ember only has ingestion and daily counts | Stale relative to the inspected work release: calendar, web app, frozen calibration, replay and exports already exist. Audit branch and commit before assessing status. |
| Author answered discussion 1879 | Confirmed: m-compagnucci posted on November 13, after the Navigator's November 12 answer. The accepted-answer badge still points to the Navigator; read both. |
| Monthly calendar | Adopt as primary. Keep daily ingestion and UTC lineage; aggregate for patterns. Weekly view is secondary. |
| Either reference scale | Author accepts either when justified. Preserve the existing reference-scale occupied-cell-day metric; do not silently replace it with native monthly detections. |
| NOAA-20/21 continuity | Include a platform-specific continuity workstream. NOAA-21 adjustment requires its own evidence and protocol, not a copied NOAA-20 factor. |
| Portolan mirror bypasses keyed Area API | Promising alternative acquisition route. Verify schema, fidelity, coverage, bandwidth and snapshot identity before using it for scientific results. |
| All-time aggregate immediately solves harmonization | Reject as an assumption. Inspect whether sensor, platform, time and quality dimensions survive aggregation. Visualization aggregates cannot replace detection-level calibration inputs. |
| Solar-time correction is approximately 60 lines | Computing a time covariate is easy; identifying a correction is a research problem. Adopt diagnostics first, gate any correction on independent validation. |
| Orbital drift explains another project's error | Unsupported causal attribution. Do not repeat it. Fire regime, sampling, cloud, sensor response and fitting choices can all contribute. |
| Competitors ignore schedules / lack scientific holdout | Not established. Reviewed material includes platform/day-night handling and published held-out evaluation. Do not claim exclusivity. |
| Rebuild the app and remove nine regions | Preserve the existing app and nine-region scope. Prioritize Pantanal and Chilecito end-to-end; other regions expose actual readiness. |
| Exact submission length, deadline and AI declaration | Verify against the current official submission guide and local event. A pasted recommendation is not sufficient authority. |

## Source authority

- Author response: https://github.com/nasa/spaceapps/discussions/1879
  Supports justified scale choice, FIRMS archive, future platform continuity and a
  monthly pattern-oriented calendar. Do not interpret it as requiring a specific model.
- Navigator regional-focus advice: https://github.com/nasa/spaceapps/discussions/2016
- Mirror publisher: https://source.coop/portolan-mirrors/firms-catalog
  NASA remains authoritative; the mirror is third-party distribution.
- NASA drift notice: https://landweb.modaps.eosdis.nasa.gov/displayissue?id=1254
  Reports geometric and diurnal sampling impacts, with fire-product effects under
  investigation. Exact future retirement dates are not pinned by this specification.

## M1: Optional mirror adapter

Deliver a bounded adapter alongside the existing Area API path. Do not interrupt or
discard running downloads. Start with one year and the unchanged Chilecito rectangle.
Avoid an unrestricted all-years/global query as the first operation.

Acceptance:

1. Inspect Parquet metadata and actual field types, CRS, timestamp semantics, platform
   identifiers, processing classes, nulls and per-product available dates. Record the
   schema and query; fail explicitly when required columns are absent.
2. Explicit annual URLs and predicate pushdown; measure bytes/time before expanding.
   Remote wildcard support and small download volume are not assumed. Querying remotely
   still transfers data. Configure timeout, retries and a resumable per-year cache.
3. Preserve source URL, retrieval timestamp, upstream version/ETag when available,
   extraction checksum and immutable local extract. The mirror replaces NRT with SP;
   pin snapshots so a later query cannot silently change evaluation inputs.
4. Keep platform, sensor, quality and day/night in groups. Retain detection coordinates
   and UTC day to reproduce occupied cell-days. Monthly count and FRP sums are separate
   diagnostics; summed FRP samples are not energy or burned area.
5. Null fire type remains unknown, not vegetation. Retain unknown records with explicit
   status; report the effect of type filtering by processing class. Apply confidence
   rules per product; never compare VIIRS classes numerically with MODIS confidence.
6. Reconcile matched product/vintage/geometry/time samples with authoritative FIRMS.
   Compare IDs or coordinates/times/platforms, duplicate rules, counts and cell-days.
   Explain discrepancies before approving use; geographic boundaries must be identical.
7. Do not change Pantanal bounds to the smaller example SQL rectangle. Any new polygon
   gets a new geometry ID and separate calibration/baseline.
8. The all-time A5 aggregate, file sizes and alleged fleet-jump ratios in the supplied
   recommendation remain unverified here. Never transfer those ratios to our regions
   or label all interannual change as sensor artifacts.

## T1: Observation-schedule diagnostics

Compute approximate local mean solar hour as `(UTC decimal hour + longitude/15) mod 24`.
Keep UTC acquisition dates for the existing daily metric. Local-date rollover is retained
separately if needed. This is not civil time or apparent solar time; no timezone/DST
conversion is appropriate. Handle midnight with circular statistics or day/night strata.

Deliver a platform-by-year/month distribution of detection times, stratified by region
and day/night, with sample sizes. Label it **times of detected hotspots**: detections
alone do not measure all observation opportunities or the true diurnal fire cycle.

Before an adjustment can ship, require an identifiable model and observation-exposure
evidence (swaths/usable coverage or a justified independent reference), overlap in time
strata, region/season controls and predeclared temporally separated evaluation. Compare
against the same scalar/seasonal baselines and report peak bias and anomaly agreement.
No correction is published merely because the corrected trend looks flatter. Drift
coincides with calendar time and can be confounded with real changes in fire activity.

## U1: Calm calendar and map

- Primary screen: area/period controls, one interpretation, month-by-year calendar and
  map. Methods and diagnostics use progressive disclosure. Keep critical provenance near
  its metric; avoid a wall of caveats or unsupported reassuring claims.
- Activity heatmap: perceptually ordered color-blind-safe sequential palette. Label
  linear versus log scaling, units and domain. Hold the scale fixed within comparisons.
- Anomaly heatmap: a separate diverging palette centered on the declared neutral value
  (zero difference or ratio one). Show reference years/n and the calculation in tooltip
  and table; baseline support follows the registered contract.
- Missing, retrieved zero and partial periods have distinct symbols/textures. Never fill
  an unobserved month with seasonal interpolation. Partial periods are not full months.
- Map: aggregate all included detections into the existing observed cell metric. Preserve
  optional point inspection. Do not imply a monthly regional factor creates calibrated
  per-pixel values. Keep legend, attribution, actual footprint and accessible fallback.
- Acceptance: keyboard month selection, table alternative, readable 390px layout, no
  horizontal document overflow, synchronized export and reproducible shared state.

## B1: Repository identity and delivery evidence

README starts with the approved Ember Atlas logo, a one-sentence purpose, live product
links, an actual product screenshot and current coverage/validation status. Use the
existing approved logo asset, not a competitor asset or a newly invented NASA-like seal.
No approved logo asset was found in the inspected checkout; logo insertion remains
blocked on obtaining that file. Keep the project name visible meanwhile.

Distinguish deployed capabilities, local experiments and planned additions. Link specs,
data sources, method, evaluation and execution commands. Do not promise global validity.
The default GitHub branch must eventually contain the current README; a stale default
branch can make reviewers assess an obsolete implementation.

## Delivery order and done criteria

| Order | Deliverable | Done when |
| --- | --- | --- |
| 1 | Pantanal end-to-end + Chilecito case | Actual available history, synchronized calendar/map, contextual July 2026 analysis and exports work |
| 2 | M1 mirror feasibility | Schema + fidelity report + bounded performance measurement pass; adapter outputs preserve original metric |
| 3 | Regional evaluation | Existing registered gates pass; legacy runner outputs alone do not authorize publication |
| 4 | U1 UI and B1 README | Desktop/mobile/keyboard checks, correct status, approved logo and reproducible product screenshot |
| 5 | T1 schedule diagnostic | Reproducible time distributions and confounding limitations; correction remains gated |
| 6 | Platform expansion | Separate S-NPP/NOAA-20/NOAA-21 overlap evidence and versioned transfer protocol |

Do not block submission on a new AI agent, globe, alert system or unvalidated drift model.
Preserve all nine regions, with status per region. Fewer completed scientific cases are
preferable to unsupported adjusted histories. This document adds no new empirical result.
