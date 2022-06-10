from Types.ObjectPosition import ObjectPosition
from ComputerVision.Tracker import Tracker


def ComputerVisionTrackingTest():
    #cvision = ComputerVision()
    last_direction = ObjectPosition.middle
    while True:
        current_direction = Tracker().GetPositionTrackingObject()
        if ObjectPosition.left:
            print("links")
        if ObjectPosition.middle:
            print("midden")
        if ObjectPosition.right:
            print("rechts")
        last_direction = current_direction


ComputerVisionTrackingTest()
