from fingerprint.verify import FingerprintVerifier
from face.recognize import FaceRecognizer
from face.utils import CameraError

finger = FingerprintVerifier()
face = FaceRecognizer()

print("SMART ACCESS SYSTEM")
print("1. Fingerprint dulu, baru buka kamera per scan (lama)")
print("2. Preview kamera permanen + live face recognition, granted dari sidik jari")
mode = input("Pilih mode (1/2): ").strip()

if mode == "2":
	try:
		face.run_live(finger.poll)
	except CameraError as e:
		print(f"CAMERA ERROR: {e}")
else:
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
