from ..IOComponent.Ax12a import Ax12
from ..Types.ArmPosition import ArmPosition


class ArmDriver:
    servoLibrary = Ax12
    servoIds = [int]

    def __init__(self):
        self.servos.append(69)
        self.servos.append(70)
        self.servos.append(71)
        # self.servos.append(72)

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
