import RPi.GPIO as GPIO


class Magnet:

    def __init__(self, pin):
        self.Pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def Activate(self, active):
        if active:
            GPIO.output(self.Pin, GPIO.HIGH)
        else:
            GPIO.output(self.Pin, GPIO.LOW)
