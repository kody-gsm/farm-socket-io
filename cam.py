import websockets
import cv2
import base64
import asyncio
import json
from websockets.exceptions import ConnectionClosedError

USER_NAME = 'rpi_1234'

BACKEND_URL = '192.168.1.4:8000'

async def capture(ws):
    if not cv2.waitKey(33) < 0:
        return
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        ret,frame  =cam.read()
        if not ret:
            return
        # cv2.imshow('cam',frame)

        _, img_en = cv2.imencode('.jpg', frame)
        img_64 =base64.b64encode(img_en)
        img_str = img_64.decode('utf-8')
        print(img_str[:20])
        message ={'type':'image','message':img_str}
        await ws.send(json.dumps(message))
    except Exception as e:
        print(e)
    cam.release()

async def main():
    url = f"ws://{BACKEND_URL}/ws/{USER_NAME}"
    print(url)
    try:
        for ii in range(200):
            async with websockets.connect(url, ping_interval=None) as websocket:
                for i in range(1):
                    print(i)
                    try:
                        await asyncio.gather(capture(websocket))
                    except websockets.ConnectionClosed:
                        print('tttterminate')
                await websocket.close()

    except ConnectionClosedError as e:
        print(f"WebSocket connection closed unexpectedly: {e}")

if __name__== '__main__':
    asyncio.run(main())