import numpy as np
import imutils
import cv2
import sys
from collections import deque

def mouse_click_red(event, x, y, flags, param):
    global firstClick
    global colorsLimits
    global undo

    if event == cv2.EVENT_LBUTTONDOWN:
        color = frame[y, x]

        undo.append([list(colorsLimits[0]), list(colorsLimits[1])])
        if firstClick == True:
            colorsLimits[0][0] = colorsLimits[0][1] = (0, int(color[1]), int(color[2]))
            colorsLimits[1][0] = colorsLimits[1][1] = (179, int(color[1]), int(color[2]))
            firstClick = False
        else:
            if color[0] < 90:
                if color[1] < colorsLimits[0][0][1]:
                    colorsLimits[0][0] = (colorsLimits[0][0][0], int(color[1]), colorsLimits[0][0][2])
                if color[2] < colorsLimits[0][0][2]:
                    colorsLimits[0][0] = (colorsLimits[0][0][0], colorsLimits[0][0][1], int(color[2]))
                if color[0] > colorsLimits[0][1][0]:
                    colorsLimits[0][1] = (int(color[0]), colorsLimits[0][1][1], colorsLimits[0][1][2])
                if color[1] > colorsLimits[0][1][1]:
                    colorsLimits[0][1] = (colorsLimits[0][1][0], int(color[1]), colorsLimits[0][1][2])
                if color[2] > colorsLimits[0][1][2]:
                    colorsLimits[0][1] = (colorsLimits[0][1][0], colorsLimits[0][1][1], int(color[2]))
            else:
                if color[1] < colorsLimits[1][0][1]:
                    colorsLimits[1][0] = (colorsLimits[1][0][0], int(color[1]), colorsLimits[1][0][2])
                if color[2] < colorsLimits[1][0][2]:
                    colorsLimits[1][0] = (colorsLimits[1][0][0], colorsLimits[1][0][1], int(color[2]))
                if color[0] < colorsLimits[1][0][0]:
                    colorsLimits[1][0] = (int(color[0]), colorsLimits[1][0][1], colorsLimits[1][0][2])
                if color[1] > colorsLimits[1][1][1]:
                    colorsLimits[1][1] = (colorsLimits[1][1][0], int(color[1]), colorsLimits[1][1][2])
                if color[2] > colorsLimits[1][1][2]:
                    colorsLimits[1][1] = (colorsLimits[1][1][0], colorsLimits[1][1][1], int(color[2]))
        print(colorsLimits)
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(undo) > 0:
            colorsLimits = undo.pop()
            print("Undo: " + str(colorsLimits))
            if len(undo) == 0:
                firstClick = True

def mouse_click(event, x, y, flags, param):
    global firstClick
    global colorsLimits
    global undo

    if event == cv2.EVENT_LBUTTONDOWN:
        color = frame[y, x]

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
            print("Undo: " + str(colorsLimits))
            if len(undo) == 0:
                firstClick = True

def rgbColorPicker(colorLimitsIni, undoIni):
    global colorsLimits
    global camera
    global firstClick
    global frame
    global undo

    cv2.setMouseCallback("image", mouse_click)
    colorsLimits = [(0, 0, 0), (255, 255, 255)]
    undo = deque()

    firstClick = True

    if colorLimitsIni is not None:
        colorsLimits = colorLimitsIni
        firstClick = False
        undo = undoIni

    while True:

        (grabbed, frame_cam) = camera.read()

        frame = imutils.resize(frame_cam, width=frameWidth)  # 600px -> menos px, mais rapido de processar

        rgb = frame.copy()

        # Criacao e tratamendo da mascara
        mask = cv2.inRange(rgb, colorsLimits[0], colorsLimits[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        if firstClick == False:
            rgb[np.where(mask == [255])] = (120, 255, 255)

        output = cv2.bitwise_and(frame, frame, mask=mask)

        # cv2.imshow('image', cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR))
        cv2.imshow('image', rgb)

        cv2.imshow('mask', output)

        key = cv2.waitKey(10)

        if key == 27:
            return colorsLimits

def hsvColorPicker(cor, colorLimitsIni, undoIni):
    global colorsLimits
    global camera
    global firstClick
    global frame
    global undo

    firstClick = True
    undo = deque()

    if (cor == 'red'):
        colorsLimits = [[(0, 0, 0), (180, 255, 255)], [(179, 0, 0), (179, 255, 255)]]
        cv2.setMouseCallback("image", mouse_click_red)
    else:
        colorsLimits = [(0,0,0), (180, 255, 255)]
        cv2.setMouseCallback("image", mouse_click)
    if colorLimitsIni is not None:
        colorsLimits = colorLimitsIni
        firstClick = False
        undo = undoIni

    while True:

        (grabbed, frame_cam) = camera.read()

        frame = imutils.resize(frame_cam, width=frameWidth)  # 600px -> menos px, mais rapido de processar

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hsv = frame.copy()

        # Criacao e tratamendo da mascara
        if(cor == 'red'):
            mask1 = cv2.inRange(hsv, colorsLimits[0][0], colorsLimits[0][1])
            mask1 = cv2.erode(mask1, None, iterations=2)
            mask1 = cv2.dilate(mask1, None, iterations=2)
            mask2 = cv2.inRange(hsv, colorsLimits[1][0], colorsLimits[1][1])
            mask2 = cv2.erode(mask2, None, iterations=2)
            mask2 = cv2.dilate(mask2, None, iterations=2)
            mask = mask1+mask2
        else:
            mask = cv2.inRange(hsv, colorsLimits[0], colorsLimits[1])
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

        if firstClick == False:
            hsv[np.where(mask == [255])] = (120, 255, 255)

        output = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('image', cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR))

        cv2.imshow('mask', cv2.cvtColor(output, cv2.COLOR_HSV2BGR))

        key = cv2.waitKey(10)

        if key == 27:
            return colorsLimits

if __name__ == '__main__':

    colorsLimits = []
    undo = deque()
    firstClick = True

    result = {}
    dicUndo = {}

    camera = cv2.VideoCapture(0)

    frame = None

    frameWidth = 600

    cv2.namedWindow("image")

    try:
        if len(sys.argv) == 2:
            while True:
                cor = raw_input('Nome da cor: ')
                colorLimitsIni = result.get(cor)
                undoIni = dicUndo.get(cor)
                if cor == '':
                    break
                if sys.argv[1] == 'rgb':
                    range = rgbColorPicker(colorLimitsIni, undoIni)
                elif sys.argv[1] == 'hsv':
                    range = hsvColorPicker(cor, colorLimitsIni, undoIni)
                result[cor] = range
                dicUndo[cor] = undo.__copy__()
                print(dicUndo)
        else:
            print("Uso python colorPicker.py [rgb|hsv]")

    except KeyboardInterrupt:
        print()
        print(result)
        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()