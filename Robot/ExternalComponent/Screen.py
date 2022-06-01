from ..Types.EmotionState import EmotionState
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
        match emotion:
            case EmotionState.Angry:
                self.__SendToDisplay("page angry")
            case EmotionState.Happy:
                self.__SendToDisplay("page happy")
            case EmotionState.Sad:
                self.__SendToDisplay("page sad")
            case EmotionState.Neutral:
                self.__SendToDisplay("page neutral")
            case EmotionState.Tired:
                self.__SendToDisplay("page tired")

    # TODO Volg deze guide:https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/
    # en calibreer de gewichtssensor en importeer de library.
    def DisplayText(self):
        val = max(0, int(hx.get_weight(5)))
        self.__SendToDisplay(val)
