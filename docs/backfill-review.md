# Backfill review and integration decisions

Reviewed branch: `sync/local-backfill`, `6a4e45c42102be1ace17d423f4751b25e8c6b0b0`. Current release retains the occupied-cell-day analytical pipeline; the alternative Poisson model measures native detection counts.

| Material | Decision | Status / evidence |
| --- | --- | --- |
| Calm monthly calendar, separate anomaly view | Adapt within existing shared Explore/demo | Implemented; browser and export checks recorded in `submission/calendar-continuity-check.json` |
| Platform/day-night solar-time summaries | Retain as research direction | Deferred: original inputs, exposure and provenance unavailable |
| 313-month experimental harmonized outputs | Do not publish or merge as validated series | Missing reproducible source Parquets/manifests; research generators blocked |
| Claimed 95% bounds | Remove arbitrary extrapolation bounds and withhold combined intervals | Static correction only; no empirical uncertainty estimate approved |
| Missing panel entries | Preserve NaN, never infer retrieved zero | Static correction; future adapter must establish retrieval completeness |
| MODIS-denial preprocessing | Restrict solar-time baseline to training cutoff | Static correction; new independent evaluation required |
| Orbital-loss percentage / guaranteed removal of instrument jump | Exclude causal claim | Missing identification and usable-observation evidence |
| Availability attachment | Retain exact CSV with SHA-256 metadata | Implemented; upstream timestamp unknown; not a published coverage extension |
| Local regional runner and acquisition changes | Do not wholesale cherry-pick older pipeline files | Deferred to a separately tested acquisition task; current production pipeline preserved |
| Qwen recommendations | Record as secondary proposals | Stale app/coverage assessment rejected; deadlines, competitors and causal claims unverified |
| Marina video | Timestamped requirement mapping | Implemented from owner transcript; independent audiovisual verification blocked |
| Supplied emblem | Approved reference, no fabricated replacement | Deferred until original asset is accessible in workspace |

The eight-region observed release remains available. Historical MODIS extension, SP/NRT joins, additional platforms and correction of orbital schedule effects require their own acquisition and evaluation gates. A visually smoother record is insufficient acceptance evidence.
