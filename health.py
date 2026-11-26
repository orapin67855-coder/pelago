from api._json import Quiet, send_json


class handler(Quiet):
    def do_GET(self):
        send_json(self, 200, {"ok": True, "stage": "trial"})
