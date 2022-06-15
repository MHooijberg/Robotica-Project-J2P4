from Types.EmotionState import EmotionState
import serial


class Screen:

    def __init__(self):
        pass

    def __SendToDisplay(self, commando):
        ser = serial.Serial(
            port='/dev/serial0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        data = bytes([commando])
        ser.write(data)

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
