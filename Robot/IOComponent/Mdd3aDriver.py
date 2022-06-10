import RPi.GPIO as GPIO  # using RPi.GPIO module
import array
from time import sleep


class Mdd3aDriver:
    pins = []

    def __init__(self, m1aPin, m1bPin, m2aPin, m2bPin):
        # TODO: Can we setup the GPIO in Controller.py?
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pins.insert(0, m1aPin)
        self.pins.insert(1, m1bPin)
        self.pins.insert(2, m2aPin)
        self.pins.insert(3, m2bPin)

        for x in self.pins:
            GPIO.setup(x, GPIO.OUT)
            self.pwmPins.insert(0, GPIO.PWM(x, 20000))

        for x in range(4):
            self.pwmPins[x].start(0)

    def Move(self, speedLeft, speedRight):
        if speedLeft > 0:
            self.pwmPins[0].ChangeDutyCycle(speedLeft)
            self.pwmPins[1].ChangeDutyCycle(0)
        elif speedLeft < 0:
            self.pwmPins[1].ChangeDutyCycle(abs(speedLeft))
            self.pwmPins[0].ChangeDutyCycle(0)
        if speedRight > 0:
            self.pwmPins[2].ChangeDutyCycle(speedRight)
            self.pwmPins[3].ChangeDutyCycle(0)
        elif speedRight < 0:
            self.pwmPins[3].ChangeDutyCycle(abs(speedRight))
            self.pwmPins[2].ChangeDutyCycle(0)

    def Rotate(self, speed):
        if speed > 0:
            self.pwmPins[0].ChangeDutyCycle(speed)
            self.pwmPins[1].ChangeDutyCycle(0)
            self.pwmPins[2].ChangeDutyCycle(0)
            self.pwmPins[3].ChangeDutyCycle(speed)
        elif speed < 0:
            self.pwmPins[0].ChangeDutyCycle(0)
            self.pwmPins[1].ChangeDutyCycle(speed)
            self.pwmPins[2].ChangeDutyCycle(speed)
            self.pwmPins[3].ChangeDutyCycle(0)

    def Brake(self):
        for x in self.pwmPins:
            x.ChangeDutyCycle(0)
