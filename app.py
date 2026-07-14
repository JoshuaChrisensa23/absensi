from fingerprint.verify import FingerprintVerifier
from face.recognize import FaceRecognizer
from face.utils import CameraError

finger = FingerprintVerifier()
face = FaceRecognizer()

print("SMART ACCESS SYSTEM")

while True:
	user=finger.wait()
	if user is None:
		continue

	print(f"Fingerprint: {user['username']}")

	try:
		result = face.verify(user["username"])
	except CameraError as e:
		print(f"CAMERA ERROR: {e}")
		continue

	if result:
		print("ACCESS GRANTED")
	else:
		print("ACCESS DENIED")
