# Isolated backfill research

Reviewed source: `sync/local-backfill` commit `6a4e45c42102be1ace17d423f4751b25e8c6b0b0`. The original inputs under `data/monthly/*.parquet` and retrieval manifests are not included. No results were reproduced in this release. See [acceptance gates](../specs/007-calendar-backfill.md).

The retained scripts describe a separate Poisson detection-count model, not the published occupied-cell-day method. Both entry points exit before reading inputs or generating a site. Unsupported generated HTML/JSON is deliberately excluded from this release.

Reviewed corrections in the retained model: missing panel counts are NaN rather than zero; the denial-test solar-time baseline respects the training cutoff; absent estimates remain NaN; arbitrary extrapolation intervals are removed; combined day/night intervals are withheld. These static corrections do not validate the model. Source completeness, exposure, SP/NRT separation, identifiability, strict serialization and independent monthly/peak evaluation remain pending. Existing published results are unchanged.

Next action: provide immutable Parquets plus source manifests, then implement a tested input adapter and independent protocol before removing the generation block. No claimed 95% intervals or purely orbital detection losses may be published from this experiment.
