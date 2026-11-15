# Release verification checklist

Authoritative executed identity: [transition-release.json](../submission/transition-release.json). Distinguish source commit from immutable data commit. The prior public Pantanal expansion at `a792e07` remains in history; current public execution is recorded after deployment.

- [x] Eight fixed study geometries and real precomputed SP/NRT observations.
- [x] 79 complete paired SP months per region; full snapshot/native/grid/flag reconciliation for 16 datasets.
- [x] All eight regional evaluation artifacts reproduced; seven local inner choices passed each registered independent gate.
- [x] Original Pantanal files/factors unchanged; extra 19 months remain an audit outside its published adjustment domain.
- [x] All candidate metrics, residuals and reference-selected peaks retained; no outcome-based method switch.
- [x] Literal versions/types retained, including verified joins to frozen source records; reference label change visibly qualified.
- [x] Local desktop/mobile workflow, exports, source fields, SVG keyboard links, missing/zero/partial states and tile/shard-failure recovery exercised.
- [x] Original local data URLs protected; initial SP/NRT views local; other observations pinned to immutable public Git bytes with SHA verification.
- [x] Unit tests, frozen-file/credential checks, real recording and nine-page print executed locally.
- [ ] Current pinned production source deployed and signed-out public workflow retested; see executed identity report.
- [ ] Official Project Demonstration format, eligibility/deadline and media restrictions confirmed by Team Owner (official pages returned 503).
- [ ] Human roster/contributions, physical-device check and human pitch rehearsal completed by Team Owner.
- [ ] Terms accepted and final Submit for Judging performed by Team Owner.

Scientific limits remain explicit: all reported thermal types, unverified reference-vintage homogeneity/VIIRS code interpretation, unknown usable observation opportunity, no ground-truth accuracy, no SP/NRT join, no factor transfer to smaller masks, and no pre-2020 archive outside Pantanal. These limits are not replaced by a generic banner.

Commands: `python -m unittest discover -s tests`; `node --test tests/*.mjs`; `python scripts/verify_regional_artifacts.py`; `python scripts/check_release_integrity.py`; `BASE_URL=… python scripts/check_eight_regions.py`. Use `python scripts/serve.py --port 8930` for local route parity. Deployment procedure is in DEPLOYMENT.md. Owner portal actions are deliberately not automated.
