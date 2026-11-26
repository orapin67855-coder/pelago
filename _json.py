import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))


def send_json(handler, code, body):
    raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "public, max-age=0, must-revalidate")
    handler.end_headers()
    handler.wfile.write(raw)


class Quiet(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return
