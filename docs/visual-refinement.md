# P2/P3 visual refinement

P2 follows the UX audit: typography, restrained transitions and additional real imagery. The owner selected deeper visual presentation for P3; broader data acquisition is outside this visual release.

## Implemented scope

- Self-hosted Manrope with SIL OFL license, Latin/interface subset and system fallback; tabular scientific values retain export precision.
- Brief feedback on controls and scene entry, with no autoplay or looping effects. Reduced-motion preferences and static print take precedence.
- About study-area atlas: eight NASA GIBS true-color images dated September 1, 2024, registry order, actual bounds, source queries and direct Explore links generated with the existing URL-state helper. Cloud/swath gaps are retained. The dated images are editorial context, separate from the selected-month FIRMS metric.
- Nine-section pitch navigation uses the existing presentation state. Previous/Next, keyboard, mobile scroll, source links and nine-page print remain supported.

## Scientific invariants

No FIRMS ingestion, fitting, data shards, aggregation, baseline, source transition or export calculation is changed. The frozen Pantanal factors, stronger scalar baseline, geographic limits, processing-version caveat and unknown usable observation coverage remain visible. No image is used as physical validation of the calibration.

## Backfill review boundary

The owner requested review of a local Windows `backfill` directory. That directory is not mounted in this Linux execution workspace and is not present in the current Git tree. Review requires an uploaded archive or accessible repository branch. Existing `/tmp` scripts with “backfill” in their names are not evidence of that directory's contents. No claim of evaluating or integrating those unavailable files is made.

Once accessible, inspect the inventory and source manifests, acquisition dates/products/geometry, credential handling, checksums, completeness, duplicate/overlap rules and consistency with frozen artifacts before considering any integration. New training or method selection requires its own evaluation protocol.

## Verification

Source `b58b7d16579de4579dcdd35be4ce620d00d6e7f2` is publicly deployed. [Executed evidence](../submission/visual-release.json) records three responsive experience checks, five routes per size, eight atlas links at two sizes, the selected Pantanal CSV, font failure, reduced motion, targeted accessibility rules, nine-page print, anonymous asset checks and CI. The prior 50-group scientific/export suite remains documented against its tested source; it was not rerun for this presentation-only change. Physical-device, assistive-technology and human presentation checks remain separate owner actions.
