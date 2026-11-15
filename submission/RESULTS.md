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

The older Pantanal MODIS backfill comprises 1,400 verified original windows, extending MODIS to 2000-11-01–2024-12-31 with 8,827 retrieved UTC days. NOAA-20 SP paired publication remains 2020–2024. New source files/manifests are preserved in deterministic archives with member checksums. Older platform mix is not independently harmonized; replay historical baselines use earlier complete matched-domain months only.

[Eight-row coverage inventory](eight-region-coverage.md) lists all released study extents, products and dates. Seven added regions have one complete matched SP month, not independently evaluated regional adjustment. Separate NRT snapshots are partial-month windows. Usable swath/cloud observation coverage remains unknown. [Release evidence](transition-release.json) and [public browser execution](eight-region-check-public.json) record the tested source and per-region CSV counts.
