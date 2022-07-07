import numpy as np
import cv2


if __name__ == "__main__":

	# define a video capture object
	vid = cv2.VideoCapture(1)
	
	while(True):
		
		# Capture the video frame
		# by frame
		ret, frame = vid.read()


		### Step 1 : Convert frame to HSV
		hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		### Step 2: Select lower and upper bounds for color filtering to create a mask
		lower = np.array([0, 85, 176])
		upper = np.array([40, 255, 255])
		mask = cv2.inRange(hsv_image, lower, upper)

		### Step 3: Remove Noise in Image
		kernel = np.ones((5,5), np.uint8)
		mask = cv2.erode(mask, kernel, iterations=1)

		### Step 4: Find and draw Contours
		contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		# print(contours)
		
		# frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)

		## Step 5: Take only the largest contour as the main contour
		main_contour = []
		for cnt in contours:
			area = cv2.contourArea(cnt)
			if area > 200:
				main_contour.append(cnt)

		frame = cv2.drawContours(frame, main_contour, -1, (0, 0, 255), 3)
		# # print(len(main_contour))

		## Step 6: Calculate the centroid of the object
		try:
			M = cv2.moments(main_contour[0])			
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			print(M)

			text = str((cx, cy))
			frame = cv2.putText(frame, text, (cx, cy),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
		except Exception as e:
			print(e)
			pass

	
		# Display the resulting frame
		cv2.imshow('frame', frame)
		# cv2.imshow('HSV', hsv_image)
		cv2.imshow('mask', mask)
		
		# the 'q' button is set as the
		# quitting button you may use any
		# desired button of your choice
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	# After the loop release the cap object
	vid.release()
	# Destroy all the windows
	cv2.destroyAllWindows()

