import RPi.GPIO as GPIO
class Magnet:

    def __init__(self, pin):
        # 'pin' = magnetpin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
    
    def turnON(self):
        GPIO.output(self.pin, GPIO.HIGH)
    
    def turnOFF(self):
        GPIO.output(self.pin, GPIO.LOW)
