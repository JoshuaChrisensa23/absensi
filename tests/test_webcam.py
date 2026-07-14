import cv2

cam=cv2.VideoCapture(0)

while True:
	rest,img=cam.read()
	cv2.imshow("Camera",img)
	if cv2.waitKey(1)==27:
		break

cam.release()
cv2.destroyAllWindows()

