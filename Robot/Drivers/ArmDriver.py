from IOComponent.Ax12a import Ax12
from Types.ArmPosition import ArmPosition
from time import sleep
from Types.Action import Action


class ArmDriver:
    servoLibrary = Ax12()
    servoIds = []

    def __init__(self, baseId, lowerId, upperId, headId):
        self.servoIds.append(baseId)
        self.servoIds.append(lowerId)
        self.servoIds.append(upperId)
        self.servoIds.append(headId)

    def MoveTo(self, x, y, z):
        pass

    # Convert from degrees to position
    def MoveTo(self, baseAngle, lowerAngle, upperAngle, headAngle):
        self.servoLibrary.move(int(self.servoIds[0]), baseAngle)
        self.servoLibrary.move(int(self.servoIds[1]), lowerAngle)
        self.servoLibrary.move(int(self.servoIds[2]), upperAngle)
        #self.servoLibrary.move(int(self.servoIds[3]), headAngle)
        sleep(1)
        self.StabilizeHead()

    # TODO: add security for when armPosition is null.
#     def MoveTo(self, armPosition):
#         match armPosition:
#             case ArmPosition.Rest:
#                 self.servoLibrary.move(self.servoIds[0], 0)
#                 self.servoLibrary.move(self.servoIds[1], 0)
#                 self.servoLibrary.move(self.servoIds[2], 0)
#                 self.servoLibrary.move(self.servoIds[3], 0)
#
#             case ArmPosition.Weigh:
#                 self.servoLibrary.move(self.servoIds[0], 0)
#                 self.servoLibrary.move(self.servoIds[1], 0)
#                 self.servoLibrary.move(self.servoIds[2], 0)
#                 self.servoLibrary.move(self.servoIds[3], 0)

    def Dance(self, DanceType):
        pass

    def StabilizeHead(self):
        # Functions needed: readPosition to return the current position of the servo's.
        # Step 1, get values of the servos
        # Step 2, calculate the desired position of the head servo, by subtracting the 3rd servo's position from the 2nd servo position
        # Step 3, Make the head servo move

        # TODO: Put the 0.29 and 150 magic numbers into variables

        pos2 = self.servoLibrary.readPosition(self.servoIds[1])
        pos3 = self.servoLibrary.readPosition(self.servoIds[2])
        currentHeadPos = self.servoLibrary.readPosition(self.servoIds[3])

        # Convert to degrees
        deg2 = pos2 * 0.29
        deg3 = pos3 * 0.29
        degHead = currentHeadPos * 0.29

        relativeDeg2 = deg2 - 150
        relativeDeg3 = deg3 - 150
        relativeHeadDeg = degHead - 150

        totalRotation = relativeDeg2 + relativeDeg3  # + relativeHeadDeg
        neededRotation = 180 - totalRotation

        headPos = int((neededRotation + 150) / 0.29)

        print("\n==== Servo Information ====")
        print("Servo ", str(self.servoIds[1]), ": Position ", str(
            pos2), " | Degrees ", str(deg2), " | Relative Degrees ", str(relativeDeg2))
        print("Servo ", str(self.servoIds[2]), ": Position ", str(
            pos3), " | Degrees ", str(deg3), " | Relative Degrees ", str(relativeDeg3))
        print("Head Servo ", str(self.servoIds[3]), ": Position ", str(currentHeadPos), " | Degrees ", str(degHead), " | Relative Degrees ", str(
            relativeHeadDeg), " | Needed Rotation ", str(neededRotation), " | Absolute End Rotation ", str(neededRotation + 150), " | Absolute End Position ", str(headPos))
        print("==== End Of Servo Information ====\n")

        # TODO: Jur er moet alleen nog gekeken worden of de neededRotation links om of rechts om gaat. hoe? geen idee.
        self.servoLibrary.move(int(self.servoIds[3]), headPos)

    def moveDirection(self, step, direction):

        if direction == Action.Up:

            self.servoLibrary.move(int(self.servoIds[1]), step)
            self.servoLibrary.move(int(self.servoIds[2]), step)

        elif direction == Action.Down:

            self.servoLibrary.move(int(self.servoIds[1]), step)
            self.servoLibrary.move(int(self.servoIds[2]), step)

        elif direction == Action.Left:

            self.servoLibrary.move(int(self.servoIds[0]), step)

        elif direction == Action.Right:

            self.servoLibrary.move(int(self.servoIds[0]), step)
