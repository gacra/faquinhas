import numpy as np
import imutils
import cv2


def mouse_click(event, x, y, flags, param):
    global firstClick

    if event == cv2.EVENT_LBUTTONDOWN:
        color = frame[y, x]

        print(color)
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

colorsLimits = [(0,0,0), (255, 255, 255)]

camera = cv2.VideoCapture(0)

frameWidth = 600

cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_click)

firstClick = True

#try:
while True:

    while True:

        (grabbed, frame_cam) = camera.read()

        frame = imutils.resize(frame_cam, width=frameWidth)  # 600px -> menos px, mais rapido de processar

        # Criacao e tratamendo da mascara
        mask = cv2.inRange(frame, colorsLimits[0], colorsLimits[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        output = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('image', frame)

        cv2.imshow('mask', output)

        key = cv2.waitKey(1) & 0xFF

#except:
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
