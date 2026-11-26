import unittest
from datetime import datetime, timezone

from app.fsi import fsi_of, moon_label, moon_phase

NOW = datetime(2026, 11, 26, 12, 0, tzinfo=timezone.utc)
# Values produced by the same formulas in js/app.js at NOW.
JS = {
    "moon_ph": 0.5616041348364433,
    "full": 88.20624100809731,
    "bloom": 62.08111899140841,
    "sst_only": 51.23664206493593,
    "deep": 23.05485775020485,
}


def _obs(**extra):
    phase = moon_phase(NOW)
    base = {"moon": phase}
    base.update(extra)
    return base


class FsiParityTest(unittest.TestCase):
    def test_js_parity_vector(self):
        phase = moon_phase(NOW)
        self.assertAlmostEqual(phase["ph"], JS["moon_ph"], places=9)
        full = _obs(sst=29, sstT="2026-11-26T00:00:00Z", chl=0.8, chlT="2026-11-25T00:00:00Z", depth=40)
        bloom = _obs(sst=29, sstT="2026-11-26T00:00:00Z", chl=12, chlT="2026-11-25T00:00:00Z", depth=40)
        sst_only = _obs(sst=31, sstT="2026-11-20T00:00:00Z")
        deep = _obs(depth=250)
        self.assertAlmostEqual(fsi_of(full, NOW), JS["full"], places=6)
        self.assertAlmostEqual(fsi_of(bloom, NOW), JS["bloom"], places=6)
        self.assertAlmostEqual(fsi_of(sst_only, NOW), JS["sst_only"], places=6)
        self.assertAlmostEqual(fsi_of(deep, NOW), JS["deep"], places=6)
        self.assertIsNone(fsi_of(_obs(), NOW))

    def test_moon_label_is_not_an_accuracy_claim(self):
        label = moon_label(moon_phase(NOW))
        self.assertIn("โดยประมาณ", label)
        self.assertNotIn("แม่น", label)

    def test_trial_confidence_never_exceeds_mid(self):
        from app.service import build_spot

        def fetch(_url):
            if "analysed_sst" in _url:
                return {"table": {"rows": [["2026-11-26T00:00:00Z", 12.3, 100.9, 29.0]]}}
            if "chlor_a" in _url:
                return {"table": {"rows": [["2026-11-25T00:00:00Z", 0.0, 12.3, 100.9, 0.8]]}}
            return {"table": {"rows": [[12.3, 100.9, -40.0]]}}

        body = build_spot(12.306, 100.924, now=NOW, fetch=fetch)
        self.assertEqual(body["stage"], "trial")
        self.assertIn(body["confidence"], ("ต่ำ", "กลาง"))
        self.assertNotIn("accuracy", body)
        self.assertNotIn("%", body["notice"])
        self.assertEqual(body["fsi"], 88)
