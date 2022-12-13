from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from . import ParsePayload, GameState

class RequestHandler(BaseHTTPRequestHandler):
	on_payload_callback = None
	token = None
	gamestate = GameState.GameState()

	def do_POST(self):
		body_length = int(self.headers["Content-Length"])
		body = self.rfile.read(body_length).decode("utf-8")

		payload = json.loads(body)

		if not self._check_token(payload):
			return

		ParsePayload.parse_payload(self.gamestate, payload)

		if self.on_payload_callback is not None:
			self.on_payload_callback(self.gamestate)

		self.send_response(204)
		self.end_headers()

	def _check_token(self, payload):
		if "auth" not in payload or "token" not in payload["auth"]:
			return False

		return payload["auth"]["token"] == self.token

class GSIServer:
	def __init__(self, address, token):
		RequestHandler.token = token

		self.server = HTTPServer(address, RequestHandler)

	def set_payload_callback(self, payload_callback):
		RequestHandler.on_payload_callback = payload_callback

	def run(self):
		try:
			self.server.serve_forever()
		except KeyboardInterrupt:
			pass

		self.server.server_close()