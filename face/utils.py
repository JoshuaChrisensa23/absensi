import cv2
import face_recognition
import os

class CameraError(Exception):
	pass

def open_camera(index=0):
	cap = cv2.VideoCapture(index)

	if not cap.isOpened():
		raise CameraError("Cannot Open Camera")

	cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)

	return cap

def close_camera(cap):
	if cap:
		cap.release()

	cv2.destroyAllWindows()

def capture_frame(cap):
	ret,frame = cap.read()
	if not ret:
		return None
	return frame

def rgb_frame(frame):
	return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def load_face_image(path):
	if not os.path.exists(path):
		raise FileNotFoundError(path)
	return face_recognition.load_image_file(path)

def detect_face(image):
	return face_recognition.face_locations(image)

def encode_face(image):
	encoding=face_recognition.face_encodings(image)

	if len(encoding) == 0:
		return None

	return encoding[0]

def draw_face_box(frame,locations):
	for top, right, bottom, left in locations:
		cv2.rectangle(
			frame,
			(left,top),
			(right,bottom),
			(0,255,0),
			2
		)
	return frame
