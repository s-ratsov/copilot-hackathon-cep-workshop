import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from game_logic import CHOICES, normalize_choice, play_round


def parse_choice_from_path(path):
    path_choice = path.lstrip("/").strip().lower()
    if path_choice in CHOICES:
        return path_choice
    raise ValueError("Path must be one of /rock, /paper, /scissors, /lizard, /spock or /play")


def parse_choice_from_body(body_bytes):
    try:
        payload = json.loads(body_bytes.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("Request body must be valid JSON.") from exc

    if not isinstance(payload, dict) or "choice" not in payload:
        raise ValueError("JSON body must contain a 'choice' field.")

    return normalize_choice(payload["choice"])


class RPSHandler(BaseHTTPRequestHandler):
    def _write_json(self, status_code, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self):
        try:
            if self.path == "/play":
                content_length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(content_length)
                user_choice = parse_choice_from_body(body)
            else:
                user_choice = parse_choice_from_path(self.path)

            self._write_json(200, play_round(user_choice))
        except ValueError as exc:
            self._write_json(400, {"error": str(exc)})

    def do_GET(self):
        self._write_json(
            200,
            {
                "message": "Use POST /play with JSON {'choice': 'rock'} or POST /rock|/paper|/scissors|/lizard|/spock",
                "choices": list(CHOICES),
            },
        )

    def log_message(self, format_, *args):
        # Keep terminal output clean for workshop usage.
        return


def run_api(host="127.0.0.1", port=8000, print_func=print):
    server = ThreadingHTTPServer((host, port), RPSHandler)
    print_func("RPSLS API Server")
    print_func(f"Listening on: http://{host}:{port}")
    print_func("Use POST /play with JSON body, or POST /rock|/paper|/scissors|/lizard|/spock")
    server.serve_forever()
