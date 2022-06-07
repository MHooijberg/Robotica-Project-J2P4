import asyncio
from bleak import BleakClient

class Remote:
    # TODO: The remote might send fluctuations when moving the joystick,
    #       a solution would be an implementation for an error margin,
    #       in other words the percentage needs to differ an x amount
    #       before it will update to the robot.

    # Definitions:
    #   center (x/y): From this point the center is calculated
    #   inner Deadzone: How far (in percentage) the stick has to be pushed before responding to input.
    #   outer Deadzone: How far (in percentage) can be pushed before it stops repsonding to input.
    def __init__(self, centerX, centerY, range, innerDeadzone, outerDeadzone):
        self.CenterX = centerX
        self.CenterY = centerY
        self.Range = range
        self.InnerDeadzone = innerDeadzone
        self.OuterDeadzone = outerDeadzone

    async def ReceiveData(self):
        async with BleakClient(self.address) as client:
            raw_data = await client.read_gatt_char(self.MODEL_NBR_UUID)
            data_array = format("".join(map(chr, raw_data))).split(",")
            print("Data received over bluetooth: {0}".data_array)
            return data_array

    # Steps: 
    #   1. Het midden moet null zijn.
    #   2. X en Y naar callibreren naar het midden converten.
    #   3. Deadzones bepalen
    #   4. Kijken of de X en Y tussen de Deadzones vallen.
    #   5. Zo ja dan convert naar percentage anders zet terug naar 0% of 100%.

    # TODO: there are different types of deadzones, see if they are fun and usefull to implement?
    #       For example you could do something per quardrant so that you can define the x range seperately from the y.
    def JoystickToPercentage(self, xPos, yPos):
        # TODO: Calibrate code with left and right and negative and positive with the actual hardware.
        percentageFactor = 100 / self.Range

        xPos = xPos - self.CenterX
        yPos = yPos - self.CenterY
        absoluteInnerDeadzone = (int) (self.InnerDeadzone / percentageFactor)
        absoluteOuterDeadzone = (int) (self.OuterDeadzone / percentageFactor)

        # Convert the x value to a percentage.
        if xPos <= absoluteInnerDeadzone and xPos >= -absoluteInnerDeadzone:
            transitionedX = 0
        elif xPos >= absoluteOuterDeadzone:
            transitionedX = 100
        elif xPos >= -absoluteOuterDeadzone:
            transitionedX = -100
        else:
            transitionedX = xPos * percentageFactor

        # Conver the y value to a percentage.
        if yPos <= absoluteInnerDeadzone and yPos >= -absoluteInnerDeadzone:
            transitionedY = 0
        elif yPos >= absoluteOuterDeadzone:
            transitionedY = 100
        elif yPos >= -absoluteOuterDeadzone:
            transitionedY = -100
        else:
            transitionedY = yPos * percentageFactor

        return (transitionedX, transitionedY)

    def SetJoystickDeadzone(self, innerDeadzone, outerDeadzone):
        self.InnerDeadzone = innerDeadzone
        self.OuterDeadzone = outerDeadzone




