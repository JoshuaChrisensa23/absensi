from fingerprint.enroll import FingerEnroll
from fingerprint.database import FingerprintDatabase

print("SMART ACCESS - FINGERPRINT ENROLLMENT")

finger_id = int(input("Finger ID (slot number, e.g. 3): "))
username = input("Username: ")

enroller = FingerEnroll()
success = enroller.enroll(finger_id)

if success:
	FingerprintDatabase().add_user(finger_id, username)
	print(f"Enrolled '{username}' as finger ID {finger_id}")
else:
	print("Enrollment failed, user not saved.")
