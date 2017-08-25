import cv2
import numpy as np
import sys

print(sys.argv[1])
image = cv2.imread(sys.argv[1])

limites = (([17, 5, 100], [65, 56, 200]),
	([86, 31, 0], [255, 200, 50]))

i = 0

for limite in limites:
	i += 1
	inferior = np.array(limite[0])
	superior = np.array(limite[1])

	mask = cv2.inRange(image, inferior, superior)
	output = cv2.bitwise_and(image, image, mask = mask)

	cv2.imshow('image ' + str(i), np.hstack([image, output]))

cv2.waitKey(0)