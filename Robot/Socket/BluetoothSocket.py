import asyncio
from bleak import BleakClient
    
class RemoteSocket:
    address = "78:E3:6D:12:1B:C6"
    MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

    def __init__(self):
        pass
    
    async def ReceiveData(self):
        async with BleakClient(self.address) as client:
            raw_data = await client.read_gatt_char(self.MODEL_NBR_UUID)
            data_array = format("".join(map(chr, raw_data))).split(",")
            print("Data received over bluetooth: {0}".data_array)
            return data_array
    
    # TODO: Bespreken of dit niet beter een RemoteController Class kan zijn omdat het eigenlijk de
    #       verbinding is met de afstandsbediening, dan kunnen we hier de data conversie ook in zetten.
    #       of anders een math class om speciale functies op zich te nemen.

    # QUICK SCAN FOR DEVICES
    #
    # import asyncio
    # from bleak import BleakScanner
    # 
    # async def main():
    #     devices = await BleakScanner.discover()
    #     for d in devices:
    #         print(d)
    # 
    # asyncio.run(main())
