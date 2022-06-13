import time
import unittest
import asyncio
import cv2
import numpy as np
from ExternalComponent.Camera import VideoCaptureThreading

width=1280 
height=720 

class VideoCaptureTest(unittest.TestCase):
    def setUp(self):
        pass

    async def _run():
        cap = VideoCaptureThreading(0)
        cap.start()
        while True:
            await asyncio.sleep(0)
    #        _, frame = cap.read()
    #         cv2.imshow('Frame', frame)
    #         cv2.waitKey(1) & 0xFF

    async def tracking():
        cap = VideoCaptureThreading(0)
        cap.start()
        while True:
            await asyncio.sleep(0)
    #         _, frame = cap.read()
    #         #Convert BGR to HSV
    #         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #         # define range of blue color in HSV
    #         #lower_color_filter = np.array([82, 150, 100])
    #         #upper_color_filter = np.array([90, 255, 255])
    #         lower_color_filter = np.array([0, 150, 0])
    #         upper_color_filter = np.array([30, 255, 255])
    #         # Threshold the HSV image to get only the specified colorsq
    #         mask = cv2.inRange(hsv, lower_color_filter, upper_color_filter)
    #         # Bitwise-AND mask and original image
    #         res = cv2.bitwise_and(frame, frame, mask=mask)

    #         contours, hierarchy = cv2.findContours(
    #         mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #         for cntr in contours:
    #             hull = [cntr]
    #             # cHull = cv.convexHull(contours[cntr])
    #             # cv.drawContours(frame,[cHull], -1, (0, 0, 255), 2)
    #             area = cv2.contourArea(cntr)
    #             # Van de closed contours/hulls degene met de grootste area pakken
    #             if area > 700 and area < 15000:
    #                 cv2.drawContours(frame, hull, -1, (0, 0, 255), 2)

    #         cv2.imshow('frame', frame)
    #         cv2.imshow('mask', mask)
    #         cv2.imshow('res', res)
    #         k = cv2.waitKey(5) & 0xFF
    #         if k == 27:
    #             break
            ret,frame = cap.read()
            
            #Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # define range of blue color in HSV
            2
            #lower_color_filter = np.array([90, 137, 29])
            #upper_color_filter = np.array([124, 255, 118])
            
            lower_color_filter = np.array([100, 206, 30])
            upper_color_filter = np.array([130, 255, 180])

            #lower_color_filter = np.array([88, 255, 255])
            #upper_color_filter = np.array([98, 255, 180])
            
            # Threshold the HSV image to get only the specified colors
            mask = cv2.inRange(hsv, lower_color_filter, upper_color_filter)
            
            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame, frame, mask=mask)

            # Get contours
            contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

            # Centroid X and Y values
            cx = 0
            cy = 0

            # for every contour
            for cntr in contours:
                
                # Find convex hull
                hull = [cv2.convexHull(cntr)]

                # Find moments(average of pixel intensities) for finding centroid
                M = cv2.moments(cntr)

                # Find area for small protective layer
                area = cv2.contourArea(cntr)

                # Calculate centroid coördinates
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])

                    # Small protective layer to get rid of noise
                    if area > 400:
                        cv2.drawContours(frame, hull, -1, (0, 0, 255), 2)
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)

                        # Based on the X coordinates of the centroid tell
                        # the robot to move a certain direction.
                        if cx>450:
                            print("left")
                        if cx<200:
                            print("right")
                        if cx<450 and cx>200:
                            print("middle")

            # Show the images for debugging
            cv2.imshow("mask", mask)
            cv2.imshow("frame", frame)
            cv2.imshow("res", res)

                # On Q press, stop application from running
            if cv2.waitKey(1) & 0xff == ord('q'):
                break




# from enum import Enum
# import cv2 as cv
# import numpy as np
# import time
# import asyncio
# import unittest

# from ExternalComponent.Camera import VideoCaptureThreading


# class VideoCaptureTest(unittest.TestCase):

#     async def GetPositionTrackingObject():
#         cap = VideoCaptureThreading(0)

#         while True:
#             _, frame = cap.read()
#             #Convert BGR to HSV
#             hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#             # define range of blue color in HSV
#             #lower_color_filter = np.array([82, 150, 100])
#             #upper_color_filter = np.array([90, 255, 255])
#             lower_color_filter = np.array([0, 150, 0])
#             upper_color_filter = np.array([30, 255, 255])
#             # Threshold the HSV image to get only the specified colorsq
#             mask = cv.inRange(hsv, lower_color_filter, upper_color_filter)
#             # Bitwise-AND mask and original image
#             res = cv.bitwise_and(frame, frame, mask=mask)

#             contours, hierarchy = cv.findContours(
#             mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

#             for cntr in contours:
#                 hull = [cntr]
#                 # cHull = cv.convexHull(contours[cntr])
#                 # cv.drawContours(frame,[cHull], -1, (0, 0, 255), 2)
#                 area = cv.contourArea(cntr)
#                 # Van de closed contours/hulls degene met de grootste area pakken
#                 if area > 700 and area < 15000:
#                     cv.drawContours(frame, hull, -1, (0, 0, 255), 2)

#             cv.imshow('frame', frame)
#             cv.imshow('mask', mask)
#             cv.imshow('res', res)
#             k = cv.waitKey(5) & 0xFF
#             if k == 27:
#                 break


