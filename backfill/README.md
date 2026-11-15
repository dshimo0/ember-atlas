# Local backfill prototype

This snapshot preserves the local experimental calendar and solar-time analysis for review. Open `docs/index.html` to inspect it. The experiment uses aggregated detection counts and a separate method from the published occupied-cell-day analysis. See [spec 005](../specs/005-history-continuity-and-product.md) for validation requirements before integration.

The scripts expect local `data/monthly` Parquet inputs and use Python with NumPy, pandas and DuckDB. Run from this directory. The input files and intermediate outputs stay local.
