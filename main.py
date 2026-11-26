from fastapi import FastAPI, HTTPException, Query

from app.fsi import moon_label, moon_phase
from app.service import build_spot

app = FastAPI(title="pelago Asia", docs_url=None, redoc_url=None)


@app.get("/api/health")
def health():
    return {"ok": True, "stage": "trial"}


@app.get("/api/moon")
def moon():
    phase = moon_phase()
    return {"ph": phase["ph"], "age": phase["age"], "ill": phase["ill"], "label_th": moon_label(phase)}


@app.get("/api/spot")
def spot(lat: float = Query(...), lon: float = Query(...)):
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        raise HTTPException(status_code=400, detail="lat/lon out of range")
    return build_spot(lat, lon)
