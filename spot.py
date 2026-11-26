from urllib.parse import parse_qs, urlparse

from api._json import Quiet, send_json
from app.service import build_spot


class handler(Quiet):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        try:
            lat = float(qs.get("lat", [""])[0])
            lon = float(qs.get("lon", [""])[0])
        except ValueError:
            send_json(self, 400, {"detail": "lat and lon are required"})
            return
        if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
            send_json(self, 400, {"detail": "lat/lon out of range"})
            return
        send_json(self, 200, build_spot(lat, lon))
