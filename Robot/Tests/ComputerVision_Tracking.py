import Robot.Types.ObjectPosition as ObjectPosition
import Robot.ComputerVision.Tracker as Tracker


def ComputerVisionTrackingTest():
    #cvision = ComputerVision()
    last_direction = ObjectPosition.middle
    while True:
        current_direction = Tracker().GetPositionTrackingObject()
        if (current_direction != last_direction):
            match current_direction:
                case ObjectPosition.left:
                    print("links")
                case ObjectPosition.middle:
                    print("midden")
                case ObjectPosition.right:
                    print("rechts")
            last_direction = current_direction


# TODO: Define how we test, now this code will be executed after importing (if I'm not mistaken).
ComputerVisionTrackingTest()
