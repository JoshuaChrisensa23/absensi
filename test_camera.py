from face.utils import open_camera, close_camera

cap = open_camera()
print("Camera opened, press ESC in the window to close")

import cv2

while True:
	ret, frame = cap.read()
	if not ret:
		print("Failed to read frame")
		break

	cv2.imshow("Camera Test", frame)
	if cv2.waitKey(1) & 0xFF == 27:
		break

close_camera(cap)
print("Camera closed")
