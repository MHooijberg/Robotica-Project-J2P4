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

    def MoveTo(self, baseAngle, lowerAngle, upperAngle, headAngle):
        self.servoLibrary.move(self.servoIds[0], baseAngle)
        self.servoLibrary.move(self.servoIds[1], lowerAngle)
        self.servoLibrary.move(self.servoIds[2], upperAngle)
        self.servoLibrary.move(self.servoIds[3], headAngle)


    # TODO: add security for when armPosition is null.
    def MoveTo(self, armPosition):
        match armPosition:
            case ArmPosition.Rest:
                self.servoLibrary.move(self.servoIds[0], 0)
                self.servoLibrary.move(self.servoIds[1], 0)
                self.servoLibrary.move(self.servoIds[2], 0)
                self.servoLibrary.move(self.servoIds[3], 0)

            case ArmPosition.Weigh:
                self.servoLibrary.move(self.servoIds[0], 0)
                self.servoLibrary.move(self.servoIds[1], 0)
                self.servoLibrary.move(self.servoIds[2], 0)
                self.servoLibrary.move(self.servoIds[3], 0)


    def Dance(self, DanceType):
        pass

    def StabilizeHead(self):
        #Functions needed: readPosition to return the current position of the servo's.
        #Step 1, get values of the servos
        #Step 2, calculate the desired position of the head servo, by subtracting the 3rd servo's position from the 2nd servo position
        #Step 3, Make the head servo move

        Pos2 = self.servoLibrary.readPosition(self.servoIds[1], 0)
        Pos3 = self.servoLibrary.readPosition(self.servoIds[2], 0)

        Deg2 = Pos2 * 0.29
        Deg3 = Pos3 * 0.29

        HeadPos = Deg3 - Deg2

        self.servoLibrary.move(self.servoIds[3], HeadPos)

