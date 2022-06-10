from hx711 import HX711
import time
import sys
import RPi.GPIO as GPIO
# The following is modified code from the 'example' file from https://github.com/tatobari/hx711py
# The 'hx711' file is from the same source and is not modified at all
# Any comments from, with some exeptions, from this file as well as the 'hx711' file have been added by the original creator
# Originally a file for a virtual hx711 was included, but has been deleted, because it has no purpose within this contect
# TODO: Test this code
class WeightSensor:
    
    def __init__(self, pinA, pinB):
        referenceUnit = 1 
        #recommended: "pinA" = 5 and "pinB" = 6
        hx = HX711(pinA, pinB)

        
    def getWeight(self):
        # I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
        # Still need to figure out why does it change.
        # If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
        # There is some code below to debug and log the order of the bits and the bytes.
        # The first parameter is the order in which the bytes are used to build the "long" value.
        # The second paramter is the order of the bits inside each byte.
        # According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
        self.hx.set_reading_format("MSB", "MSB")

        # HOW TO CALCULATE THE REFFERENCE UNIT
        # To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
        # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
        # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
        # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
        #hx.set_reference_unit(113)
        self.hx.set_reference_unit(self.referenceUnit)

        self.hx.reset()

        self.hx.tare()

        print("Tare done! Add weight now....")

        # to use both channels, you'll need to tare them both
        #hx.tare_A()
        #hx.tare_B()
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.

        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string

        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = self.hx.get_weight(5)
        print(val)

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        self.hx.power_down()
        self.hx.power_up()
        return val
#
#      ^             ^
#     / \           / \
#    /   \         /   \
#   /     \       /     \  
#  /    |-->     <--|    \
# /     |           |     \
# \     |           |     /
#  \    |-----------|    /
#   \  /             \  /
#    \/               \/
#    |    /-\   /-\    |
#    |    | |   | |    |
#    |    \-/   \-/    |
#    \                 /
#     \      \_/      /
#      \_____________/
#
