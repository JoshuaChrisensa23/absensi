import serial

from .protocol import FingerProtocol

class SerialReader:
	def __init__(self,port="/dev/ttyUSB0",baudrate=115200):
		self.ser=serial.Serial(port,baudrate,timeout=1)
		print(f"Connected -> {port}")

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
