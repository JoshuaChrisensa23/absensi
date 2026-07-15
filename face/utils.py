import sys
import time

import cv2
import face_recognition
import os

class CameraError(Exception):
	pass

def open_camera(index=0, warmup_frames=10, warmup_timeout=2, retries=3):
	backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_V4L2

	# Some USB webcams are flaky on the Pi's onboard USB controller: a single
	# cap.read() can eat the whole warmup budget in one "select() timeout"
	# even though the device works fine a moment later. Reopening the device
	# a few times is more reliable than one long wait.
	for attempt in range(1, retries + 1):
		cap = cv2.VideoCapture(index, backend)

		if not cap.isOpened():
			cap.release()
			print(f"[WARN] Camera open attempt {attempt}/{retries} failed (index={index}), retrying...")
			time.sleep(0.5)
			continue

		# Many USB/V4L2 webcams only stream in MJPG at higher resolutions;
		# without requesting it explicitly the driver may fail to negotiate
		# a working format and every read() times out via select().
		cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
		cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
		cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

		# Discard initial frames: the camera (esp. USB/V4L2) needs a moment
		# to start delivering frames, otherwise early cap.read() calls fail
		# with a "select() timeout" and burn the caller's read budget. Also
		# reject frames that are still essentially black - auto-exposure on
		# some USB webcams takes several frames to ramp up after opening, so
		# a successful read() doesn't always mean a usable picture.
		deadline = time.time() + warmup_timeout
		got_frame = False
		for _ in range(warmup_frames):
			if time.time() > deadline:
				break
			ret, test_frame = cap.read()
			if ret and test_frame.mean() > 10:
				got_frame = True
				break

		if got_frame:
			return cap

		cap.release()
		print(f"[WARN] Camera warmup attempt {attempt}/{retries} failed (index={index}), retrying...")
		time.sleep(0.5)

	raise CameraError(
		f"Camera could not be opened or never delivered a frame (index={index}) after {retries} attempts. "
		"Check `v4l2-ctl --list-devices` / `--list-formats-ext` on the device, and on Raspberry Pi "
		"make sure the camera has enough USB power (use a powered hub if it disconnects under load)."
	)

def show_preview(window_name, frame):
	"""Show a frame if a display is available; degrade to headless otherwise
	(common on Raspberry Pi run over SSH without X). Returns the pressed key
	(masked to 0-255) or -1 if no key/preview."""
	try:
		cv2.imshow(window_name, frame)
		return cv2.waitKey(1) & 0xFF
	except cv2.error as e:
		print(f"[WARN] Preview unavailable this frame (window '{window_name}'): {e}")
		return -1

def close_camera(cap):
	if cap:
		cap.release()
		# Let the V4L2 driver fully tear down before the next open_camera()
		# call (app.py opens/closes the camera every loop iteration); reopening
		# immediately after release() can leave the device stuck delivering
		# no frames ("select() timeout") on some USB webcam/driver combos.
		time.sleep(0.5)

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
