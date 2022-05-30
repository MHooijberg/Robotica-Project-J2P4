from ..IOComponent.Ax12a import Ax12


class ArmDriver:
    self.servoLibrary = Ax12
    self.servoIds = [int]

    def __init__(self):
        self.servos.append(69)
        self.servos.append(70)
        self.servos.append(71)
        self.servos.append(72)

    def MoveTo(self, x, y, z):
        pass

    def MoveTo(self, armPosition):
        pass

    def Dance(self, DanceType):
        pass
