# Ember Atlas | Release verification

Application: https://ember-atlas-opal.vercel.app/

Input release: `35fd9186738772a7076225b3d640343680efa8a6`, branch `work`. Scientific snapshot: `snapshot-19621fa88d40.json.gz`, uncompressed SHA-256 `19621fa88d408fb5d9aa87482de1bb219e8dd7ed67128c1147d1a63fb087e677`. Validation: `validation-ba55acfc7909.json`. The FIRMS snapshot, validation, frozen fitting rules and export model are unchanged.

## Screen and workflow

The screen starts with “Pantanal fire activity, 2020–2024,” a compact validation summary and area/sensor/date controls. September 2024 remains selected. Desktop places the interactive map beside the comparison; mobile places the map directly after the selected month and finding. The full calendar follows both panels. The observation export is beside the map; aggregate export is beside the calendar.

The default basemap uses OpenStreetMap tiles with attribution. Leaflet 1.9.4 provides zoom, pan, scale and fit-to-study-area. Failed tile requests activate local Natural Earth country boundaries, rivers and settlements. The study rectangle is distinct from these boundaries; no biome geometry is included.

## Checks

| Requirement | Evidence | Status |
| --- | --- | --- |
| Initial state and copy | Compact title, September 2024, calculated 80.5% result, 24 holdout months and full-area scope; no promotional hero or rhetorical opening. | Local verified; public retest pending |
| Desktop/mobile layout | Map beside comparison on desktop and before it on mobile; calendar follows both. | Local verified; public retest pending |
| Basemap and navigation | Real OpenStreetMap tiles, visible attribution, zoom, keyboard pan, metric scale and fit. | Local verified; public retest pending |
| Tile failure | External tile requests are aborted in a separate browser context. Local geography includes 23 river features and 27 settlements; observations and CSV remain available. | Local verified; public retest pending |
| Filter synchronization | Month, area and sensor changes update actual rendered observation layers and matching CSV records. | Local verified; public retest pending |
| Calibration scope | Both subregions have no adjusted series, factor or adjusted CSV value. | Local verified; public retest pending |
| Export reconciliation | Default September: 125,055 observation rows and 120 full-period aggregate rows. Northern MODIS September: 18,038 rows. Export rows, source references and common-grid totals reconcile with the original snapshot. | Local verified; public retest pending |
| Missing and partial data | A real zero day, a partial date interval and missing December 2019 are distinct. Unavailable counts stay blank. | Local verified; public retest pending |

## Scientific figures

- Training: 36 paired months in 2020–2022. Holdout: 24 paired months in 2023–2024.
- MAE against MODIS: 1,021.7083333333334 → 199.6997313847094 cell-days/month, an 80.45433076451603% reduction. Adjusted signed bias is -123.96830007041311 cell-days/month.
- September 2024: MODIS 5,819; VIIRS common grid 8,809; adjusted VIIRS 4,879.0529915213565. The adjusted value is 16.1531% below MODIS.
- Prior September medians, 2020–2023, n=4: MODIS 2,532; VIIRS 4,782. Native counts are 23,396 and 101,659.

These figures measure agreement with MODIS. Retrieval completeness does not establish observation coverage; swath/cloud quality masks remain unavailable.

## Verification artifacts

`python -m unittest discover -s tests` covers nine pipeline/scientific tests. `node tests/test_model.mjs` covers eight model/export cases. `scripts/check_judging_flow.py` tests fresh desktop and mobile browser contexts against the original pinned observations, including forced basemap failure. Mobile verification uses viewport/touch emulation rather than a physical device.

- `submission/judging-check-local.json` and `submission/judging-check-public.json`
- `submission/judging-desktop.png`, `submission/judging-mobile.png`, `submission/judging-first-viewport.png`
- `submission/map-fallback-desktop.png`, `submission/map-fallback-mobile.png`
- `submission/map-before-desktop.png`, `submission/map-before-mobile.png`

The final source commit, deployment and HTTP checks are recorded in `submission/judging-release.json`. Official demonstration format, event eligibility and final submission remain Team Owner checks.
