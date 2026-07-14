from .serial_reader import SerialReader

class FingerEnroll:
	def __init__(self):
		self.serial=SerialReader()
	def enroll(self,finger_id):
		command = f"ENROLL:{finger_id}"
		self.serial.write(command)
		print("Enroll Request Sent")
