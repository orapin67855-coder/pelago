"""Assemble the /api/spot contract. Trial stage only; no accuracy figure."""

from app.config import NOTICE
from app.erddap import read_spot
from app.fsi import fsi_of, js_round, moon_label, moon_phase


def build_spot(lat, lon, now=None, fetch=None):
    obs, sources = read_spot(lat, lon, fetch=fetch)
    phase = moon_phase(now)
    scored = dict(obs)
    scored["moon"] = phase
    raw = fsi_of(scored, now=now)
    complete = sources["sst"] == "ok" and sources["chl"] == "ok" and sources["depth"] == "ok"
    return {
        "lat": lat,
        "lon": lon,
        "fetched_at": _iso(now),
        "values": {
            "sst_c": obs["sst"],
            "sst_time": obs["sstT"],
            "chl_mg_m3": obs["chl"],
            "chl_time": obs["chlT"],
            "depth_m": obs["depth"],
            "moon": {
                "ph": phase["ph"],
                "age": phase["age"],
                "ill": phase["ill"],
                "label_th": moon_label(phase),
            },
        },
        "fsi": None if raw is None else int(js_round(raw)),
        "confidence": "กลาง" if raw is not None and complete else "ต่ำ",
        "sources": sources,
        "stage": "trial",
        "notice": NOTICE,
    }


def _iso(now):
    from app.fsi import _aware

    return _aware(now).strftime("%Y-%m-%dT%H:%M:%SZ")
