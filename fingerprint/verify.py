from .serial_reader import SerialReader
from .database import FingerprintDatabase

class FingerprintVerifier:
	def __init__(self):
		self.serial = SerialReader()
		self.db = FingerprintDatabase()

	def wait(self):
		print()
		print("Waiting Fingerprint")
		while True:
			user = self.poll()
			if user is not None:
				return user

	def poll(self):
		"""Non-blocking single check. Returns the matched user dict, or None
		if nothing arrived / no match this call."""
		result = self.serial.read()
		if result is None:
			return None
		if result["status"] == "MATCH":
			finger = result["finger_id"]
			user = self.db.get_user(finger)
			if user:
				print()
				print("Verified")
				print(user)
				return user
			print("Fingerprint not registered")
		elif result["status"] == "NO_MATCH":
			print("Unknown Finger")
		return None
