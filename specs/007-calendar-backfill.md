# Calendar-first continuity release

## Acceptance contract

| ID | Requirement | Evidence / gate |
| --- | --- | --- |
| C1 | Explore and demo place selected month/takeaway, then calendar, then map/comparison | Browser DOM order; desktop/mobile screenshots |
| C2 | Activity and prior-median difference are separate colour modes | Shareable `encoding=anomaly`; earlier complete same-month years, n >= 3; unsupported/zero-median percentages explicitly unavailable |
| C3 | Reference/replay values retain existing units and source lineage | Frozen scientific artifacts unchanged; matching exports |
| C4 | Chart/source table uses progressive disclosure | Keyboard-operated details; chart selection keeps existing state |
| C5 | Missing, partial and retrieved zero stay distinct | Existing data tests plus calendar state assertions |
| C6 | Preserve all eight presets, routes, map attribution/fallback and EN/PT themes | Existing public workflow suite |
| C7 | Backfill remains isolated until reproducible | Fail-closed generators; no experimental data in public assets |
| C8 | Inventory source availability separately | Owner-provided CSV retained verbatim; no implied retrieval or usable coverage |

Anomaly colour in a raw multi-sensor cell is the mean of supported per-sensor percentage differences, only when every displayed sensor has support. The underlying values remain cell-days, not an anomaly total. Blue is below, brown above; neutral is equal or unsupported, with distinct tooltip explanation. Same-month seasonal scaling preserves relative differences for adjusted-only values. Replay uses the existing earlier replay baseline. NRT has no historical anomaly.

## Backfill research gates

Require original Parquet inputs, exact bounds, source URLs/snapshot identity, retrieval time, checksums, quality rules and observation opportunity limitations. Zero requires positive retrieval evidence; absence remains missing. Fit all preprocessing on training only. Keep SP and NRT separate. No uncertainty band without a justified, evaluated construction. No causal orbital-loss claim from detection-time regressions alone. Compare new candidates against scalar and frozen seasonal baselines under a new preregistered temporal evaluation; the old holdout cannot select a replacement.

The current uploaded availability table lists product ranges, not region-level retrieval. Published registry coverage remains authoritative. The owner-supplied emblem is approved as a project identity reference; adding it is deferred until an original file is accessible. It is not a scientific map or an official NASA endorsement.
