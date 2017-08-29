import numpy as np
import imutils
import cv2
from collections import deque



def mouse_click(event, x, y, flags, param):
    global firstClick
    global colorsLimits
    global undo

    if event == cv2.EVENT_LBUTTONDOWN:
        color = hsv[y, x]

        undo.append(list(colorsLimits))
        if firstClick == True:
            colorMin = (int(color[0]), int(color[1]), int(color[2]))
            colorsLimits[0] = colorMin
            colorMax = colorMin
            colorsLimits[1] = colorMax
            firstClick = False
        else:
            if color[0] < colorsLimits[0][0]:
                colorsLimits[0] = (int(color[0]), colorsLimits[0][1], colorsLimits[0][2])
            if color[1] < colorsLimits[0][1]:
                colorsLimits[0] = (colorsLimits[0][0], int(color[1]), colorsLimits[0][2])
            if color[2] < colorsLimits[0][2]:
                colorsLimits[0] = (colorsLimits[0][0], colorsLimits[0][1], int(color[2]))
            if color[0] > colorsLimits[1][0]:
                colorsLimits[1] = (int(color[0]), colorsLimits[1][1], colorsLimits[1][2])
            if color[1] > colorsLimits[1][1]:
                colorsLimits[1] = (colorsLimits[1][0], int(color[1]), colorsLimits[1][2])
            if color[2] > colorsLimits[1][2]:
                colorsLimits[1] = (colorsLimits[1][0], colorsLimits[1][1], int(color[2]))
        print(colorsLimits)
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(undo) > 0:
            colorsLimits = undo.pop()
            print("new: " + str(colorsLimits))


colorsLimits = [(0,0,0), (180, 255, 255)]
undo = deque()


camera = cv2.VideoCapture(0)

frameWidth = 600

cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_click)

firstClick = True

try:

    while True:

        (grabbed, frame_cam) = camera.read()

        frame = imutils.resize(frame_cam, width=frameWidth)  # 600px -> menos px, mais rapido de processar

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Criacao e tratamendo da mascara
        mask = cv2.inRange(hsv, colorsLimits[0], colorsLimits[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        if firstClick == False:
            hsv[np.where(mask==[255])] = (120, 255, 255)

        output = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('image', cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR))

        cv2.imshow('mask', output)

        key = cv2.waitKey(1) & 0xFF

except KeyboardInterrupt:
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
