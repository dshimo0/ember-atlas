# Eight-region transition release checklist

Authoritative identity and executed evidence: [transition-release.json](../submission/transition-release.json). Inspect [eight-region-check-public.json](../submission/eight-region-check-public.json) for per-region/window counts and actual deployed execution. The prior one-area release evidence remains historical. The deployed source `ca8c7e9` passed all 34 main browser groups, 18 additional /demo/root checks, 39 exact-byte public checks and anonymous video playback. GitHub CI passed.

| Gate | Evidence / scope |
| --- | --- |
| Frozen science preserved | Original snapshot, validation, daily fit input and factors retain their hashes. No fitting on holdout. |
| Three methods | Training-only scalar, frozen seasonal and unadjusted evaluated on identical 24 paired months; all residuals and reference-selected peak-six metrics published. |
| Replay | Derived January 2023 scenario cutoff; month source and adjustment; separate observed holdout MODIS; source-tagged monthly CSV. |
| Eight snapshots | All eight ordered rectangles have real SP and separate NRT observations, provenance, maps and exports without a visitor key. |
| Earlier archive | All 1,400 older MODIS windows retrieved; full MODIS coverage 2000-11-01–2024-12-31, paired calibration 2020–2024 only. |
| Map | Full-data cell occupancy matches common-grid totals and cell CSV; sampled points separate; OSM and local fallback cover every extent. |
| State and exports | Desktop/mobile direct loads/refresh, region/mode/month/sensor/area changes, URL restoration and stale-response guards. CSV exact-record and cell-count reconciliation. |
| Missingness | Pre-archive missing periods blank; actual retrieved zero day numeric/exportable zero; NRT partial-month status explicit. |
| Reproducibility | Deterministic source packages, all member hashes verified, reconstruction refuses to overwrite changed files; versioned inventories and checksum-verified shards. |
| Tests | Fifteen Python tests and nineteen Node cases, plus the signed-out eight-region browser suite and print-page check. |
| Secrets | Actual ingestion key and keyed-URL patterns scanned without printing; compressed public data and source archives included. No key required by frontend. |
| Presentation | Nine interactive sections and eight world-map links; source-derived figures; actual product screenshot; current script/timing record. |
| Owner pending | Current official demonstration format/event eligibility, human roster, physical/human delivery rehearsal, rights wording, terms and final Submit for Judging action. |

The scalar outperforms seasonal on this existing evaluation; a replacement cannot be selected using the same holdout. Regional adjustment is unavailable wherever multi-year local evaluation is missing. NRT is not joined to SP. Source rectangles are not biome masks. Broader challenge ambitions remain explicit in [traceability](challenge-traceability.md).

Run `python -m unittest discover -s tests`, `node --test tests/test_*.mjs`, and `BASE_URL=… python scripts/check_eight_regions.py`. Use `python scripts/serve.py` locally. Browser checks require Playwright, Chromium and pdfinfo. Official terms and final portal submission are deliberately not automated.
