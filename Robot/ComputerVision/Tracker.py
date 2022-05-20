import cv2 as cv
from cv2 import WINDOW_NORMAL
import numpy as np
import Robot.Types.TrackMode as TrackMode
import Robot.Types.ObjectPosition as ObjectPosition


class ComputerVision:
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def GetPositionTrackingObject(self):

        # while True:
        _, self.frame = self.cap.read()

        width = 500

        height = 500

        # Convert BGR to HSV
        hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
        # define range of blue color in HSV
        #lower_color_filter = np.array([82, 150, 100])
        #upper_color_filter = np.array([90, 255, 255])
        lower_color_filter = np.array([100, 206, 30])
        upper_color_filter = np.array([130, 255, 180])
        # Threshold the HSV image to get only the specified colorsq
        mask = cv.inRange(hsv, lower_color_filter, upper_color_filter)
        # Bitwise-AND mask and original image
        res = cv.bitwise_and(self.frame, self.frame, mask=mask)

        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        cx = 0
        cy = 0

        for cntr in contours:
            hull = [cv.convexHull(cntr)]
            M = cv.moments(cntr)
            area = cv.contourArea(cntr)

            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])

                if area > 400:
                    cv.drawContours(self.frame, hull, -1, (0, 0, 255), 2)
                    cv.circle(self.frame, (cx, cy), 5, (0, 255, 255), -1)

                #print("X:", cx, "Y:", cy)
            if cx > 450:
                return ObjectPosition.left
            if cx < 200:
                return ObjectPosition.right
            if cx < 450 and cx > 200:
                return ObjectPosition.middle

                # if cx>450:
                #     print("left")
                # if cx<200:
                #     print("right")
                # if cx<450 and cx>200:
                #     print("middle")

        # cv.namedWindow('frame', WINDOW_NORMAL)
        # cv.resizeWindow('frame', (width, height))

        # cv.imshow('frame', frame)
        # cv.imshow('mask', mask)
        # cv.imshow('res', res)

    def GetMode():
        return TrackMode.none

    # @staticmethod
    # def StartCV():
    #     cap = cv.VideoCapture(0)

    # def StopCV():
    #     cv.destroyAllWindows()
