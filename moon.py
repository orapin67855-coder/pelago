from api._json import Quiet, send_json
from app.fsi import moon_label, moon_phase


class handler(Quiet):
    def do_GET(self):
        phase = moon_phase()
        send_json(self, 200, {
            "ph": phase["ph"],
            "age": phase["age"],
            "ill": phase["ill"],
            "label_th": moon_label(phase),
        })
