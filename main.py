import controller.lcd
import controller.led
import controller.pump
import sensor.cam
import sensor.sensor
import sensor.soil_humi
import sensor.temp_humi
import sensor.water_level
import asyncio, websockets
import sensor
import controller

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
    match msg[0]:
        case "s": # 센서
            match msg[1]:
                case "1": # 온습도
                    cmd = send_temp_humi
                case "2": # 토양 습도
                    cmd = send_soil_humi
                case "3": # 수위
                    cmd = send_water_level
                case "4": # 카메라
                    cmd = send_cam

        case "c": # 컨트롤러
            match msg[1]:
                case "c1": # led
                    cmd = controll_led
                case "c2": # lcd
                    cmd = controll_lcd
                case "c3": # pump
                    cmd = controll_pump

        case "s": # 설정
            match msg[1]:
                case "s1": # 미정
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

async def controll_led(detail):
    with controller.led.Led() as c:
        if detail == "True":  
            c.set(light=True)
        elif detail == "False":  
            c.set(light=False)
async def controll_lcd(detail):
    with controller.lcd.LcdDisplay() as c:
        sli = detail.split("|")
        if len(sli) == 1:
            c.set(sli[0])
        elif len(sli) == 2:
            c.set(sli[0], sli[1])
async def controll_pump(detail):
    try:
        with controller.pump.Pump() as c:
            sli = detail.split("|")         
            c.work(int(sli[1]))
            await asyncio.sleep(int(sli[0]))
            c.stop()
    except:
        pass