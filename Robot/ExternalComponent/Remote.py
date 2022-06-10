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
        self.PreviousValueX = 0
        self.PreviousValueY = 0
        #self.connected = False
#         self.PreviousValueXLeft = 0
#         self.PreviousValueYLeft = 0
#         self.PreviousValueXRight = 0
#         self.PreviousValueYRight = 0

#     async def ReceiveData(self, client):
#         try:
#             raw_data = await client.read_gatt_char(self.Uuid)
#             data_array = format("".join(map(chr, raw_data))).split(",")
#             print("Data received over bluetooth: ", str(data_array))
#             return data_array
#                 
#         except Exception as error:
#             #self.connected = False
#             print("Couldn't Connect to the XJ-9 Remote.\nHere are the details master:\n", error)
            
#         else:
#             await self.StartConnection()
#             return None
        
                
       
     #   client = BleakClient(self.Address)
     #   try:
        #    await self.client:
          #  raw_data = client.read_gatt_char(self.Uuid)
          #  data_array = format("".join(map(chr, raw_data))).split(",")
           # print("Data received over bluetooth: ", str(data_array))
         #   return data_array
        #except bleak.exc.BleakDBusError:
        
    async def StartConnection(self):
        self.client = BleakClient(self.Address)
        try:
            await client.connect()
        except Exception as e:
            print(e)
            self.connected = False
        else:
            self.connected = True
            print("Connection has been made KING")


    async def ReceiveData(self, client):
        try:               
            raw_data = await client.read_gatt_char(self.Uuid)
            data_array = format("".join(map(chr, raw_data))).split(",")
            print("Data received over bluetooth: ", str(data_array))
            return data_array
                
        except Exception as error:
            print("Couldn't Connect to the XJ-9 Remote.\nHere are the details master:\n", error)
        
        
                
       
     #   client = BleakClient(self.Address)
     #   try:
        #    await self.client:
          #  raw_data = client.read_gatt_char(self.Uuid)
          #  data_array = format("".join(map(chr, raw_data))).split(",")
           # print("Data received over bluetooth: ", str(data_array))
         #   return data_array
                    
           
        #except bleak.exc.BleakDBusError:
        #except Exception as error:
         #   print("Couldn't Connect to the XJ-9 Remote.\nHere are the details master:\n", error)
        
        #finally:
         #   await client.disconnect()

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

        transitionedX = xPos * limitedRangePercentageFactor
        transitionedY = yPos * limitedRangePercentageFactor
        
        # Convert the x value to a percentage.
        if transitionedX <= self.InnerDeadzone and transitionedX >= -self.InnerDeadzone:
            transitionedX = 0
        elif transitionedX >= self.OuterDeadzone:
            transitionedX = 100
        elif transitionedX <= -self.OuterDeadzone:
            transitionedX = -100
        else:
            difference = abs(transitionedX - self.PreviousValueX)
            if difference < 7:
                transitionedX = self.PreviousValueX
        
        if transitionedY <= self.InnerDeadzone and transitionedY >= -self.InnerDeadzone:
            transitionedY = 0
        elif transitionedY >= self.OuterDeadzone:
            transitionedY = 100
        elif transitionedY <= -self.OuterDeadzone:
            transitionedY = -100
        else:
            difference = abs(transitionedY - self.PreviousValueY)
            if difference < 7:
                transitionedY = self.PreviousValueY

        # Conver the y value to a percentage.
#         if yPos <= absoluteInnerDeadzone and yPos >= -absoluteInnerDeadzone:
#             transitionedY = 0
#         elif yPos >= absoluteOuterDeadzone:
#             transitionedY = 100
#         elif yPos <= -absoluteOuterDeadzone:
#             transitionedY = -100
#         else:
#             transitionedY = xPos * limitedRangePercentageFactor
#             difference = abs(transitionedY - self.PreviousValueY)
#             if difference < 7:
#                 transitionedY = self.PreviousValueY

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
        
        self.PreviousValueX = transitionedX
        self.PreviousValueY = transitionedY
        return (transitionedX, transitionedY)

    def SetJoystickDeadzone(self, innerDeadzone, outerDeadzone):
        self.InnerDeadzone = innerDeadzone
        self.OuterDeadzone = outerDeadzone




