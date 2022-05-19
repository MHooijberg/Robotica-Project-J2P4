import Robot.IOComponent.Motor as Motor
import Robot.Socket as Socket


class Controller:
    RemoteSocket = Socket.BluetoothSocket()
    WebSocket = Socket.WebsiteSocket()
    MotorDriver = Motor.Mdd3aDriver(12, 18, 13, 19)

    def __init__(self):
        pass

    def Update():
        pass
