import sensor.cam
import sensor.sensor
import sensor.soil_humi
import sensor.temp_humi
import sensor.water_level
import asyncio, websockets
import sensor

SOCKET:websockets.WebSocketClientProtocol

async def main():
    

    # socket 연결
    SERVER_URL = "ws://localhost:8001"
    try:
        async with websockets.connect(SERVER_URL) as socket:
            global SOCKET
            SOCKET = socket
            while True:
                msg = await socket.recv()
                
                await msg_switch(msg)
                
    except websockets.ConnectionClosedOK:
        print("socket end")

send_cam_task:asyncio.Task|None = None
async def msg_switch(msg):
    # msg 분류
    cmd = None
    if msg[0] == "s":
        if msg[1] == "1": # 온습도
            cmd = send_temp_humi
        elif msg[1] == "2": # 토양 습도
            cmd = send_soil_humi
        elif msg[1] == "3": # 수위
            cmd = send_water_level
        elif msg[1] == "4": # 카메라
            cmd = send_cam

    elif msg[0] == "c": # 컨트롤러
        if msg[1] == "1": # led
            pass
        elif msg[1] == "2": # lcd
            pass
        elif msg[1] == "3": # pump
            pass

    elif msg[0] == "s": # 설정
        if msg[1] == "1": # 미정
            pass
    
    if cmd:
        detail = None
        if len(msg) > 2:
            detail = msg[2:]
        task = asyncio.create_task(cmd(detail))
        if msg == "s4stream":
            global send_cam_task
            send_cam_task = task


async def send_temp_humi(details):
    with sensor.temp_humi.TempHumiSensor() as s:
        data = s.get_data()
        await SOCKET.send(data)

async def send_soil_humi(details):
    with sensor.soil_humi.SoilHumiSensor() as s:
        data = s.get_data()
        await SOCKET.send(data)

async def send_water_level(details):
    with sensor.water_level.WaterLevelSenSor() as s:
        data = s.get_data()
        await SOCKET.send(data)

async def send_cam(details):
    if details == "stream":
        if send_cam_task:
            raise "already stream"
        with sensor.cam.CamSenSor() as s:
            while True:
                data = s.get_data()
                await SOCKET.send(data)
                await asyncio.sleep(0.5)
    elif details == "stop":
        if not send_cam_task:
            raise "task is None"
        send_cam_task.cancel()
    else:
        with sensor.cam.CamSenSor() as s:
            data = s.get_data()
            await SOCKET.send(data)

# async def control_led(detail):
