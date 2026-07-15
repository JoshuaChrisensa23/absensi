import pickle
import time

import cv2
import face_recognition

from .utils import open_camera, close_camera, show_preview, CameraError

class FaceRecognizer:
	def __init__(self,encoding_file="face/encodings.pkl"):
		self.encoding_file=encoding_file
		self.reload()

	def reload(self):
		"""(Re)load encodings.pkl from disk. Call after rebuilding it, e.g.
		following a delete-user operation, so the running process picks up
		the change without restarting."""
		with open(self.encoding_file,"rb") as f:
			data=pickle.load(f)
		self.encodings=data["encodings"]
		self.names=data["names"]

	def verify(self,username,timeout=10):
		cap=open_camera()
		deadline=time.time()+timeout
		matched=False

		try:
			while time.time()<deadline:
				ret, frame=cap.read()

				if not ret:
					time.sleep(0.05)
					continue

				rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				small=cv2.resize(rgb, (0,0), fx=0.5, fy=0.5)
				small_locations=face_recognition.face_locations(small)
				encodings=face_recognition.face_encodings(small, small_locations)

				for encoding, (top,right,bottom,left) in zip(encodings,small_locations):
					top, right, bottom, left = top*2, right*2, bottom*2, left*2
					matches=face_recognition.compare_faces(
						self.encodings,encoding,tolerance=0.45)

					name="Unknown"
					color=(0,0,255)

					if True in matches:
						index=matches.index(True)
						name=self.names[index]
						if name==username:
							color=(0,255,0)

					cv2.rectangle(frame, (left,top), (right,bottom), color, 2)
					cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX,0.7,color,2)

					if True in matches and self.names[matches.index(True)]==username:
						matched=True

				if show_preview("Verify", frame) == 27:
					break

				if matched:
					break

			return matched
		finally:
			close_camera(cap)

	def run_live(self, poll_fingerprint):
		"""Keep the camera open permanently and run live face recognition on
		every frame, instead of opening/closing the camera per fingerprint
		scan. poll_fingerprint must be non-blocking and return a matched user
		dict (or None) - each call is checked against the faces currently on
		screen. Runs until ESC is pressed in the preview window."""
		cap=open_camera()
		recognized_names=set()

		try:
			while True:
				ret, frame=cap.read()

				if not ret:
					time.sleep(0.05)
					continue

				rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				small=cv2.resize(rgb, (0,0), fx=0.5, fy=0.5)
				small_locations=face_recognition.face_locations(small)
				encodings=face_recognition.face_encodings(small, small_locations)

				recognized_names=set()
				for encoding, (top,right,bottom,left) in zip(encodings,small_locations):
					top, right, bottom, left = top*2, right*2, bottom*2, left*2
					matches=face_recognition.compare_faces(
						self.encodings,encoding,tolerance=0.45)

					name="Unknown"
					color=(0,0,255)

					if True in matches:
						name=self.names[matches.index(True)]
						recognized_names.add(name)
						color=(0,255,0)

					cv2.rectangle(frame, (left,top), (right,bottom), color, 2)
					cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX,0.7,color,2)

				user=poll_fingerprint()
				if user is not None:
					if user["username"] in recognized_names:
						print("ACCESS GRANTED")
					else:
						print("ACCESS DENIED")

				if show_preview("Live Recognition", frame) == 27:
					break
		finally:
			close_camera(cap)

	def recognize(self):
		cap=open_camera()

		while True:
			ret, frame=cap.read()

			if not ret:
				return False

			rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			small=cv2.resize(rgb, (0,0), fx=0.5, fy=0.5)
			small_locations=face_recognition.face_locations(small)
			encodings=face_recognition.face_encodings(small, small_locations)

			for encoding, (top,right,bottom,left) in zip(encodings,small_locations):
				top, right, bottom, left = top*2, right*2, bottom*2, left*2
				matches=face_recognition.compare_faces(
					self.encodings,encoding,tolerance=0.45 )

				name="Unknown"

				if True in matches:
					index=matches.index(True)
					name=self.names[index]

				cv2.rectangle(frame, (left,top), (right,bottom), (0,255,0), 2)
				cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

			if show_preview("Recognition", frame) == 27:
				break

		close_camera(cap)
