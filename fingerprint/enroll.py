from .serial_reader import SerialReader

PROMPTS = {
	"ENROLL_START": "Starting enrollment...",
	"PLACE_FINGER": "Place your finger on the sensor",
	"REMOVE_FINGER": "Remove your finger",
	"PLACE_AGAIN": "Place the same finger again",
}

class FingerEnroll:
	def __init__(self):
		self.serial=SerialReader()

	def enroll(self,finger_id):
		command = f"ENROLL:{finger_id}"
		self.serial.write(command)
		print("Enroll Request Sent")

		while True:
			result = self.serial.read()
			if result is None:
				continue

			status = result["status"]

			if status in PROMPTS:
				print(PROMPTS[status])
			elif status == "ENROLL_OK":
				return True
			elif status == "ENROLL_FAIL":
				print(f"Enroll failed: {result['reason']}")
				return False
