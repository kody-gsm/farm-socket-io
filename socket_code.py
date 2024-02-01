import json
import asyncio
import websockets
import sys
from websockets.exceptions import ConnectionClosedError
import asyncio
import time

USER_NAME = '1234'

BACKEND_URL = '192.168.1.5:8000'

async def handle_input():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, " ")

async def ws_send(ws):
        message = {'message' : "Hello, WebSocket"}
        await ws.send(json.dumps(message))
        await asyncio.sleep(0.2)
        while True: 
            text = await handle_input()
            if text:
                message = {'message' : text}
                text = False
                await ws.send(json.dumps(message))
                await asyncio.sleep(0.2)


async def ws_recv(ws):
    while True:
        response_text_data = await ws.recv()
        print(response_text_data)
        if response_text_data != False:
            response = json.loads(response_text_data)
            print(response)
            response_text_data = False


async def main():
    url = f"ws://{BACKEND_URL}/ws/{USER_NAME}"
    print(url)
    try:
        async with websockets.connect(url, ping_interval=60) as websocket:
            await asyncio.gather(ws_recv(websocket), ws_send(websocket))

    except ConnectionClosedError as e:
        print(f"WebSocket connection closed unexpectedly: {e}")


asyncio.run(main())