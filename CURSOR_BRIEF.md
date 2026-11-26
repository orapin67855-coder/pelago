# pelago ASIA - handoff (read first)

Files: index.html, css/app.css, js/app.js (one classic script, ~58 KB), vercel.json, package.json.
Run locally: `npx serve .` then open the printed URL. Deploy: see README.md.

## Verified in a real browser (headless Chromium 157, desktop 1280x800 + phone 390x780, mocked NOAA/Open-Meteo)
No page errors; all 11 workspace screens render; live-data path (SST/chl/depth/moon -> FSI) works against mocked servers.
## NOT verified
iOS Safari/WebKit (not installed here), real NOAA/Open-Meteo/NASA/Esri responses and CORS, real devices, tile layer ids/levels for overlays, Thai TTS voice, GPS inside the LINE browser.

## Bugs fixed this round (root causes of the "globe breaks" reports)
1. Canvas stretched when its container resized (pixel size fixed at load) -> now ResizeObserver.
2. Land polygons smeared onto the globe rim -> exact horizon clipping + rim arcs + densified edges.
3. Satellite tiles warped at low zoom -> finer cell subdivision by zoom level.
4. Globe far larger than the viewport -> radius 0.46*min(W,H), Asia-centred (100E, 22N).
5. Phone: workspace strip jumped to the bottom, signal card covered the map, floating card hid the globe.

## Backend: NONE yet
All data is fetched by the browser. Needed: cron + FastAPI + PostGIS + Zarr/COG cache (daily SST/chl/waves per area), user/catch-log store, LINE webhook, admin dashboard.

## Not imported / not built
- Real coastlines/borders (Natural Earth GeoJSON). Fallback shapes are hand-simplified.
- Legal layers: EEZ, protected areas, closed seasons, disputed areas ("unknown = don't recommend").
- Ocean fronts (SST gradient grid), salinity, tide currents, pressure trend, wind direction, reefs/drop-offs, solunar windows.
- Tide tables (licensed source), 8-day chlorophyll averages, cloud-cover handling beyond freshness decay.
- Catch-log storage + FSI v2 training + hit-rate measurement (needs >=300 verified trips over 2 seasons before any accuracy claim).
- LINE login (LIFF), morning push, SOS sending, price aggregation, i18n, recorded voice.

## Accuracy statements that are allowed
- Moon phase: mean-synodic formula, error up to about half a day; replace with an ephemeris (SunCalc / astronomy-engine) for better. Not "100%".
- Chlorophyll/SST: satellite estimates with latency, cloud gaps, coastal turbidity bias. Not "100%".
- Fish-finding: unmeasured. No percentage may be displayed.

## Imagery
Use NASA GIBS (public) + Esri World Imagery (check terms/attribution). Google Earth/Maps imagery is not a free tile source: it needs Google's own APIs, keys, billing and display rules; do not scrape tiles.
