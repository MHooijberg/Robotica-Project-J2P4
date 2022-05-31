import RPi.GPIO as GPIO
class Magnet:

    def __init__(self):
        Mag_Pin = 20
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Mag_Pin, GPIO.OUT)
    
    def turnON(self):
        GPIO.output(self.Mag_Pin, GPIO.HIGH)
    
    def turnOFF(self):
        GPIO.output(self.Mag_Pin, GPIO.LOW)
