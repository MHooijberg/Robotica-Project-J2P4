import asyncio
import cv2 as cv
import numpy as np


class Camera:
    frameList = []
    loop = asyncio.get_event_loop()
    cv.VideoCapture(0).release()
    cap = cv.VideoCapture(0)

    @staticmethod
    def GetFrame(frameIndex):
        return Camera.frameList[frameIndex]

    @staticmethod
    async def StreamLoop_Async():
        print("Start of StreamLoop_Async.")
        
        while True:
            _, frame = Camera.cap.read()
            if (len(Camera.frameList) < 72):
                #print("Entered if statement.")
                Camera.frameList.append(frame)
            else:
                #print("Entered else statement.")
                for x in range(1, 72):
                    Camera.frameList.insert(x - 1, Camera.frameList[x])
                Camera.frameList[71] = frame
            await asyncio.sleep(0.01)
        

    @staticmethod
    def StartStream():
        asyncio.ensure_future(Camera.StreamLoop_Async())
        Camera.loop.run_forever()

    @staticmethod
    def StopStream():
        Camera.cap.release()
