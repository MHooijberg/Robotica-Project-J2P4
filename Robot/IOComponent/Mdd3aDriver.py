import RPi.GPIO as GPIO  # using RPi.GPIO module
import array
from time import sleep

# The driver for the DC Motors

# TODO: kijk of alle setups en outputs enz nodig zijn want dit is nog testcode.
# TODO: Callibreer code met de linker en rechter outputs.


class Mdd3aDriver:
    pins = array.array(int)

    def __init__(self, m1aPin, m1bPin, m2aPin, m2bPin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pins.insert(0, m1aPin)
        self.pins.insert(1, m1bPin)
        self.pins.insert(2, m2aPin)
        self.pins.insert(3, m2bPin)

        GPIO.setup(self.pins[0], GPIO.OUT)
        GPIO.setup(self.pins[1], GPIO.OUT)
        GPIO.setup(self.pins[2], GPIO.OUT)
        GPIO.setup(self.pins[3], GPIO.OUT)

        self.pwmPin1a = GPIO.PWM(self.pins[0], 20000)
        self.pwmPin1b = GPIO.PWM(self.pins[1], 20000)
        self.pwmPin2a = GPIO.PWM(self.pins[2], 20000)
        self.pwmPin2b = GPIO.PWM(self.pins[3], 20000)

        self.pwmPin1a.start(0)
        self.pwmPin1b.start(0)
        self.pwmPin2a.start(0)
        self.pwmPin2b.start(0)

    def Backward(self, speedLeft, speedRight):
        self.pwmPin1b.start(speedLeft)
        self.pwmPin1a.ChangeDutyCycle(0)
        self.pwmPin2b.start(speedRight)
        self.pwmPin2a.ChangeDutyCycle(0)

    def Brake(self):
        self.pwmPin1a.ChangeDutyCycle(0)
        self.pwmPin1b.ChangeDutyCycle(0)
        self.pwmPin2a.ChangeDutyCycle(0)
        self.pwmPin2b.ChangeDutyCycle(0)

    def Forward(self, speedLeft, speedRight):
        self.pwmPin1a.start(speedLeft)
        self.pwmPin1b.ChangeDutyCycle(0)
        self.pwmPin2a.start(speedRight)
        self.pwmPin2b.ChangeDutyCycle(0)

    # Rotate around the midpoint with both motors, to the right.
    def RotateLeft(self, speed):
        self.pwmPin1a.start(speed)
        self.pwmPin1b.ChangeDutyCycle(0)
        self.pwmPin2b.start(speed)
        self.pwmPin2a.ChangeDutyCycle(0)

    # Rotate around the midpoint with both motors, to the right.

    def RotateRight(self, speed):
        self.pwmPin1b.start(speed)
        self.pwmPin1a.ChangeDutyCycle(0)
        self.pwmPin2a.start(speed)
        self.pwmPin2b.ChangeDutyCycle(0)

    # Only the left wheel spins.
    def TurnLeft(self, speed):
        self.pwmPin1a.start(speed)
        self.pwmPin1b.ChangeDutyCycle(0)
        self.pwmPin2a.ChangeDutyCycle(0)
        self.pwmPin2b.ChangeDutyCycle(0)

    # Only the right wheel spins.
    def TurnRight(self, speed):
        self.pwmPin2a.start(speed)
        self.pwmPin1a.ChangeDutyCycle(0)
        self.pwmPin1b.ChangeDutyCycle(0)
        self.pwmPin2b.ChangeDutyCycle(0)
