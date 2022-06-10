from tkinter import W
import librosa
import IPython.display as ipd
import time
from Types.SteeringMode import SteeringMode
from IOComponent.Mdd3aDriver import Mdd3aDriver


class WheelDriver:
    def __init__(self, m1a, m1b, m2a, m2b):
        self.Wheels = Mdd3aDriver(m1a, m1b, m2a, m2b)

    def Brake(self):
        self.Wheels.Brake()

    def Drive(self, direction, mode):
        # If the direction is 0 brake.
        if direction[0] == 0 and direction[1] == 0:
            self.Wheels.Brake()
        else:
            # Static: Just drive or turn, not both.
            if mode == SteeringMode.static:
                strengthX = abs(direction[0])
                strengthY = abs(direction[1])
                if strengthY >= strengthX:
                    self.Wheels.Move(direction[1], direction[1])
                else:
                    self.Wheels.Rotate(direction[0])

            # Dynamic: Drive, turn and rotatate around center axis at 100%.
            # Smooth: Drive and turn at the same time, but can't rotate.
            elif mode == SteeringMode.smooth or mode == SteeringMode.dynamic:
                naturalHorizontalDirection = abs(direction[0])

                if mode == SteeringMode.dynamic and naturalHorizontalDirection == 100:
                    self.Wheels.Rotate(direction[0])
                else:                    
                    # Secondary wheel = X% of the speed of the primary wheel.
                    secondaryWheelSpeed = (direction[1] / 100) * naturalHorizontalDirection
                    if direction[0] != 0:
                        # Determain if the left or right wheel should be the primary / secondary wheel.
                        leftSpeed = secondaryWheelSpeed if direction[0] < 0 else direction[1]
                        rightSpeed = secondaryWheelSpeed if direction[0] > 0 else direction[1]
                    else:
                        # If no direction is given go forward equal to the power of the Y-direction.
                        leftSpeed, rightSpeed = direction[1]
                    self.Wheels.Move(leftSpeed, rightSpeed)

    def Dance(self):
        x, sr = librosa.load('/dansje.wav')
        ipd.Audio(x, rate=sr)
        tempo, beat = librosa.beat.beat_track(
            x, sr=sr, start_bpm=103, units='time')
        print(len(beat))
        print(beat[1])
        # ADD the motor functions and arm functions
        self.MotorDriver.Forward(0, 0, 0)
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
        self.MotorDriver.Forward(30, 10)
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
        self.ArmDriver.MoveTo(0, 0, 0)
