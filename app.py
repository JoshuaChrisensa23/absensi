from fingerprint.verify import FingerprintVerifier
from face.recognize import FaceRecognizer

finger = FingerprintVerifier()
face = FaceRecognizer()

print("SMART ACCESS SYSTEM")

while True:
	user=finger.wait()
	if user is None:
		continue

	print(f"Fingerprint: {user['username']}")
	result =face.verify(user["username"])

	if result:
		print("ACCESS GRAMTED")
	else:
		print("ACCESS DENIED")
