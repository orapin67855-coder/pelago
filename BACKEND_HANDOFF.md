# Backend handoff (for the friend taking the backend)

## What exists
`backend/app/fsi.py` (moon + FSI v1, pure), `erddap.py` (SST/chl/depth point queries), `cache.py` (in-memory TTL), `main.py` (FastAPI). The frontend does NOT call this API yet: it fetches NOAA/Open-Meteo directly from the browser (js/app.js `live()`, `wx`).

## API contract (v0, may change)
`GET /api/spot?lat=12.306&lon=100.924` ->
`{lat,lon,fetched_at,values:{sst_c,sst_time,chl_mg_m3,chl_time,depth_m,moon:{ph,age,ill,label_th}},fsi:int|null,confidence:"ต่ำ"|"กลาง",sources:{sst,chl,depth:"ok"|"error"},stage:"trial",notice}`
Rules: never return an accuracy percentage; confidence max "กลาง" in trial; `fsi:null` when no data.

## Priority tasks
1. Run it and VERIFY the ERDDAP queries from a server (esp. chlorophyll `nesdisVHNchlaDaily` dimensions; ETOPO var `z`). Fix `erddap.py` if needed.
2. Daily job: download SST/chl/waves grids per active area -> store Zarr/COG; serve cells instead of per-click point queries (0.05 deg grid, guide section FSI).
3. PostGIS schema: areas, ports, legal_layers(eez, protected, closed_season with start/end), spots(source), catch_logs, price_reports, alerts. Consent + "delete my data" (PDPA).
4. Legal filters before any recommendation ("unknown = don't recommend"): EEZ + 5 km buffer, disputed areas removed, protected areas, closed seasons, boat-type zones.
5. Weather: server-side Open-Meteo (free = non-commercial only; commercial needs a plan or NOAA GFS/WaveWatch III).
6. Fronts (SST gradient percentile), salinity, tide (licensed source), pressure trend, wind direction.
7. LINE: Messaging API webhook + LIFF login, morning push, SOS relay (needs verified rescue numbers per country - do not guess).
8. Catch-log ingestion + FSI v2 (logistic) + spatial CV; only then publish hit rate per area stage (trial/beta/verified).
9. Admin dashboard: data freshness per source, user counts, hit rate per area.
10. Switch frontend to this API (keep UI unchanged), keep browser fallback.

## Parity
`backend/tests/test_fsi.py::test_js_parity_vector` pins Python to js/app.js `fsiOf`. If you change weights, change `config.py` AND `FW/FT` in js/app.js (or delete the JS model once the API is the single source).
