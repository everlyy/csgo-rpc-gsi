from abc import ABC, abstractmethod
import json
import os
import socket
import struct
import sys
import uuid

class Op:
	HANDSHAKE = 0
	FRAME = 1
	CLOSE = 2
	PING = 3
	PONG = 4

class DiscordRPC(ABC):
	def __init__(self, client_id):
		self.client_id = client_id

		self._connect()
		self._handshake()

		print(f"Connected to Discord as {self.client_id}")

	def init_for_os(client_id):
		if sys.platform == "win32":
			return DiscordRPC_Windows(client_id)
		else:
			return DiscordRPC_Unix(client_id)

	def set_activity(self, activity):
		nonce = str(uuid.uuid4())
		data = {
			"cmd": "SET_ACTIVITY",
			"args": { 
				"pid": os.getpid(),
				"activity": activity
			},
			"nonce": nonce
		}

		print(f"Setting activity {nonce}")
		self.write(data)

	@abstractmethod
	def _connect(self):
		return

	@abstractmethod
	def _write(self, data):
		return

	@abstractmethod
	def _read(self, length):
		return

	@abstractmethod
	def _close(self):
		return

	def _handshake(self):
		data = {
			"v": 1,
			"client_id": self.client_id
		}
		opcode, data = self.write_read(data, op=Op.HANDSHAKE)

		if opcode == Op.FRAME and data["cmd"] == "DISPATCH" and data["evt"] == "READY":
			return
		else:
			if op == Op.CLOSE:
				print(f"Handshake failed")
				self.close()

	def _read_header(self):
		header = self._read_exactly(8)
		return struct.unpack("<II", header)

	def _read_exactly(self, length):
		buffer = b""
		remaining = length
		while remaining:
			chunk = self._read(remaining)
			buffer += chunk
			remaining -= len(chunk)
		return buffer

	def write_read(self, data, op):
		self.write(data, op)
		return self.read()

	def write(self, data, op=Op.FRAME):
		data_bytes = json.dumps(data).encode("utf-8")
		header = struct.pack("<II", op, len(data_bytes))
		self._write(header)
		self._write(data_bytes)

	def read(self):
		op, length = self._read_header()
		data_bytes = self._read_exactly(length)
		data = json.loads(data_bytes.decode("utf-8"))
		return op, data

class DiscordRPC_Windows(DiscordRPC):
	def _connect(self):
		self._file = None
		pipe_pattern = "\\\\?\\pipe\\discord-ipc-{}"

		for i in range(10):
			path = pipe_pattern.format(i)

			try:
				self._file = open(path, "wb")
			except:
				continue

			return

		raise Exception("Couldn't connect to Discord pipe")

	def _write(self, data):
		self._file.write(data)
		self._file.flush()

	def _read(self, length):
		return self._file.read(length)

	def _close(self):
		self._file.close()

class DiscordRPC_Unix(DiscordRPC):
	def _connect(self):
		self._socket = socket.socket(socket.AF_UNIX)
		pipe_pattern = self._get_pipe_pattern()

		for i in range(10):
			path = pipe_pattern.format(i)
			if not os.path.exists(path):
				continue

			try:
				self._socket.connect(path)
			except:
				continue

			return

		raise Exception("Couldn't connect to Discord pipe")

	def _get_pipe_pattern(self):
		environment_keys = [ "TEMP", "TMP", "TMPDIR", "XDG_RUNTIME_DIR" ]
		directory = "/tmp"

		for key in environment_keys:
			directory = os.environ.get(key)
			if directory is not None:
				break

		return os.path.join(directory, "discord-ipc-{}")

	def _write(self, data):
		self._socket.sendall(data)

	def _read(self, length):
		return self._socket.recv(length)

	def _close(self):
		self._socket.close()
