import numpy as np
import imutils
import cv2

camera = cv2.VideoCapture(0)

try:

    while True:

        (grabbed, frame) = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 50, 150)

        # find contours in the edge map
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(edged, cnts, -1, (255,0,0), 3)

        cv2.imshow("output", edged)
        key = cv2.waitKey(1) & 0xFF
except:
    pass