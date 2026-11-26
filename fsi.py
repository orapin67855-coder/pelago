"""Moon phase and FSI v1. Same formulas as js/app.js moon() and fsiOf()."""

import math
from datetime import datetime, timezone

from app.config import FT, FW

SYNODIC = 29.530588853


def _aware(now):
    if now is None:
        return datetime.now(timezone.utc)
    if now.tzinfo is None:
        return now.replace(tzinfo=timezone.utc)
    return now.astimezone(timezone.utc)


def js_round(value):
    if value >= 0:
        return math.floor(value + 0.5)
    return math.ceil(value - 0.5)


def moon_phase(now=None):
    ms = _aware(now).timestamp() * 1000.0
    phase = ((ms / 864e5 - 10962.76) / SYNODIC) % 1.0
    phase = (phase + 1.0) % 1.0
    return {
        "ph": phase,
        "age": phase * SYNODIC,
        "ill": (1.0 - math.cos(2.0 * math.pi * phase)) / 2.0,
    }


def moon_label(phase):
    ph, age, ill = phase["ph"], phase["age"], phase["ill"]
    if ph < 0.0625 or ph > 0.9375:
        name = "จันทร์ดับ"
    elif ph < 0.4375:
        name = "ข้างขึ้น " + str(max(1, js_round(age))) + " ค่ำ"
    elif ph < 0.5625:
        name = "เต็มดวง"
    else:
        name = "ข้างแรม " + str(max(1, js_round(age - 14.77))) + " ค่ำ"
    return name + " · สว่าง " + str(js_round(ill * 100)) + "% (โดยประมาณ)"


def _parse_time(value):
    if not value:
        return None
    text = str(value).replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def fsi_of(obs, now=None):
    """Return the raw 0-100 score, or None when sst, chlorophyll and depth are all missing."""
    if obs.get("sst") is None and obs.get("chl") is None and obs.get("depth") is None:
        return None
    moment = _aware(now)

    def age_days(stamp):
        parsed = _parse_time(stamp)
        if parsed is None:
            return 9.0
        return max(0.0, (moment - parsed).total_seconds() / 86400.0)

    def fresh(stamp):
        return math.exp(-max(0.0, age_days(stamp) - 1.0) / 3.0)

    sst, chl, depth = obs.get("sst"), obs.get("chl"), obs.get("depth")
    if sst is None:
        s_sst, a_sst = 0.0, 0.0
    else:
        s_sst = math.exp(-(((sst - FT["sst"]) / FT["sw"]) ** 2) / 2.0)
        a_sst = fresh(obs.get("sstT"))
    if chl is None:
        s_chl, a_chl = 0.0, 0.0
    elif chl > FT["bloom"] or chl <= 0:
        s_chl, a_chl = 0.0, fresh(obs.get("chlT"))
    else:
        s_chl = math.exp(-((math.log10(chl) - FT["lc"]) ** 2) / (2.0 * FT["lw"] ** 2))
        a_chl = fresh(obs.get("chlT"))
    if depth is None:
        s_depth, a_depth = 0.0, 0.0
    else:
        s_depth = max(0.0, min(1.0, min(depth / 10.0, (200.0 - depth) / 120.0)))
        a_depth = 1.0
    ill = obs["moon"]["ill"]
    scores = {"sst": s_sst, "chl": s_chl, "depth": s_depth, "moon": 1.0 - ill * 0.6, "season": 0.5}
    avail = {"sst": a_sst, "chl": a_chl, "depth": a_depth, "moon": 1.0, "season": 1.0}
    numer = 0.0
    denom = 0.0
    for key, weight in FW.items():
        numer += weight * avail[key] * scores[key]
        denom += weight * avail[key]
    if denom == 0:
        return None
    return 100.0 * numer / denom
