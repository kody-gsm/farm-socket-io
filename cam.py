import websockets
import cv2
import base64
import asyncio

server = ''
port = ''


async def capture():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while cv2.waitKey(33) < 0:
        ret,frame  =cam.read()
        if not ret:
            break
        cv2.imshow('cam',frame)

        _, img_en = cv2.imencode('.jpg', frame)
        img_64 =base64.b64decode(img_en)
        # img_str = img_64.decode('utf-8')

        # await websockets.send(img_str)
    cam.release()


if __name__== '__main__':
    asyncio.run(capture())