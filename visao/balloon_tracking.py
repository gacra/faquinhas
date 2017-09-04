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

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #hsv = frame

        for color, colorLim in colorsLimits.iteritems():

            # Criacao e tratamendo da mascara
            mask = cv2.inRange(hsv, colorLim[0], colorLim[1])
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            detect = False

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
                area = cv2.contourArea(c)
                (x, y, w, h) = cv2.boundingRect(approx)

                #((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                if h > 10:
                    #cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    #cv2.circle(frame, (int(x), int(y)), int(radius),
                    #           (0, 255, 255), 2)
                    #x = (center[0]-(frameWidth/2.0))/float((frameWidth/2.0))
                    #y = (center[1] - (frameHeight/ 2.0)) / float((frameHeight/2.0))

                    colorsPosition[color] = (x, y, h, area)
                    detect = True



                if ((len(approx) > 8) & (area > 30)):
                    print("Redondo")

                cv2.drawContours(frame, c, -1, (255, 0, 0), 3)

            if detect == False:
                if color in colorsPosition:
                    del colorsPosition[color]

        frame = cv2.flip(frame, 1)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        print(colorsPosition)

except KeyboardInterrupt:
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
