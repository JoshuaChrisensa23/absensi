from fingerprint.enroll import FingerEnroll
from fingerprint.database import FingerprintDatabase
from face.register import FaceRegister
from face.encoder import FaceEncoder

print("SMART ACCESS - FINGERPRINT ENROLLMENT")

finger_id = int(input("Finger ID (slot number, e.g. 3): "))
username = input("Username: ")

enroller = FingerEnroll()
success = enroller.enroll(finger_id)

if success:
	FingerprintDatabase().add_user(finger_id, username)
	print(f"Enrolled '{username}' as finger ID {finger_id}")

	print()
	print("Now registering face photos for this user...")
	FaceRegister().register(username)

	encoder = FaceEncoder()
	encoder.encode_folder("face/samples")
	encoder.save("face/encodings.pkl")
else:
	print("Enrollment failed, user not saved.")
