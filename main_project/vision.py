import imutils
import cv2
import pickle


class Vision(Thread):
    # Responsible for handling images from camera

    def __init__(self, camera_number, image_width, debug_mode, world):
        """
        Init vision object
        :param camera_number: Number of the used camera
        :param image_width: Image width in pixels
        :param debug_mode: If True shows the image for debug
        :param world: World object
        """

        '''
        self.colorsLimits = {'blue': [(101, 125, 81), (120, 255, 255)],
                             'green': [(32, 57, 106), (68, 216, 215)],
                             'red': [[(0, 111, 113), (7, 244, 189)], [(179, 229, 156), (179, 229, 156)]]}
        '''

        with open('../calibr.wr', 'rb') as input_file:
            self.colors_limits = pickle.load(input_file)

        print(self.colors_limits)

        self.camera = cv2.VideoCapture(camera_number)
        self.image_width = image_width
        self.debug_mode = debug_mode

        self.world = world

        self.world.init_all_balloons(self.colors_limits.keys())


    def update(self):
        """
        Update world information from camera image
        """
        (_, frame) = self.camera.read()

        frame = imutils.resize(frame, width=self.image_width)

        frame_height = len(frame)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for color, color_limits in self.colors_limits.iteritems():
            # Mask creation and handling
            if color == 'red':
                mask1 = cv2.inRange(hsv_frame, color_limits[0][0],
                                    color_limits[0][1])
                mask1 = cv2.erode(mask1, None, iterations=2)
                mask1 = cv2.dilate(mask1, None, iterations=2)
                mask2 = cv2.inRange(hsv_frame, color_limits[1][0],
                                    color_limits[1][1])
                mask2 = cv2.erode(mask2, None, iterations=2)
                mask2 = cv2.dilate(mask2, None, iterations=2)
                mask = mask2 + mask1
            else:
                mask = cv2.inRange(hsv_frame, color_limits[0], color_limits[1])
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

            all_contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)[-2]

            detection = False

            if len(all_contours) > 0:
                contour = max(all_contours, key=cv2.contourArea)
                approx = cv2.approxPolyDP(contour,
                                          0.01 * cv2.arcLength(contour, True),
                                          True)
                area = cv2.contourArea(contour)
                (_, _, _, height) = cv2.boundingRect(approx)

                M = cv2.moments(contour)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                if height > 10:
                    position_x = (center[0] - (
                            self.image_width / 2.0)) / float(
                        (self.image_width / 2.0))
                    position_y = (center[1] - (frame_height / 2.0)) / float(
                        (frame_height / 2.0))
                    height = height / float(frame_height)

                    self.world.set_balloon(color, position_x, position_y,
                                           height,
                                           area)
                    self.world.has_balloon = True
                    detection = True

                if self.debug_mode:
                    cv2.drawContours(frame, contour, -1, (255, 0, 0), 3)

            if detection is False:
                self.world.set_invisible_balloon(color)

        if self.debug_mode:
            frame = cv2.flip(frame, 1)
            cv2.imshow("Frame", frame)


    def finish(self):
        """
        Release the camera and destroy all windows.
        """
        self.camera.release()
        cv2.destroyAllWindows()
