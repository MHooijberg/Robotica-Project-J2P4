# import asyncio
# import cv2 as cv
# import numpy as np


# class Camera:
#     frameList = []
#     loop = asyncio.get_event_loop()
#     cv.VideoCapture(0).release()
#     cap = cv.VideoCapture(0)

#     @staticmethod
#     def GetFrame(frameIndex):
#         return Camera.frameList[frameIndex]

#     @staticmethod
#     async def StreamLoop_Async():
#         print("Start of StreamLoop_Async.")
        
#         while True:
#             _, frame = Camera.cap.read()
#             if (len(Camera.frameList) < 72):
#                 #print("Entered if statement.")
#                 Camera.frameList.append(frame)
#             else:
#                 #print("Entered else statement.")
#                 for x in range(1, 72):
#                     Camera.frameList.insert(x - 1, Camera.frameList[x])
#                 Camera.frameList[71] = frame
#             await asyncio.sleep(0.01)
        

#     @staticmethod
#     def StartStream():
#         asyncio.ensure_future(Camera.StreamLoop_Async())
#         Camera.loop.run_forever()

#     @staticmethod
#     def StopStream():
#         Camera.cap.release()

import threading
import cv2


class VideoCaptureThreading:
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def start(self):
        if self.started:
            print('[!] Threaded video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()