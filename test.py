SERVER_URL = "ws://192.168.1.15:8000/pot/connect"
import asyncio, websockets

async def sckt():
    async with websockets.connect(SERVER_URL, extra_headers={"pot_code":"asdasddsa"}) as socket:
        print("asd")

asyncio.run(sckt())