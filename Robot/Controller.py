# ==== General Imports: ====
import asyncio
from bleak import BleakClient
import RPi.GPIO as GPIO

# ==== Package Imports ====
from ComputerVision.Tracker import Tracker
from Drivers.ArmDriver import ArmDriver
from Drivers.WheelDriver import WheelDriver
from ExternalComponent.Camera import Camera
from ExternalComponent.Remote import Remote
from ExternalComponent.Screen import Screen
from IOComponent.Hcsr04 import Hcsr04
from IOComponent.Magnet import Magnet
from Types.Action import Action
from Types.ArmPart import ArmPart
from Types.ArmPosition import ArmPosition
from Types.SteeringMode import SteeringMode
from Types.TrackMode import TrackMode

# ================
# ---- Notes: ----
# ================
# TODO: Implement setting to set steering at max value, (turning 1 wheel or rotating around axis)
# TODO: Implement a start and stop animation in the DefaultPosition.
# TODO: Fill up more pins, not all have been configured
# TODO: Discuss if the robot should stop its action when the controller loses connection.
# TODO: Variables on alphabetical order.
#
# Robot life cycle steps:
#   1. Initialize Objects.
#   2. Go to starting position:
#        - Wheels on brake
#        - Arm in folded position
#        - Make sure all components are in their default state.
#        - Initialize GPIO here
#   3. Go into update cycle:
#        - Connect to bluetooth controller
#        - Read instructions from controller.
#        - Execute instruction / command:
#           - Manually:
#               - Drive
#               - Arm
#               - Magnet
#           - Autonomous:
#               - BlueBlock
#               - BlackLine
#               - Shavings
#           - Dance:
#               - LineDance
#               - The other dance :)
#        -
#   4. Shutdown:
#        - Good bye message.
#        - Return to default position.
#        - Return GPIO to their default states.
#        - Clean up serial and GPIO channel.
#        - Shutdown system.


