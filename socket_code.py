import json
import asyncio
import websockets
import sys
from websockets.exceptions import ConnectionClosedError

USER_NAME = '김철중'

async def connect_to_websocket():
    url = f"wss://port-0-websocket-1igmo82cloo8459k.sel5.cloudtype.app/ws/chat/dksl/{USER_NAME}/"
    print(url)
    try:
        async with websockets.connect(url) as websocket:
            message = {'message' : "Hello, WebSocket"}
            await websocket.send(json.dumps(message))
            text = False
            while True:
                if text:
                    text = text.split('\n')[0]
                    message = {'message' : text}
                    text = False
                    await websocket.send(json.dumps(message))
                response_text_data = await websocket.recv()
                response = json.loads(response_text_data)
                print(response)

                

    except ConnectionClosedError as e:
        print(f"WebSocket connection closed unexpectedly: {e}")

asyncio.run(connect_to_websocket())