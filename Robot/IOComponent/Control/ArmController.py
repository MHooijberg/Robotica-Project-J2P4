from enum import Enum

# TODO: Remove this from this file and give it it's own place.


class ArmPosition(Enum):
    Rest = 0
    WeighPosition = 1
    Folded = 2  # TODO: Research which default positions are needed.


class ArmController:
    def __init__(self):
        pass

    def MoveTo(self, x, y, z):
        pass

    def MoveTo(self, armPosition):
        pass

    def DanceController(self, DanceType):
        pass
