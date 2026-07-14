import os
import sys
import time

import serial

from .protocol import FingerProtocol

DEFAULT_PORT = "COM3" if sys.platform == "win32" else "/dev/ttyUSB0"

class SerialReader:
	def __init__(self,port=None,baudrate=115200):
		port = port or os.environ.get("FINGERPRINT_PORT", DEFAULT_PORT)
		try:
			self.ser=serial.Serial(port,baudrate,timeout=1)
		except serial.SerialException as e:
			raise serial.SerialException(
				f"Could not open fingerprint reader on port {port!r}. "
				f"Make sure the device is plugged in and set the correct port "
				f"via the FINGERPRINT_PORT environment variable (check Device "
				f"Manager > Ports (COM & LPT) on Windows). Original error: {e}"
			) from None

		# Opening the port resets Arduino boards (via DTR); wait for it to
		# finish booting so early writes aren't lost.
		deadline = time.time() + 10
		ready = False
		while time.time() < deadline:
			line = self.ser.readline().decode(errors="ignore").strip()
			if line == "READY":
				ready = True
				break

		suffix = "" if ready else " (no READY signal, board may still be booting)"
		print(f"Connected -> {port}{suffix}")

	def read(self):
		if not self.ser.in_waiting:
			return None

		line = self.ser.readline().decode(
			errors="ignore"
		).strip()

		if line == "":
			return None

		return FingerProtocol.parse(line)

	def write(self,command):
		self.ser.write(
			(command + "\n").encode()
		)
