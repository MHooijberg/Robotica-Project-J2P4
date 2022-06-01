import asyncio
from ExternalComponent.Camera import Camera
import cv2 as cv


async def function_2():
    print("Start of function_2.")
    while True:
        await asyncio.sleep(0.01)
        if (len(Camera.frameList) == 72):
            frame = Camera.GetFrame(71)
            print(type(frame))
            cv.imshow('ffkes een tessie', frame)
        print("\n HELLO WORLD \n")

loop = asyncio.get_event_loop()
asyncio.ensure_future(Camera.StreamLoop_Async())
asyncio.ensure_future(function_2())
loop.run_forever()
