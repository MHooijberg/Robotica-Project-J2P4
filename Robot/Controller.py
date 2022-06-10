# ==== General Imports: ====
import asyncio
from bleak import BleakClient

# ==== Package Imports ====
from ComputerVision.Tracker import Tracker
from Drivers.ArmDriver import ArmDriver
from Drivers.WheelDriver import WheelDriver
from ExternalComponent.Remote import Remote
from ExternalComponent.Screen import Screen
from IOComponent.Hcsr04 import Hcsr04
from IOComponent.Magnet import Magnet
from Types.SteeringMode import SteeringMode

# ================
# ---- Notes: ----
# ================
# TODO: Implement setting to set steering at max value, (turning 1 wheel or rotating around axis)
# TODO: Implement a setting to set from when it needs to turn in the special way.
#
# Robot life cycle steps:
#   1. Initialize Objects.
#   2. Go to starting position:
#        - Wheels on brake
#        - Arm in folded position
#   3. Go into update cycle:
#        - Connect to bluetooth controller
#        - Read instructions from controller.
#        - Execute instruction / command:
#           - Drive:
#           - Arm:
#           -
#        -

# Update Loop Cycle:
#   1. Retrieve Settings from remote.
#   2. Change State based on the remote settings.
#   3. Start / Keep doing action if State Changed.
#   4. Repeat.
# TODO: Discuss with group about being able to controll the arm while driving.


class Controller:
    # ===============================
    # ---------- Settings -----------
    # ===============================
    ShouldTurnnOff = False

    # ===============================
    # ------ Pin configuration ------
    # ===============================
    M1A_PIN = 12
    M1B_PIN = 18
    M2A_PIN = 13
    M2B_PIN = 19
    # MAGNET_PIN =

    # ===============================
    # ---- Remote  configuration ----
    # ===============================
    ADDRESS = "78:E3:6D:12:1B:C6"
    UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
    CENTER_X_LEFT = 1959
    CENTER_Y_LEFT = 1644
    CENTER_X_RIGHT = 1755
    CENTER_Y_RIGHT = 1782
    RANGE = 2047
    INNER_DEADZONE = 7
    OUTER_DEADZONE = 100

    # ===============================
    # ----- Servo configuration -----
    # ===============================
    BASE_SERVO_ID = 69
    LOWER_ARM_SERVO_ID = 70
    UPPER_ARM_SERVO_ID = 71
    HEAD_SERVO_ID = 72

    # ===============================
    # ---- Driving configuration ----
    # ===============================
    STEERING_MODE = SteeringMode.static

    # ===============================
    # ------- Starting States -------
    # ===============================

    # ===============================
    # ------ Object  Instances ------
    # ===============================
    ObjectTracker = Tracker()
    Arm = ArmDriver(BASE_SERVO_ID, LOWER_ARM_SERVO_ID,
                    UPPER_ARM_SERVO_ID, HEAD_SERVO_ID)
    Remote = Remote(ADDRESS, UUID, CENTER_X_LEFT, CENTER_Y_LEFT,
                    CENTER_X_RIGHT, CENTER_Y_RIGHT, RANGE, INNER_DEADZONE, OUTER_DEADZONE)
    Screen = Screen()
    #Magnet = Magnet(MAGNET_PIN)
    MotorDriver = WheelDriver(M1A_PIN, M1B_PIN, M2A_PIN, M2B_PIN)

    @staticmethod
    async def Update_Loop():

        while Controller.ShouldTurnnOff is False:
            # Try to connect with the controller. If it succeeds, perform handle the commands.
            try:
                async with BleakClient(Controller.ADDRESS, timeout=0.5) as client:
                    # Keep reading instructions untill the robot is told to turn off.
                    while Controller.ShouldTurnnOff is False:
                        # Read data from the remote.
                        command_array = await Controller.Remote.ReceiveData(client)
                        # If we don't receive any data, terminate this iteration and try again.
                        if command_array is None:
                            continue

                        # Handle the manual control menu.
                        elif command_array[4] == "Manually":
                            # Drive
                            if command_array[5] == "ON":
                                joystickA = Controller.Remote.JoystickToPercentage(
                                    command_array[0], command_array[2], True)
                                Controller.Drive(joystickA)
                            # Control Arm
                            elif command_array[6] == "ON":
                                pass
                            # Turn on and off the magnet.
                            if command_array[7] == "ON":
                                Controller.Magnet.turnON()
                            elif command_array[7] == "OFF":
                                Controller.Magnet.turnOff()

                        # Handle the autonomous control menu.
                        elif command_array[4] == "Autonomous":
                            if command_array[5] == "ON":
                                pass
                            elif command_array[6] == "ON":
                                pass
                            elif command_array[7] == "ON":
                                pass

                        # Handle the dance menu.
                        elif command_array[4] == "Dance":
                            if command_array[5] == "ON":
                                pass
                            elif command_array[6] == "ON":
                                pass
            # If it doesn't connect or the connection is dropped, then print error and try again.
            except Exception as e:
                print(e)
                continue
            # If any exception is thrown or when the robot should turn off go to default position.
            finally:
                pass

    @staticmethod
    def DefaultPosition():
        pass
