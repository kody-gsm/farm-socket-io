from controller import lcd
from controller import led
from controller import pump
from sensor import cam
from sensor import sensor
from sensor import soil_humi
from sensor import temp_humi
from sensor import water_level
import asyncio, websockets

import typing
SOCKET:websockets.WebSocketClientProtocol

SERVER_URL = "ws://insam-api.dodojini.shop/pot/connect"

async def main():

    # socket 연결
    try:
        async with websockets.connect(SERVER_URL, extra_headers={"pot_code":"sds"}) as socket:
            global SOCKET
            SOCKET = socket
            while True:
                msg = await socket.recv()
                print(msg)
                await msg_switch(msg)
                
    except websockets.ConnectionClosedOK:
        print("socket end")

send_cam_task:typing.Union[asyncio.Task, None] = None
async def msg_switch(msg:str):
    id, msg = msg.split("#", 1)

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
            cmd = controll_led
        elif msg[1] == "2": # lcd
            cmd = controll_lcd
        elif msg[1] == "3": # pump
            cmd = controll_pump

    elif msg[0] == "s": # 설정
        if msg[1] == "1": # 미정
            pass
    
    if cmd:
        detail = None
        if len(msg) > 2:
            detail = msg[2:]
        task = asyncio.create_task(cmd(id, detail))
        if msg == "s4stream":
            global send_cam_task
            send_cam_task = task


async def send_temp_humi(id, details):
    with temp_humi.TempHumiSensor() as s:
        data = s.get_data()
        await SOCKET.send(id+"#"+str(data))

async def send_soil_humi(id, details):
    with soil_humi.SoilHumiSensor() as s:
        data = s.get_data()
        await SOCKET.send(id+"#"+data)

async def send_water_level(id, details):
    with water_level.WaterLevelSenSor() as s:
        data = s.get_data()
        await SOCKET.send(id+"#"+data)

async def send_cam(id, details):
    print(details)
    if details == "stream":
        print('dk')
        if send_cam_task:
            print("tlqkf")
            raise "already stream"
        
        print("asd")
        with cam.CamSenSor() as s:
            while True:
                data = s.get_data()
                await SOCKET.send(id+"#"+data)
                await asyncio.sleep(0.5)
    elif details == "stop":
        if not send_cam_task:
            raise "task is None"
        send_cam_task.cancel()
    else:
        print("dksl")
        with cam.CamSenSor() as s:
            data = s.get_data()
            await SOCKET.send(id+"#"+data)

async def controll_led(detail):
    with led.Led() as c:
        if detail == "True":  
            c.set(light=True)
        elif detail == "False":  
            c.set(light=False)
async def controll_lcd(detail):
    with lcd.LcdDisplay() as c:
        sli = detail.split("|")
        if len(sli) == 1:
            c.set(sli[0])
        elif len(sli) == 2:
            c.set(sli[0], sli[1])
async def controll_pump(detail):
    try:
        with pump.Pump() as c:
            sli = detail.split("|")         
            c.work(int(sli[1]))
            await asyncio.sleep(int(sli[0]))
            c.stop()
    except:
        pass
# async def control_led(detail):
if __name__ == "__main__":
    asyncio.run(main())
