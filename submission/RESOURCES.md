# Resource and attribution inventory

| Category | Link text and full URL | Product/version and use | Rights / verification |
| --- | --- | --- | --- |
| NASA | NASA FIRMS — https://www.earthdata.nasa.gov/data/tools/firms | Raw thermal anomaly observations, calendar, comparisons, CSV | NASA FIRMS credited in UI; landing page HTTP 200 verified 2026-11-15 |
| NASA | MODIS C6.1 fire archive — https://firms.modaps.eosdis.nasa.gov/download/ | MODIS_SP, Terra/Aqua pooled reference | Actual Area API extracts and checksums verified; product-page license text pending owner review |
| NASA | NOAA-20 VIIRS 375 m fire archive — https://firms.modaps.eosdis.nasa.gov/download/ | VIIRS_NOAA20_SP comparison | Actual observations verified; exact product documentation/attribution wording pending |
| NASA | FIRMS Area API — https://firms.modaps.eosdis.nasa.gov/api/area/ | Bounded authenticated CSV ingestion | Key restricted to ingestion; never cite keyed URLs |
| Other | Ember Atlas — https://github.com/dshimo0/ember-atlas | Existing project scripts and specs, retained history | No repository license grant asserted; owner should select license before downstream reuse |
| Other | Python — https://www.python.org/ | Standard-library pipeline and local server | Python Software Foundation license; runtime not bundled |
| Other | Playwright — https://playwright.dev/python/ | Verification and screen capture only | Apache-2.0; not shipped in browser |
| Other | Chromium — https://www.chromium.org/ | Automated screen capture | Tool only; screenshots contain project UI, no people/audio |
| Other | Vercel — https://vercel.com/ | Static app and media hosting on the existing Hobby team | Actual provider; no Vercel client library or imagery bundled |
| Other | OpenAI Codex — https://openai.com/codex/ | Coding, tests, documentation assistance | AI disclosure belongs in portal materials |

## Map resources

| Resource | Version/use | Attribution and source |
| --- | --- | --- |
| OpenStreetMap | Standard raster basemap with rivers, settlements and boundaries | © OpenStreetMap contributors. https://www.openstreetmap.org/copyright . Tile usage policy: https://operations.osmfoundation.org/policies/tiles/ . Normal interactive requests only; no bulk tile download or offline tile cache. |
| Leaflet | 1.9.4, locally vendored JavaScript/CSS and navigation controls | BSD-2-Clause license preserved at web/vendor/leaflet/LICENSE; source checksums in web/vendor/leaflet/SOURCE.json. https://leafletjs.com/ |
| Natural Earth | Admin 0 countries 1:110m; rivers and populated places 1:50m; local geographic fallback | Public domain: https://www.naturalearthdata.com/about/terms-of-use/ . Raw inputs under data/reference; URLs and SHA-256 values in web/assets/local-geography.json. |

Map credits remain visible in the map control and Methods & data. The study rectangle is an analysis extent; no Pantanal biome geometry is included. Local copies of attributed NASA imagery are used as editorial context; no music, font service or NASA insignia is used.

## Current link verification

Checked 2026-11-15 UTC; exact results and resolved URLs are in [resource-check.json](resource-check.json). NASA FIRMS landing, archive and Area API pages returned 200, as did OpenStreetMap copyright/tile policy and Leaflet. The archive page identifies the NOAA-20 375 m record starting 2018-04-01. The paired release uses January 2020–July 2026 SP observations with MODIS_SP, whose literal source-version strings are now preserved per record. Natural Earth's terms endpoint returned 406 on this check; committed source/checksum metadata and existing public-domain attribution remain preserved, and owner verification is still required for final portal wording. Official challenge/resources/event/legal pages returned 503. Link HTTP availability alone does not certify event eligibility or permission wording.

The pitch includes actual product captures and credited NASA editorial composites, labeled separately from quantitative evidence. The nine-slide PDF is a print export of the product presentation. A temporary eSpeak NG synthesized read measured script duration; no generated audio is published or submitted. The public screen recording is silent and contains no people. Codex implementation/documentation assistance is disclosed in PROJECT-PAGE.md.

## Eight-region and replay release

Actual additional products: MODIS_NRT and VIIRS_NOAA20_NRT in a separate November 8–14, 2026 UTC snapshot for all eight areas. MODIS_SP backfill starts November 1, 2000 in the Pantanal study area. Exact source availability, date windows, byte hashes and acquisition fields are retained; no S-NPP or NOAA-21 observations are added to the product.

The study-area geometries are project-defined rectangles from data/region-definitions-v1.json, not licensed official biome/state boundaries. Natural Earth supplies all 177 country geometries and the locally selected rivers/settlements needed across eight extents. The pitch world map is generated from those same attributed source geometries, with direct links to the registry's actual datasets.

New original CSVs/manifests are packaged under data/source-archives with archive/member SHA-256 values; their recorded data/history and data/regions paths are restored byte-for-byte by scripts/source_archives.py. Dataset evidence inventories link the archive index. Source and deployment checks are recorded in transition-release.json. The current pitch uses actual product screenshots and source-derived figures. Temporary timing speech is not a published asset.

Source-field definitions: https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs (HTTP 200, 2026-11-15 UTC). The NASA download page advertises Collection 6.1; observed version strings include 6.03/61.03 and are retained literally without claiming uniformity. All reported thermal types are included, not independently classified wildfire events. See methodology and the current coverage inventory for actual release periods.

## Editorial NASA imagery

- **Blue Marble 2007 West**, NASA/Goddard Space Flight Center/Reto Stöckli. NASA image identifier `GSFC_20171208_Archive_e002131`; released October 9, 2007. Source: https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e002131/GSFC_20171208_Archive_e002131~medium.jpg . Local file `web/assets/earth-nasa.jpg`. Used in About, Pitch and general editorial Earth context. It is a composite, not current imagery or the selected period's analytical layer.
- **MODIS Terra corrected reflectance, true color**, NASA GIBS, September 1, 2024, study bounds W/S/E/N -59/-23/-54/-15. WMS source and exact request parameters are retained in `web/assets/editorial-imagery.json`. Local file `pantanal-modis-2024-09-01.jpg`; used only as dated Pantanal editorial context in scene 1. No detections are overlaid on that photograph.
- NASA media guidance: https://www.nasa.gov/nasa-brand-center/images-and-media/ (HTTP 200 when acquired). Credits remain adjacent to imagery. No NASA endorsement is implied. Original source metadata, byte hashes and declared use are in [editorial-imagery.json](../web/assets/editorial-imagery.json). No generated scientific image or portrait is used.

## P2/P3 visual assets

Eight local study-area context images use NASA GIBS `MODIS_Terra_CorrectedReflectance_TrueColor`, dated 2024-09-01. [regional-imagery.json](../web/assets/regional-imagery.json) records exact WMS queries, WGS84 study bounds, dimensions and SHA-256. These are editorial reflectance images, separate from FIRMS monthly activity; clouds and swath gaps remain visible. No new thermal observations, fire perimeters or burned-area estimates are inferred.

Manrope: [Google Fonts source](https://github.com/google/fonts/tree/main/ofl/manrope), SIL Open Font License 1.1. [Local license](../web/assets/fonts/OFL.txt), [subset provenance](../web/assets/fonts/provenance.json). The font is self-hosted; normal application use makes no request to a font service.
