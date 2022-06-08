import asyncio
from bleak import BleakClient
#from bleak import exc.BleakDBusError

class Remote:
    # TODO: The remote might send fluctuations when moving the joystick,
    #       a solution would be an implementation for an error margin,
    #       in other words the percentage needs to differ an x amount
    #       before it will update to the robot.

    # Definitions:
    #   center (x/y): From this point the center is calculated
    #   inner Deadzone: How far (in percentage) the stick has to be pushed before responding to input.
    #   outer Deadzone: How far (in percentage) can be pushed before it stops repsonding to input.
    def __init__(self, address, uuid, centerXLeft, centerYLeft, centerXRight, centerYRight, range, innerDeadzone, outerDeadzone):
        self.Address = address
        self.Uuid = uuid
        self.CenterXLeft = centerXLeft
        self.CenterYLeft = centerYLeft
        self.CenterXRight = centerXRight
        self.CenterYRight = centerYRight
        self.Range = range
        self.InnerDeadzone = innerDeadzone
        self.OuterDeadzone = outerDeadzone

    async def ReceiveData(self):
        try:
            async with BleakClient(self.Address) as client:
                raw_data = await client.read_gatt_char(self.Uuid)
                data_array = format("".join(map(chr, raw_data))).split(",")
                print("Data received over bluetooth: ", str(data_array))
                return data_array
        #except bleak.exc.BleakDBusError:
        except Exception as error:
            print("Couldn't Connect to the XJ-9 Remote.\nHere are the details master:\n", error)
                

    # Steps: 
    #   1. Het midden moet null zijn.
    #   2. X en Y naar callibreren naar het midden converten.
    #   3. Deadzones bepalen
    #   4. Kijken of de X en Y tussen de Deadzones vallen.
    #   5. Zo ja dan convert naar percentage anders zet terug naar 0% of 100%.

    # TODO: there are different types of deadzones, see if they are fun and usefull to implement?
    #       For example you could do something per quardrant so that you can define the x range seperately from the y.
    def JoystickToPercentage(self, xPosRaw, yPosRaw, isLeftJoystick):
        # TODO: Calibrate code with left and right and negative and positive with the actual hardware.
        #Percentage factor with full range.
        fullRangePercentageFactor = 100 / self.Range
        
        if isLeftJoystick == True:
            xPos = int(xPosRaw) - self.CenterXLeft
            yPos = int(yPosRaw) - self.CenterYLeft
        else:
            xPos = int(xPosRaw) - self.CenterXRight
            yPos = int(yPosRaw) - self.CenterYRight
        
        absoluteInnerDeadzone = (int) (self.InnerDeadzone / fullRangePercentageFactor)
        absoluteOuterDeadzone = (int) (self.OuterDeadzone / fullRangePercentageFactor)
        # Percentage factor including the range bounds (deadzones)
        limitedRangePercentageFactor = 100 / (absoluteOuterDeadzone - absoluteInnerDeadzone)
        

        # Convert the x value to a percentage.
        if xPos <= absoluteInnerDeadzone and xPos >= -absoluteInnerDeadzone:
            transitionedX = 0
        elif xPos >= absoluteOuterDeadzone:
            transitionedX = 100
        elif xPos <= -absoluteOuterDeadzone:
            transitionedX = -100
        else:
            transitionedX = xPos * limitedRangePercentageFactor

        # Conver the y value to a percentage.
        if yPos <= absoluteInnerDeadzone and yPos >= -absoluteInnerDeadzone:
            transitionedY = 0
        elif yPos >= absoluteOuterDeadzone:
            transitionedY = 100
        elif yPos <= -absoluteOuterDeadzone:
            transitionedY = -100
        else:
            transitionedY = xPos * limitedRangePercentageFactor

        print("\n==== Debug JoystickConversion ====",
              "\nX Position: ", xPosRaw,
              "\nY Position: ", yPosRaw,
              "\nRange: ", self.Range,
              "\nfullRangePercentageFactor: ", fullRangePercentageFactor,
              "\nCentered X Position: ", xPos,
              "\nCentered Y Position: ", yPos,
              "\nabsoluteInnerDeadzone: ", absoluteInnerDeadzone,
              "\nabsoluteOuterDeadzone: ", absoluteOuterDeadzone,
              "\nRemaining Range: ",(absoluteOuterDeadzone - absoluteInnerDeadzone),
              "\nlimitedRangePercentageFactor: ", limitedRangePercentageFactor,
              "\ntansitionedX: ", transitionedX,
              "\ntransitionedY: ", transitionedY,
              "\n=== End of Debug Information ===="
              )

        print("Joystick output: x=",transitionedX,"% y=",transitionedY,"%", sep='')
        return (transitionedX, transitionedY)

    def SetJoystickDeadzone(self, innerDeadzone, outerDeadzone):
        self.InnerDeadzone = innerDeadzone
        self.OuterDeadzone = outerDeadzone




