import RPi.GPIO as GPIO
import time

class Hcsr04:

# ================
# ---- Notes: ----
# ================
#
#
# TODO: Test this code with the HCSR04 distance sensor
#
# --Function--
#
# The goal of this class is to communicate with the HCSR04 distance sensor
# Not only does it receive the data from the sensor, this function also calculates this data in cm
# Please keep in mind that this class only returns the measured data between the censor and the obstacle in centimeters
# It does not return directions for the wheels, this needs to be done outside of this class
#
#
# --How to use--
#
# 1. call the 'findTarget' function, which will almost immeadially call the 'createRadar' function
# 2. the purpose for the 'createRadar' method is to first create a radar, which it uses to check diferences in height on a terrain
#    when the difference is under the average of the radar, this class will classify it as an object
#    this method will return a black image on which a surten number of objects may be located
#    these objects will be represented as thick, red lines
# 3. after calling the 'localizeJunk' method, the findTarget will first check if there are any items at all
#    if there are found items, it will search for the biggest target and draw that target on an emty black image (otherwise 'No items found' will be returned)
#    finally, it will determine if the target is at left, or the right of the middle of the screen (but not before checking if the target is in front of the screen)
#

    # initialisation method, this is used to setup global variables.
    def __init__(self, pinA, pinB):
        GPIO.setmode(GPIO.BCM)
        # recommended pinA = 18
        self.GPIO_TRIGGER = pinA
        # recommended pinB = 24
        self.GPIO_ECHO = pinB
        # set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)


    def GetDistance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
 
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
 
        StartTime = time.time()
        StopTime = time.time()
 
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
 
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
 
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
 
        return distance