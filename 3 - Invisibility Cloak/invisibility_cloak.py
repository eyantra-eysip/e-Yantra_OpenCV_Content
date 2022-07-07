import numpy as np
import cv2
import time

def resize_image(image, scale_factor):
	height, width, _ = image.shape
	width = int(width*scale_factor)
	height = int(height*scale_factor)
	image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
	return image

if __name__ == "__main__":

	capture_video = cv2.VideoCapture("invisibility_video.mp4")

	# give the camera to warm up
	time.sleep(1) 
	count = 0 
	background = 0 
	## Step 1: Capturing the background in the first few seconds of the video

	for i in range(60):
		return_val, background = capture_video.read()
		if return_val == False :
			continue 
	
		background = np.flip(background, axis = 1) # flipping of the frame

	background = resize_image(background, 0.4)

	cv2.imshow("background", background)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# Step 2 : Start Reading frames from the video
	while (capture_video.isOpened()):
		return_val, frame = capture_video.read()
		if not return_val :
			break 
		count = count + 1
		frame = np.flip(frame, axis = 1)
		frame = resize_image(frame, 0.4)


		## Step 3 : Color filtering and creation of mask
		hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		lower = np.array([30, 30, 0])       
		upper = np.array([85, 255, 255])
		mask = cv2.inRange(hsv_image, lower, upper)

	    # Step 4 : Removing noise
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations = 2) ## Erosion followed by dilation. Useful for removing noise
		mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations = 1)
		
		# Step 5 : Creating an inverse mask
		mask2 = cv2.bitwise_not(mask)


		# # Generating the final output
		res1 = cv2.bitwise_and(background, background, mask = mask)
		res2 = cv2.bitwise_and(frame, frame, mask = mask2)
		final_output = cv2.addWeighted(res1, 1, res2, 1, 0)		
		
		cv2.imshow("original", frame)
		# cv2.imshow("mask2", mask2)
		# cv2.imshow("res2", res2)
		cv2.imshow("original", final_output)


		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cv2.destroyAllWindows()