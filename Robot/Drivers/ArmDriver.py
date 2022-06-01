from ..IOComponent.Ax12a import Ax12
from ..Types.ArmPosition import ArmPosition

#TODO: Implement head, and maybe it should be positioned seperately from the arm.
# TODO: maybe a head stabilisation code, where the head of the robot is kept stable,
#       based on the position of the other servo's

class ArmDriver:
    servoLibrary = Ax12
    servoIds = [int]

    def __init__(self, baseId, lowerId, upperId, headId):
        self.servos.append(baseId)
        self.servos.append(lowerId)
        self.servos.append(upperId)
        self.servos.append(headId)

    def MoveTo(self, x, y, z):
        pass

    def MoveTo(self, baseAngle, lowerAngle, upperAngle):
        self.servoLibrary.move(self.servoIds[0], baseAngle)
        self.servoLibrary.move(self.servoIds[1], lowerAngle)
        self.servoLibrary.move(self.servoIds[2], upperAngle)

    # TODO: add security for when armPosition is null.
    def MoveTo(self, armPosition):
        match armPosition:
            case ArmPosition.Rest:
                self.servoLibrary.move(self.servoIds[0], 0)
                self.servoLibrary.move(self.servoIds[1], 0)
                self.servoLibrary.move(self.servoIds[2], 0)
            case ArmPosition.Weigh:
                self.servoLibrary.move(self.servoIds[0], 0)
                self.servoLibrary.move(self.servoIds[1], 0)
                self.servoLibrary.move(self.servoIds[2], 0)

    def Dance(self, DanceType):
        pass
