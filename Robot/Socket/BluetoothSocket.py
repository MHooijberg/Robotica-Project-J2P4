import asyncio
from bleak import BleakClient

address = "78:E3:6D:12:1B:C6"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
    
class RemoteSocket:
    
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

    async def main(address):
        async with BleakClient(address) as client:
            model_number = await client.read_gatt_char(MODEL_NBR_UUID)
            print("Model Number: {0}".format("".join(map(chr, model_number))))
            return model_number

    asyncio.run(main(address))
    
    def __init__(self):
        pass