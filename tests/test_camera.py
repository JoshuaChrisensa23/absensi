import cv2

print("Opening Camera")

cap = cv2.VideoCapture("/dev/video0",cv2.CAP_V4L2)

if not cap.isOpened():
	print("Cannot Open Camera")
	exit()

camera = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
	ret, frame = cap.read()
	if not ret:
		break
	cv2.imshow("Smart Access Camera", frame)
	key = cv2.waitKey(1)

	if key == 27:
		break

cap.release()

cv.destroyAllWindows()

