from Types.EmotionState import EmotionState
import serial
from Drivers.SerialDriver import SerialDriver


class Screen:

    def __init__(self):
        pass

    def __SendToDisplay(self, commando):
        data = bytes([commando])
        SerialDriver.write(data)

    def DisplayEmotion(self, emotion):
        if emotion == EmotionState.Angry:
            self.__SendToDisplay("page angry")
        elif emotion == EmotionState.Happy:
            self.__SendToDisplay("page happy")
        elif emotion == EmotionState.Sad:
            self.__SendToDisplay("page sad")
        elif emotion == EmotionState.Neutral:
            self.__SendToDisplay("page neutral")
        elif emotion == EmotionState.Tired:
            self.__SendToDisplay("page tired")
