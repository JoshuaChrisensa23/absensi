import pickle
import time

import cv2
import face_recognition

from .utils import open_camera, close_camera, show_preview, CameraError

class FaceRecognizer:
	def __init__(self,encoding_file="face/encodings.pkl"):
		with open(encoding_file,"rb") as f:
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
