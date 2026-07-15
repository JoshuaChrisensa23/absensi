import os
import shutil

from fingerprint.verify import FingerprintVerifier
from face.recognize import FaceRecognizer
from face.encoder import FaceEncoder
from face.utils import CameraError

SAMPLES_DIR = "face/samples"
ENCODINGS_FILE = "face/encodings.pkl"

finger = FingerprintVerifier()
face = FaceRecognizer()

def delete_user(username):
	"""Remove a user's photos, fingerprint record, and rebuild encodings.pkl
	from the remaining photos. A large/stale samples folder and long-running
	camera sessions are what trigger the segfaults, so pruning old users
	keeps the dataset (and each face_encodings() call) small."""
	sample_path = os.path.join(SAMPLES_DIR, username)

	if os.path.isdir(sample_path):
		shutil.rmtree(sample_path)
		print(f"Deleted photos: {sample_path}")
	else:
		print(f"No photos found for '{username}'")

	removed = finger.db.remove_by_username(username)
	print(f"Removed {removed} fingerprint record(s) for '{username}'")

	encoder = FaceEncoder()
	encoder.encode_folder(SAMPLES_DIR)
	encoder.save(ENCODINGS_FILE)
	face.reload()

print("SMART ACCESS SYSTEM")
print("1. Fingerprint dulu, baru buka kamera per scan (lama)")
print("2. Preview kamera permanen + live face recognition, granted dari sidik jari")
print("3. Hapus data user (foto + fingerprint)")
mode = input("Pilih mode (1/2/3): ").strip()

if mode == "3":
	username = input("Username yang mau dihapus: ").strip()
	confirm = input(f"Yakin hapus semua data '{username}'? (y/n): ").strip().lower()
	if confirm == "y":
		delete_user(username)
	else:
		print("Dibatalkan")
elif mode == "2":
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
