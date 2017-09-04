import numpy as np
import imutils
import cv2

colorsLimits = {'red': [(170, 150, 6), (180 + 5, 255, 255)],
                'blue': [(96, 150, 6), (120, 255, 255)],
                'green': [(30, 150, 6), (68, 255, 255)]}

colorsPosition = {}

camera = cv2.VideoCapture(0)
#camera = cv2.VideoCapture(1)

frameWidth = 600
cv2.namedWindow("Frame")

try:

    while True:

        (grabbed, frame) = camera.read()

        frame = imutils.resize(frame, width=frameWidth)  # 600px -> menos px, mais rapido de processar

        frameHeight = len(frame)

        output = frame.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect circles in the image
        circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)

        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                print("circulo pra caraio")
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # show the output image
        cv2.imshow("output", np.hstack([frame, output]))
        key = cv2.waitKey(1) & 0xFF

        print("Hey")


except KeyboardInterrupt:
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
