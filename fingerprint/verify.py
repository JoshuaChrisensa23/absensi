from .serial_reader import SerialReader
from .database import FingerprintDatabase

class FingerprintVerifier:
	def __init(self):
		self.serial = SerialReader()
		self.db = FingerprintDatabase()

	def wait(self):
		print()
		print("Waiting Fingerprint")
		while True:
			result = self.serial.read()
			if result is None:
				continue
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
