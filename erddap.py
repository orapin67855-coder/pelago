"""Point queries against NOAA ERDDAP. Same URLs as js/app.js live()."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from app.cache import TTLCache
from app.config import ERDDAP

_cache = TTLCache()


def _get_json(url, timeout=12):
    with urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _rows(url, fetch):
    payload = fetch(url)
    return payload["table"]["rows"]


def read_spot(lat, lon, fetch=None):
    """Return raw observations and a per-source ok/error flag. Missing values stay None."""
    fetch = fetch or _get_json
    key = (round(float(lat), 3), round(float(lon), 3))
    cached = _cache.get(key)
    if cached is not None and fetch is _get_json:
        return cached
    obs = {"sst": None, "sstT": None, "chl": None, "chlT": None, "depth": None}
    sources = {"sst": "error", "chl": "error", "depth": "error"}
    try:
        rows = _rows(ERDDAP + "jplMURSST41.json?analysed_sst[(last)][(" + str(lat) + ")][(" + str(lon) + ")]", fetch)
        if rows and rows[0][3] is not None:
            obs["sstT"] = rows[0][0]
            obs["sst"] = float(rows[0][3])
            sources["sst"] = "ok"
    except (HTTPError, URLError, TimeoutError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        pass
    try:
        base = ERDDAP + "nesdisVHNchlaDaily.json?chlor_a[last-3:1:last]"
        point = "[(" + str(lat) + ")][(" + str(lon) + ")]"
        try:
            rows = _rows(base + "[0:1:0]" + point, fetch)
        except (HTTPError, URLError, TimeoutError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
            rows = _rows(base + point, fetch)
        filled = [row for row in rows if row[-1] is not None]
        if filled:
            last = filled[-1]
            obs["chlT"] = last[0]
            obs["chl"] = float(last[-1])
            sources["chl"] = "ok"
    except (HTTPError, URLError, TimeoutError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        pass
    try:
        rows = _rows(ERDDAP + "ETOPO_2022_v1_15s.json?z[(" + str(lat) + ")][(" + str(lon) + ")]", fetch)
        if rows and rows[0][2] is not None:
            obs["depth"] = max(0.0, -float(rows[0][2]))
            sources["depth"] = "ok"
    except (HTTPError, URLError, TimeoutError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        pass
    if fetch is _get_json:
        _cache.set(key, (obs, sources))
    return obs, sources
