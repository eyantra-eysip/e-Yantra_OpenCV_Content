import numpy as np
import cv2

def on_trackbar(val):
	hue_min = cv2.getTrackbarPos("Hue Min", "TrackedBars")
	hue_max = cv2.getTrackbarPos("Hue Max", "TrackedBars")
	sat_min = cv2.getTrackbarPos("Sat Min", "TrackedBars")
	sat_max = cv2.getTrackbarPos("Sat Max", "TrackedBars")
	val_min = cv2.getTrackbarPos("Val Min", "TrackedBars")
	val_max = cv2.getTrackbarPos("Val Max", "TrackedBars")

	print(hue_min, hue_max, sat_min, sat_max, val_min, val_max)

	lower = np.array([hue_min, sat_min, val_min])
	upper = np.array([hue_max, sat_max, val_max])

	img_mask = cv2.inRange(imageHSV, lower, upper)
	
	cv2.imshow("ImageHSV", imageHSV)
	cv2.imshow("ImageMask", img_mask)

if __name__ == "__main__":

	cv2.namedWindow("TrackedBars")
	cv2.resizeWindow("TrackedBars", 640, 240)

	cv2.createTrackbar("Hue Min", "TrackedBars", 0, 179, on_trackbar)
	cv2.createTrackbar("Hue Max", "TrackedBars", 179, 179, on_trackbar)
	cv2.createTrackbar("Sat Min", "TrackedBars", 0, 255, on_trackbar)
	cv2.createTrackbar("Sat Max", "TrackedBars", 255, 255, on_trackbar)
	cv2.createTrackbar("Val Min", "TrackedBars", 0, 255, on_trackbar)
	cv2.createTrackbar("Val Max", "TrackedBars", 255, 255, on_trackbar)
	image = cv2.imread("rubix_2.jpg")

	imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	


	cv2.imshow("Image", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()