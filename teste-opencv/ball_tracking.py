from collections import deque
import numpy as np
import imutils
import cv2

buffer_size = 64

colorLower = (170, 150, 6)
colorUpper = (180 + 5, 255, 255)

#colorLower = (70, 150, 6)
#colorUpper = (135, 255, 255)

pts = deque(maxlen=buffer_size)

camera = cv2.VideoCapture(0)

while True:

	(grabbed, frame) = camera.read() #grabbed: boolean se o frame foi lido ou nao

	frame = imutils.resize(frame, width=600) #600px -> menos px, mais rapido de processar
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	#Criacao e tratamendo da mascara
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)


	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
 		print(center)

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
	# update the points queue
	#pts.appendleft(center)

	'''
		# loop over the set of tracked points
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 	'''

	# show the frame to our screen
	frame = cv2.flip(frame, 1)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()