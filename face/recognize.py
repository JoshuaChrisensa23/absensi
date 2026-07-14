import pickle
import time

import cv2
import face_recognition

from .utils import open_camera, close_camera

class FaceRecognizer:
	def __init__(self,encoding_file="face/encodings.pkl"):
		with open(encoding_file,"rb") as f:
			data=pickle.load(f)
		self.encodings=data["encodings"]
		self.names=data["names"]

	def verify(self,username,timeout=5):
		cap=open_camera()
		deadline=time.time()+timeout

		try:
			while time.time()<deadline:
				ret, frame=cap.read()

				if not ret:
					continue

				rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				locations=face_recognition.face_locations(rgb)
				encodings=face_recognition.face_encodings(rgb, locations)

				for encoding in encodings:
					matches=face_recognition.compare_faces(
						self.encodings,encoding,tolerance=0.45)

					if True in matches:
						index=matches.index(True)
						if self.names[index]==username:
							return True

			return False
		finally:
			close_camera(cap)

	def recognize(self):
		cap=open_camera()

		while True:
			ret, frame=cap.read()

			if not ret:
				return False

			rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			locations=face_recognition.face_locations(rgb)
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
