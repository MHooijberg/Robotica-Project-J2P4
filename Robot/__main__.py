import asyncio
import cv2 as cv
from ExternalComponent.Camera import Camera
from ComputerVision.Tracker import Tracker

tracker = Tracker()

async def function_2():
    print("Start of function_2.")
    while True:
        await asyncio.sleep(0.01)
        print()
        if (len(Camera.frameList) == 72):
            frame = Camera.GetFrame(71)
            print(type(frame))
            print("Getting Object Position:")
            tracker.GetPositionTrackingObject(frame)
        #print("\n HELLO WORLD \n")

loop = asyncio.get_event_loop()
asyncio.ensure_future(Camera.StreamLoop_Async())
asyncio.ensure_future(function_2())
loop.run_forever()
