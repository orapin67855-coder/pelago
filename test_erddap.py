import unittest
from urllib.error import URLError

from app.erddap import read_spot


class ErddapParseTest(unittest.TestCase):
    def test_uses_latest_chlorophyll_and_depth_below_sea_level(self):
        seen = []

        def fetch(url):
            seen.append(url)
            if "analysed_sst" in url:
                return {"table": {"rows": [["2026-11-26T00:00:00Z", 12.3, 100.9, 28.4]]}}
            if "[0:1:0]" in url:
                raise URLError("dimension mismatch")
            if "chlor_a" in url:
                return {"table": {"rows": [
                    ["2026-11-23T00:00:00Z", None],
                    ["2026-11-25T00:00:00Z", 0.4],
                ]}}
            return {"table": {"rows": [[12.3, 100.9, -32.0]]}}

        obs, sources = read_spot(12.306, 100.924, fetch=fetch)
        self.assertEqual(obs["sst"], 28.4)
        self.assertEqual(obs["chl"], 0.4)
        self.assertEqual(obs["chlT"], "2026-11-25T00:00:00Z")
        self.assertEqual(obs["depth"], 32.0)
        self.assertEqual(sources, {"sst": "ok", "chl": "ok", "depth": "ok"})
        self.assertTrue(any("[0:1:0]" in url for url in seen))
        self.assertTrue(any("chlor_a" in url and "[0:1:0]" not in url for url in seen))

    def test_failed_source_stays_missing(self):
        def fetch(url):
            raise URLError("offline")

        obs, sources = read_spot(1, 2, fetch=fetch)
        self.assertIsNone(obs["sst"])
        self.assertIsNone(obs["chl"])
        self.assertIsNone(obs["depth"])
        self.assertEqual(set(sources.values()), {"error"})