class Controller:
    # =====================================
    # ---------- Settings -----------
    # =====================================
    SHOULD_TURN_OFF = False
    SHOULD_ANIMATE_SHUTDOWN = False
    SHOULD_ANIMATE_START = True

    # =====================================
    # ------ Pin configuration ------
    # =====================================
    AX12_DIRECTION_PIN = 23
    HCSR04_ECHO_PIN = 20
    HCSR04_TRIGGER_PIN = 16
    HX711_DATA_PIN = 5
    HX711_CLOCK_PIN = 5
    M1A_PIN = 12
    M1B_PIN = 18
    M2A_PIN = 19
    M2B_PIN = 13
    MAGNET_PIN = 22
    SHUTDOWN_SWITCH_PIN = 17
    DISPLAY_SERVO_SWITCH_PIN = 24

    # =====================================
    # ---- Remote  configuration ----
    # =====================================
    ADDRESS = "78:E3:6D:12:1B:C6"
    UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
    CENTER_X_LEFT = 1959
    CENTER_Y_LEFT = 1644
    CENTER_X_RIGHT = 1755
    CENTER_Y_RIGHT = 1782
    RANGE = 2047
    INNER_DEADZONE = 7
    OUTER_DEADZONE = 100

    # =====================================
    # ----- Arm / Servo configuration -----
    # =====================================
    #ARM_STRUCTURE = [[69], [70, 71], [72]]
    ARM_STRUCTURE = [[63], [23, 32], [69]]
    CONVERSION_NUMBER = 0.29
    DEFAULT_STABILISATION_AMOUNT = 180
    DIRECTION_RX = GPIO.LOW
    DIRECTION_SWITCH_DELAY = 0.0001
    DIRECTION_TX = GPIO.HIGH
    FOLD_POSITION = [517, [60], 60]
    MAX_POSITION_PER_ROTATION_REQUEST = 4  # 1.16°
    WEIGH_POSITION = [517, [672], 51]
    ZERO_POSITION = 150

    # =====================================
    # ---- Driving configuration ----
    # =====================================
    STEERING_MODE = SteeringMode.Dynamic

    # =====================================
    # ----------- States ------------
    # =====================================
    ARM_START_POSITION = ArmPosition.Folded
    WHEEL_START_ACTION = Action.Stop
    MAGNET_IS_ACTIVE = False

    # =====================================
    # ------ Object  Instances ------
    # =====================================
    ObjectTracker = Tracker()
    Arm = ArmDriver(ARM_STRUCTURE, CONVERSION_NUMBER,
                    DEFAULT_STABILISATION_AMOUNT, ZERO_POSITION,
                    FOLD_POSITION, WEIGH_POSITION, AX12_DIRECTION_PIN,
                    DIRECTION_TX, DIRECTION_RX, DIRECTION_SWITCH_DELAY)
    Camera = Camera()
    Remote = Remote(ADDRESS, UUID, CENTER_X_LEFT, CENTER_Y_LEFT,
                    CENTER_X_RIGHT, CENTER_Y_RIGHT, RANGE, INNER_DEADZONE, OUTER_DEADZONE)
    Screen = Screen()
    Magnet = Magnet(MAGNET_PIN)
    MotorDriver = WheelDriver(M1A_PIN, M1B_PIN, M2A_PIN, M2B_PIN)

    @staticmethod
    async def Update_Loop():
        Controller.Camera.start()
        Controller.DefaultPosition()
        while Controller.SHOULD_TURN_OFF is False:
            # Try to connect with the controller. If it succeeds, perform handle the commands.
            try:
                async with BleakClient(Controller.ADDRESS, timeout=0.5) as client:
                    # Keep reading instructions untill the robot is told to turn off.
                    while Controller.SHOULD_TURN_OFF is False:
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
                                    command_array[0], command_array[1], True)
                                Controller.MotorDriver.Drive(
                                    joystickA, Controller.STEERING_MODE)
                            # Control Arm
                            elif command_array[6] == "ON":
                                joystickA = Controller.Remote.JoystickToPercentage(
                                    command_array[0], command_array[1], True)
                                joystickB = Controller.Remote.JoystickToPercentage(
                                    command_array[2], command_array[3], False)

                                # Man, I'm going to bed, everything is setup.
                                # implement MAX_POSITION_PER_ROTATION_REQUEST
                                # multiplied by the percentage of the axis.
                                # JoystickA X = Base, Y = Arm
                                # JoystickB Y = Head
                                rotationFactor = Controller.MAX_POSITION_PER_ROTATION_REQUEST / 100
                                baseRotation = int(
                                    rotationFactor * joystickA[0])
                                armRotation = int(
                                    rotationFactor * joystickA[1])
                                headRotation = int(
                                    rotationFactor * joystickB[1])
                                Controller.Arm.Rotate(
                                    ArmPart.Base, baseRotation, False)
                                Controller.Arm.Rotate(
                                    ArmPart.Arm, armRotation, False)
                                Controller.Arm.Rotate(
                                    ArmPart.Head, headRotation, False)

                            # Turn on and off the magnet.
                            if command_array[7] == "ON" and Controller.MAGNET_IS_ACTIVE is False:
                                Controller.MAGNET_IS_ACTIVE = True
                                Controller.Magnet.turnON()
                            elif command_array[7] == "OFF" and Controller.MAGNET_IS_ACTIVE is True:
                                Controller.MAGNET_IS_ACTIVE = False
                                Controller.Magnet.turnOff()

                        # Handle the autonomous control menu.
                        elif command_array[4] == "Autonomous":
                            frame = Controller.Camera.read()
                            if command_array[5] == "ON":
                                objectPosition = Controller.ObjectTracker.GetPositionTrackingObject(
                                    frame, TrackMode.BlueBlock)
                            elif command_array[6] == "ON":
                                objectPosition = Controller.ObjectTracker.GetPositionTrackingObject(
                                    frame, TrackMode.BlackLine)
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
                # Controller.Default_Position()

    @staticmethod
    def DefaultPosition():
        Controller.MotorDriver.Brake()
