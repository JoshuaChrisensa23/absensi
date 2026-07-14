import cv2

for i in range(6):
	cap = cv2.VideoCapture(i, cv2.CAP_V4L2)

	if cap.isOpened():
		print(f"Camera Found at index  {i}")
		ret, frame = cap.read()
		
		if ret:
			print("Frame recieved")
		else:
			print("Cannot read frame")

		cap.release()

	else:
		print(f"Index {i} not available")

