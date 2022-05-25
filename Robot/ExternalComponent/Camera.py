import asyncio
import cv2 as cv
import numpy as np


class Camera:
    def __init__(self):
        self.frameList = []
        self.loop = asyncio.get_event_loop()

    def GetFrame(self, frameIndex):
        return self.frameList[frameIndex]

    async def __StreamLoop_Async(self):
        while True:
            _, frame = self.cap.read()
            if (len(self.frameList) < 72):
                self.frameList.append(frame)
            else:
                for x in range(1, 72):
                    self.frameList.insert(x - 1, self.frameList[x])
                self.frameList[71] = frame

    def StartStream(self):
        self.cap = cv.VideoCapture(0)
        asyncio.ensure_future(__StreamLoop_Async())
        self.loop.run_forever()

    def StopStream(self):
        self.loop.stop()
