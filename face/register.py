import os
import cv2
import face_recognition

from .utils import open_camera, close_camera, show_preview

class FaceRegister:
	def __init__(self, sample_dir="face/samples"):
		self.sample_dir=sample_dir
	def register(self, username, total_images=20):
		save_path=os.path.join(self.sample_dir,username)
		os.makedirs(save_path, exist_ok=True)

		cap=open_camera()

		print(f"Register face: {username}")
		print("Press Space to capture")
		print("Press ESC to cancel")

		count=0
		while True:
			ret, frame=cap.read()
			if not ret:
				continue

			small=cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
			rgb=cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
			locations=[
				(top*2, right*2, bottom*2, left*2)
				for top, right, bottom, left in face_recognition.face_locations(rgb)
			]

			for top, right, bottom, left in locations:
				cv2.rectangle(frame, (left,top), (right, bottom), (0,255,0), 2)
			key=show_preview("Register Face", frame)

			if key ==27:
				break

			if key ==32:
				if len(locations) != 1:
					print("Exactly One face must be visible.")
					continue
				filename = os.path.join(
					save_path, f"{count+1:03}.jpg"
				)
				cv2.imwrite(filename, frame)
				count += 1

				print(f"Saved {filename}")

				if count >= total_images:
					break

		close_camera(cap)

		print()
		print(f"Registration Finished({count}images)")
