# pelago-asia backend (skeleton)
Run (from this folder): `pip install -r requirements.txt && uvicorn app.main:app --reload`
Tests (stdlib only): `python -m unittest discover -s tests -t .`
Endpoints: `GET /api/health`, `GET /api/moon`, `GET /api/spot?lat=&lon=`  (contract + roadmap: ../docs/BACKEND_HANDOFF.md)
Status: `python -m unittest discover -s tests -t .` passes, including JS parity for `fsiOf`. Live NOAA responses are not assumed; a failed source stays null and confidence stays "ต่ำ" or "กลาง". No database, auth, LINE or queue yet.
