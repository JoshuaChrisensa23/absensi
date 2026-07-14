import pickle
import time

import cv2
import face_recognition

from .utils import open_camera, close_camera, CameraError

class FaceRecognizer:
	def __init__(self,encoding_file="face/encodings.pkl"):
		with open(encoding_file,"rb") as f:
			data=pickle.load(f)
		self.encodings=data["encodings"]
		self.names=data["names"]

	def verify(self,username,timeout=5):
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
				small=cv2.resize(rgb, (0,0), fx=0.25, fy=0.25)
				locations=[
					(top*4, right*4, bottom*4, left*4)
					for top, right, bottom, left in face_recognition.face_locations(small)
				]
				encodings=face_recognition.face_encodings(rgb, locations)

				for encoding, (top,right,bottom,left) in zip(encodings,locations):
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

				cv2.imshow("Verify", frame)
				if cv2.waitKey(1) & 0xFF == 27:
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
			small=cv2.resize(rgb, (0,0), fx=0.25, fy=0.25)
			locations=[
				(top*4, right*4, bottom*4, left*4)
				for top, right, bottom, left in face_recognition.face_locations(small)
			]
			encodings=face_recognition.face_encodings(rgb, locations)

			for encoding, (top,right,bottom,left)in zip(encodings,locations):
				matches=face_recognition.compare_faces(
					self.encodings,encoding,tolerance=0.45 )

				name="Unknown"

				if True in matches:
					index=matches.index(True)
					name=self.names[index]

				cv2.rectangle(frame, (left,top), (right,bottom), (0,255,0), 2)
				cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

			cv2.imshow("Recognition", frame)

			if cv2.waitKey(1)==27:
				break

		close_camera(cap)
