# Measured transition evidence

The versioned replay evaluation and regional registry are addressed by `web/data/replay-evaluation.json` and `web/data/regions.json`. Original Pantanal input snapshot, daily fit CSV, frozen factors and validation remain unchanged.

Training: 36 complete paired months in 2020–2022. Evaluation: 24 complete paired months in 2023–2024, full Pantanal study area. All methods use the same globally anchored 0.05° WGS84 / UTC-day occupied-cell metric.

| Method | Monthly MAE | Signed bias | Peak-six MAE | Peak-six bias |
| --- | ---: | ---: | ---: | ---: |
| Unadjusted common-grid VIIRS | 1021.708333 | +1021.708333 | 2225.166667 | +2225.166667 |
| Training-only least-squares scalar | 175.329287 | −54.344752 | 404.601727 | −404.601727 |
| Frozen quarterly factors | 199.699731 | −123.968300 | 534.637305 | −534.637305 |

Units: occupied cell-days/month. Scalar factor 0.5497999781946175 minimizes training-only through-origin squared residuals. Peak six are ranked by observed MODIS activity, not candidate residual: 2024-08, 2024-09, 2023-11, 2024-10, 2024-06, 2024-07. Every monthly residual is in the immutable artifact and public CSV. The scalar is stronger on this existing holdout; later method selection requires separate evaluation.

January 2023 is a source-change replay scenario. MODIS remains observed after the cutoff. September 2024 MODIS is 5,819 cell-days, VIIRS common grid 8,809, seasonal replay 4,879.052992: residual −939.947008, −16.1531%. This measures reference agreement, not ground-truth or detection accuracy.

Pantanal MODIS now spans November 2000–July 2026, with 9,404 retrieved UTC days. All eight areas have 2,404 retrieved days per sensor in January 2020–July 2026. The seven new regions passed locally registered inner selection and all independent publication gates; the [regional table](regional-evaluation.md) and [coverage inventory](eight-region-coverage.md) show actual support and domains.

The 19 fresh Pantanal months have raw/scalar/quarterly MAE 399.4/89.7/70.8 and quarterly bias +67.4. Its original 2020–2024 adjustment stays frozen. NRT remains separate; source availability has zero same-sensor SP/NRT overlap.

Training MODIS records report version 6.03; outer/fresh records report 61.03. Literal labels and thermal types are preserved in current exports. This is agreement with as-delivered MODIS_SP, not proof of processing-vintage homogeneity, isolated sensor effects, wildfire classification or ground-truth accuracy. Original byte-exact inputs and derived masks are preserved in 161 source archives with 19,308 CSV/manifest members. Counts across overlapping regions are not globally unique fires.

[Executed release evidence](transition-release.json), [full artifact reconciliation](regional-artifact-check.json) and [public workflow checks](eight-region-check-public.json) identify the tested release. Physical-device testing, usable observation masks, homogeneous-reference validation, wider pre-2020 archives and official owner submission actions remain open.
