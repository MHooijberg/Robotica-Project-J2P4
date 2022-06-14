from Controller import Controller
Controller.UpdateLoop()

# import asyncio
# import cv2 as cv
# from ExternalComponent.Camera import Camera
# from ComputerVision.Tracker import Tracker
# from Controller import Controller

#tracker = Tracker()

# async def function_2():
#     print("Start of function_2.")
#     while True:
#         await asyncio.sleep(0.01)
#         print()
#         if (len(Camera.frameList) == 72):
#             frame = Camera.GetFrame(71)
#             print("Getting Object Position:")
#             tracker.GetPositionTrackingObject(frame)
#         #print("\n HELLO WORLD \n")
#
# loop = asyncio.get_event_loop()
# asyncio.ensure_future(Camera.StreamLoop_Async())
# asyncio.ensure_future(function_2())
# loop.run_forever()
# loop.run_forever()


# import asyncio
# import time
# from tracemalloc import get_object_traceback
# from Tests import cameratest

# async def firstWorker():
#     while True:
#         await asyncio.sleep(1)
#         print("First Worker Executed")

# async def secondWorker():
#     while True:
#         await asyncio.sleep(1)
#         print("Second Worker Executed")


# loop = asyncio.get_event_loop()
# try:
#     asyncio.ensure_future(cameratest.VideoCaptureTest._run())
#     asyncio.ensure_future(secondWorker())
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
# finally:
#     print("Closing Loop")
#     loop.close()
