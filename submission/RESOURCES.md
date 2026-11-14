# Resource and attribution inventory

| Category | Link text and full URL | Product/version and use | Rights / verification |
| --- | --- | --- | --- |
| NASA | NASA FIRMS — https://www.earthdata.nasa.gov/data/tools/firms | Raw thermal anomaly observations, calendar, comparisons, CSV | NASA FIRMS credited in UI; landing page verification pending |
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

Map credits remain visible in the map control and Methods & data. The study rectangle is an analysis extent; no Pantanal biome geometry is included. No external imagery, music, font service or NASA insignia is used.
