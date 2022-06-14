from time import sleep
from turtle import pos
from IOComponent.Ax12a import Ax12
from Types.ArmPosition import ArmPosition
from Types.Action import Action
from Types.ArmPart import ArmPart


class ArmDriver:
    # ==== Notes: ====
    # TODO: Put the 0.29 and 150 magic numbers into variables.
    # TODO: Jur er moet alleen nog gekeken worden of de neededRotation links om of rechts om gaat. hoe? geen idee.
    # TODO: Discuss if we want custom types instead of boolean variables for things like inDegrees = False
    # TODO: Discuss if this class should contain code like Rotate but for base etc since now its the controllers JOB
    # TODO: add security for when armPosition is null in the MoveTo(ArmPosition) method.
    # TODO: Discuss if MoveTo(self, armPosition) is needed?
    # TODO: Remove magic numbers and implement the fold, weigh and zero position in the __init__
    #
    # Arm structure array:
    #   [[Base Servo Id's], [Arm Servo Id's], [Head Servo Id's]]
    # Position structure array:
    #   [Base Angle, [Arm Angles], Head Angle]

    ServoLibrary = Ax12()
    BaseIds = []
    ArmIds = []
    HeadIds = []

    def __init__(self, armStructure, conversionNumber, defaultStabilisationAmount, zeroPostion, foldPosition, weighPosition):
        for x in armStructure[0]:
            self.BaseIds.append(x)
        for x in armStructure[1]:
            self.ArmIds.append(x)
        for x in armStructure[2]:
            self.HeadIds.append(x)
        self.FoldPosition = foldPosition
        self.WeighPosition = weighPosition
        self.ZeroPostion = zeroPostion
        self.ConversionNumber = conversionNumber
        self.DefaultStabilisationAmount = defaultStabilisationAmount

    def MoveTo(self, x, y, z):
        pass

    # Convert from degrees to position
    def MoveTo(self, position, shouldStabalizeHead=True):
        for id in self.BaseIds:
            self.ServoLibrary.move(id, int(position[0]))
        for x in range(len(position[1])):
            self.ServoLibrary.move(self.ArmIds[x], int(position[1][x]))

        if shouldStabalizeHead:
            self.StabilizeHead()
        else:
            for id in self.HeadIds:
                self.ServoLibrary.move(id, int(position[2]))

    def MoveTo(self, armPosition):
        if armPosition == ArmPosition.Zero:
            position = self.ZeroPostion * self.ConversionNumber
            for x in self.BaseIds:
                self.ServoLibrary.move(x, position)
            for x in self.ArmIds:
                self.ServoLibrary.move(x, position)
            for x in self.HeadIds:
                self.ServoLibrary.move(x, position)
        elif armPosition == ArmPosition.Folded:
            self.MoveTo(self.FoldPosition)
        elif armPosition == ArmPosition.Weigh:
            self.MoveTo(self.FoldPosition)

    def StabilizeHead(self):
        armPositions = []
        headPositions = []

        for id in self.ArmIds:
            armPositions.append(self.ServoLibrary.readPosition(id))
        for id in self.HeadIds:
            headPositions.append(self.ServoLibrary.readPosition(id))

        armDegrees = [self.ConversionNumber * x for x in armPositions]
        relativeArmDegrees = [x - self.ZeroPostion for x in armDegrees]
        totalArmDegrees = sum(relativeArmDegrees)

        neededRotation = 180 - totalArmDegrees

        self.Rotate(ArmPart.Head, neededRotation, True)

        # print("\n==== Servo Information ====")
        # print("Servo ", str(self.servoIds[1]), ": Position ", str(
        #     pos2), " | Degrees ", str(deg2), " | Relative Degrees ", str(relativeDeg2))
        # print("Servo ", str(self.servoIds[2]), ": Position ", str(
        #     pos3), " | Degrees ", str(deg3), " | Relative Degrees ", str(relativeDeg3))
        # print("Head Servo ", str(self.servoIds[3]), ": Position ", str(currentHeadPos), " | Degrees ", str(degHead), " | Relative Degrees ", str(
        #     relativeHeadDeg), " | Needed Rotation ", str(neededRotation), " | Absolute End Rotation ", str(neededRotation + 150), " | Absolute End Position ", str(headPos))
        # print("==== End Of Servo Information ====\n")

    def Rotate(self, armPart, amount, inDegrees=False):
        if (amount != 0):
            currentPosition = []

            if inDegrees:
                amount /= self.ConversionNumber

            if armPart == ArmPart.Base:
                idArray = self.BaseIds
            elif armPart == ArmPart.Arm:
                idArray = self.ArmIds
            elif armPart == ArmPart.Head:
                idArray = self.HeadIds

            for id in idArray:
                currentPosition.append(self.ServoLibrary.readPosition(id))

            for i in range(len(currentPosition)):
                moveAmount = amount if type(amount) is int else amount[i]
                self.ServoLibrary.move(
                    idArray[i], currentPosition[i] + moveAmount)
