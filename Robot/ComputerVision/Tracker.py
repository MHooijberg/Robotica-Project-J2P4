import cv2 as cv
from cv2 import WINDOW_NORMAL
import numpy as np
from Types.TrackMode import TrackMode
from Types.ObjectPosition import ObjectPosition
from Types.TrackMode import TrackMode


class Tracker:
    def GetPositionTrackingObject(self, frame, trackMode):
        width = frame.shape[1]

        if trackMode == TrackMode.BlueBlock:
            lower_color_filter = np.array([77, 87, 64])
            upper_color_filter = np.array([88, 182, 215])

        elif trackMode == TrackMode.BlackLine:
            lower_color_filter = np.array([0, 0, 0])
            upper_color_filter = np.array([179, 101, 100])

        lower_color_filter = np.array([78, 244, 89])
        upper_color_filter = np.array([109, 255, 158])

        # Convert BGR to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Threshold the HSV image to get only the specified colors
        mask = cv.inRange(hsv, lower_color_filter, upper_color_filter)

        # Bitwise-AND mask and original image
        res = cv.bitwise_and(frame, frame, mask=mask)

        # Get contours
        contours, hierarchy = cv.findContours(mask, 1, cv.CHAIN_APPROX_NONE)

        # Centroid X and Y values
        cx = 0
        cy = 0
        biggestContour = None
        # for every contour
        for cntr in contours:
            # Find convex hull
            hull = [cv.convexHull(cntr)]

            # Find moments(average of pixel intensities) for finding centroid
            M = cv.moments(cntr)

            # Find area for small protective layer
            area = cv.contourArea(cntr)

            # Calculate centroid coördinates
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])

                if (biggestContour is None) or (area > cv.contourArea(biggestContour)):
                    biggestContour = cntr

        # Small protective layer to get rid of noise
        if biggestContour is not None:
            cv.drawContours(frame, hull, -1, (0, 0, 255), 2)
            cv.circle(frame, (cx, cy), 5, (0, 255, 255), -1)
            widthFactor = width / 100
            # print("X:", cx, "Y:", cy)
            if cx > (int(widthFactor * 66)):
                print("The object position was: Right")
                return ObjectPosition.Right
            elif cx < (int(widthFactor * 33)):
                print("The object position was: Left")
                return ObjectPosition.Left
            elif cx > (int(widthFactor * 33)) and cx < (int(widthFactor * 66)):
                print("The object position was: Middle")
                return ObjectPosition.Middle
        else:
            print("The object position was not found")
            return ObjectPosition.NotFound
        # return frame

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
