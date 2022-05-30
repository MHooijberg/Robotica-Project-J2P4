from ..IOComponent.Ax12a import Ax12


class ArmDriver:
    def __init__(self):
        self.servoLibrary = Ax12
        self.servoIds = [int]
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

    def MoveTo(self, armPosition):
        pass

    def Dance(self, DanceType):
        pass
