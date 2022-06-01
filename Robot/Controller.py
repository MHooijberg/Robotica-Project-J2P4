from .ComputerVision import Tracker
from .Drivers import ArmDriver
#from .ExternalComponent import Camera
from .ExternalComponent import Screen
from .IOComponent import Hcsr04
from .IOComponent import Magnet
from .IOComponent import Mdd3aDriver
from .Socket import BluetoothSocket
# TODO: Don't import all form a folder, this is bad practice.
from .Types import *

# ================
# ---- Notes: ----
# ================
# Steps to make the controller:
#   1. Initialise all the necessary components.
#   2. Setup al the default values and states.
#   3.
#
#
# Ideas to make the function work:
#   - There needs to be different states so that we know what's going on.
#   - Do we need to have a MotorAction type to save the current action?
#   - What does the robot need to do after booting up?
#   -
#
# #


class Controller:
    # ===========================
    # ---- Pin configuration ----
    # ===========================
    M1A_PIN = 12
    M1B_PIN = 18
    M2A_PIN = 13
    M2B_PIN = 19

    # TODO: Make all IOComponents configureable with pins
    ObjectTracker = Tracker()
    Arm = ArmDriver()
    Screen = Screen()
    MotorDriver = Mdd3aDriver(12, 18, 13, 19)

    def __init__(self):
        pass

    def Update():
        pass
