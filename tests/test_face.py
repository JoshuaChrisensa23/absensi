import cv2

cascade_path = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"

face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
	print("Failed to load Haar Cascade!")
	exit()

print("Haar Cascade Loaded Sucesfuly.")

cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC,
	cv2.VideoWriter_fourcc(*'MJPG'))

if not cap.isOpened():
	print("Cannot Open Cam")
	exit()

print("Camera Opened")

while True:
	print("1")

	ret, frame = cap.read()

	print("ret =", ret)
	print("2")

	if not ret:
		print("Cannot read frame")
		continue

	print("3")

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(
		gray,
		scaleFactor=1.3, 
		minNeighbors=5, 
		minSize=(80,80)
	)

	print("4")

	for (x, y, w, h) in faces:
		cv2.rectangle(
			frame, 
			(x, y), (x+w, y+h),
			(0,255,0),
			2
		)
	cv2.imshow("Face Recognition", frame)
	
	print("5")

	if cv2.waitKey(1)==27:
		break

cap.release()

cv2.destroyAllWindows()
