import asyncio
from time import sleep
from msilib.schema import Control
#import for dance
import librosa 
import IPython.display as ipd 
import time
# TODO: Fix import issues
import ComputerVision.Tracker
import Drivers.ArmDriver
#from .ExternalComponent import Camera
import ExternalComponent.Remote
import ExternalComponent.Screen
import IOComponent.Hcsr04
import IOComponent.Magnet
import IOComponent.Mdd3aDriver
#from .Socket import BluetoothSocket
# TODO: Don't import all form a folder, this is bad practice.
# import Types import *
import Types.SteeringMode
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

# TODO: I'd like to mention that self and Contoller.variable are used interchangebly.
#       We need to do research on if this might be a bad practise.


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
    CENTER_X = 2047
    CENTER_Y = 2047
    RANGE = 2047
    INNER_DEADZONE = 9.75
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
    # TODO: Implement setting to set steering at max value, (turning 1 wheel or rotating around axis)
    # TODO: Implement a setting to set from when it needs to turn in the special way.
    # TODO: Implement safety for max speed?
    STEERING_MODE = SteeringMode.static

    # TODO: Make all IOComponents configureable with pins
    # TODO: sort by the order of imports :) i like neat code.
    ObjectTracker = Tracker()
    Arm = ArmDriver()
    Remote = Remote(CENTER_X, CENTER_Y, RANGE, INNER_DEADZONE, OUTER_DEADZONE)
    Screen = Screen()
    #Magnet = Magnet(MAGNET_PIN)
    MotorDriver = Mdd3aDriver(M1A_PIN, M1B_PIN, M2A_PIN, M2B_PIN)

    def __init__(self):
        pass

    # Update Loop Cycle:
    #   1. Retrieve Settings from remote.
    #   2. Change State based on the remote settings.
    #   3. Start / Keep doing action if State Changed.
    #   4. Repeat.
    # TODO: Discuss with group about being able to controll the arm while driving.

    # TODO: States should be included, a state for each action like current magnet action etc.
    #      Will save some resources because only when a state is changed something will happen.
    @staticmethod
    def Update_Loop():
        while Controller.ShouldTurnnOff is False:
            command_array = asyncio.run(Controller.Bluetooth.ReceiveData())

            match command_array[4]:
                case "Drive":
                    if (command_array[5] == "ON"):
                        joystickA = Controller.Remote.JoystickToPercentage(
                            command_array[0], command_array[2])
                        print("Joystick output: x=" +
                              str(joystickA[0]) + " y=" + str(joystickA[1]))
                        # TODO: Joystick B Is not needed at the moment.
                        #joystickB = Controller.Remote.JoystickToPercentage(command_array[1], command_array[3])
                        Controller.Drive(joystickA)
                    elif (command_array[6] == "ON"):
                        pass
                case "Robot Arm":
                    if (command_array[5] == "ON"):
                        Controller.Magnet.turnON()
                    else:
                        Controller.Magnet.turnOff()
                    # TODO: command_array[6] is used for the gripper which we do not have.
                case "Dance":
                    pass

    # TODO: Find a better position for this code.
    # TODO: I need to test the output of the controller to see if x can be 100 without y being 100
    def Drive(self, direction):
        match Controller.STEERING_MODE:
            case SteeringMode.static:
                if direction[0] > 0 or direction[1] > 0:
                    strengthX = abs(direction[0])
                    strengthY = abs(direction[1])
                    if strengthY > strengthX:
                        if direction[1] > 0:
                            self.MotorDriver.Forward(strengthY, strengthY)
                        else:
                            self.MotorDriver.Backward(strengthY, strengthY)
                    else:
                        if direction[0] > 0:
                            self.MotorDriver.Forward(strengthX, strengthX)
                        else:
                            self.MotorDriver.Backward(strengthX, strengthX)

            case SteeringMode.dynamic:
                pass
            case SteeringMode.smooth:
                pass

    def Dance(self):
        x, sr = librosa.load('/dansje.wav') 
        ipd.Audio(x, rate=sr)
        tempo, beat = librosa.beat.beat_track(x, sr=sr, start_bpm=103, units='time')
        print(len(beat))
        print(beat[1])
        #ADD the motor functions and arm functions
        self.MotorDriver.Forward(0,0,0)
        time.sleep(beat[3])
        self.MotorDriver.RotateLeft(50)
        self.ArmDriver.MoveTo(0, 0, 0)
        self.ArmDriver.MoveTo(0, 20, 20)
        time.sleep(beat[15]-beat[3])
        self.MotorDriver.Forward(30, 10)
        time.sleep(beat[30]-beat[15])
        self.MotorDriver.RotateRight(50)
        time.sleep(beat[45]-beat[30])
        self.MotorDriver.Forward(30, 10)
        time.sleep(beat[60]-beat[45])
        self.MotorDriver.RotateRight(50)
        time.sleep(beat[75]-beat[60])
        self.MotorDriver.Forward(30, 10)
        time.sleep(beat[90]-beat[75])
        self.MotorDriver.RotateRight(50)
        time.sleep(beat[105]-beat[90])
        self.MotorDriver.Forward(30,10)
        time.sleep(beat[120]-beat[105])
        self.MotorDriver.RotateRight(50) 
        time.sleep(beat[135]-beat[120])
        self.MotorDriver.Forward(30, 10)
        time.sleep(beat[150]-beat[135])
        self.MotorDriver.RotateRight(50)
        time.sleep(beat[165]-beat[150])
        self.MotorDriver.Forward(30, 10)
        time.sleep(beat[180]-beat[165])
        self.MotorDriver.RotateRight(50)
        time.sleep(beat[195]-beat[180])
        self.MotorDriver.Backward(20, 20)
        time.sleep(beat[203]-beat[190])
        self.MotorDriver.Brake()
        self.ArmDriver.MoveTo(0,0,0)


    
        
