import sys
import time

import cv2
import face_recognition
import os

class CameraError(Exception):
	pass

def open_camera(index=0, warmup_frames=10, warmup_timeout=6):
	backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_V4L2

	# Some V4L2 drivers fail to negotiate MJPG and every read() then times
	# out via select(); others only work *with* MJPG forced. Try MJPG first
	# (needed by most USB webcams at this resolution), then fall back to
	# the camera's default format if that never delivers a frame.
	for use_mjpg in (True, False):
		cap = cv2.VideoCapture(index, backend)

		if not cap.isOpened():
			raise CameraError(f"Cannot Open Camera (index={index})")

		if use_mjpg:
			cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
		cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
		cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

		# Discard initial frames: the camera (esp. USB/V4L2) needs a moment
		# to start delivering frames, otherwise early cap.read() calls fail
		# with a "select() timeout" and burn the caller's read budget.
		deadline = time.time() + warmup_timeout
		got_frame = False
		for _ in range(warmup_frames):
			if time.time() > deadline:
				break
			ret, _ = cap.read()
			if ret:
				got_frame = True
				break

		if got_frame:
			return cap

		cap.release()
		print(f"[WARN] Camera warmup failed with {'MJPG' if use_mjpg else 'default'} format (index={index}), retrying...")

	raise CameraError(
		f"Camera opened but never delivered a frame (index={index}) with MJPG or default format. "
		"Check `v4l2-ctl --list-devices` / `--list-formats-ext` on the device, and on Raspberry Pi "
		"make sure the camera has enough USB power (use a powered hub if it disconnects under load)."
	)

_preview_available = True

def show_preview(window_name, frame):
	"""Show a frame if a display is available; degrade to headless otherwise
	(common on Raspberry Pi run over SSH without X). Returns the pressed key
	(masked to 0-255) or -1 if no key/preview."""
	global _preview_available

	if not _preview_available:
		return -1

	try:
		cv2.imshow(window_name, frame)
		return cv2.waitKey(1) & 0xFF
	except cv2.error:
		_preview_available = False
		print(f"[WARN] No display available, continuing headless (window '{window_name}' skipped).")
		return -1

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
