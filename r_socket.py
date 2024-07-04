from controller import lcd
from controller import led
from controller import pump
from sensor import cam
from sensor import sensor
from sensor import soil_humi
from sensor import temp_humi
from sensor import water_level
from utils import r_qr
from utils import get_mac
import asyncio, websockets

import RPi.GPIO as GPIO
import subprocess
import os

import typing
SOCKET:websockets.WebSocketClientProtocol

SERVER_URL = "ws://insam-api.dodojini.shop/pot/connect"

async def main():
    # socket 연결
    GPIO.setmode(GPIO.BCM)

    display = lcd.LcdDisplay()

    hostname = "8.8.8.8"
    POT_ID = get_mac.get_mac()
    response = 0

    with open(os.devnull, 'w') as dev:
        try:
            subprocess.check_call(
                ['ping', '-c', '1', hostname],
                stdout=dev,
                stderr=dev
            )
            response = 1
        except subprocess.CalledProcessError:
            response = 0

    display.set("Checking Network")

    if response == 1:
        display.set("Network is", "Enabled")
        print(POT_ID)
        display.set("Pot ID", POT_ID)
        async with websockets.connect(SERVER_URL, extra_headers={"pot_code":POT_ID}) as socket:
            global SOCKET
            SOCKET = socket
            while True:
                msg = await socket.recv()
                print(msg)
                await msg_switch(msg)
                with water_level.WaterLevelSenSor() as w,soil_humi.SoilHumiSensor() as s:
                    water = float(w.get_data()) / 3.0
                    soil = s.get_data()
                    display.set("water :"+str(water)[:5], "soil : "+str(soil))

    else:
        display.set("Ready to regist", "Network with QR")
        r_qr.connect_network()

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
            cmd = control_led
        elif msg[1] == "2": # lcd
            cmd = control_lcd
        elif msg[1] == "3": # pump
            cmd = control_pump

    elif msg[0] == "v": # 설정
        if msg[1] == "1": # 습도 지정
            cmd = v_set_humi

    elif msg[0] == "t":
        if msg[1] == "1":
            cmd = test_1
        elif msg[1] == "2":
            cmd = test_2
    
    if cmd:
        detail = None
        if len(msg) > 3:
            detail = msg[3:]
        task = asyncio.create_task(cmd(id, detail))

        if msg == "s4:stream" or msg == "t2:stream":
            global send_cam_task
            send_cam_task = task


async def send_temp_humi(id, details):
    with temp_humi.TempHumiSensor() as s:
        data = s.get_data()
        await SOCKET.send(id+"#s1:"+str(data))

async def send_soil_humi(id, details):
    with soil_humi.SoilHumiSensor() as s:
        data = s.get_data()
        await SOCKET.send(id+"#s2:"+str(data))

async def send_water_level(id, details):
    with water_level.WaterLevelSenSor() as s:
        data = s.get_data()
        await SOCKET.send(id+"#s3:"+str(data))

async def send_cam(id, details):
    global send_cam_task
    print(send_cam_task)
    if details == "stream":
        with cam.CamSenSor() as s:
            await SOCKET.send(id+"#s4:stream")
            while True:
                data = s.get_data()
                await SOCKET.send(id+"#s4:"+data)
                await asyncio.sleep(0.5)
    elif details == "stop":
        if not send_cam_task:
            raise "task is None"
        send_cam_task.cancel()
        await SOCKET.send(id+"#s4:stop")
    else:
        with cam.CamSenSor() as s:
            data = s.get_data()
            await SOCKET.send(id+"#s4:"+data)

async def control_led(id, detail):
    with led.Led() as c:
        if detail == "True":  
            c.set(light=True)
        elif detail == "False":  
            c.set(light=False)
    await SOCKET.send(id+"#c1:set")

async def control_lcd(id, detail):
    with lcd.LcdDisplay() as c:
        sli = detail.split("|")
        if len(sli) == 1:
            c.set(sli[0])
        elif len(sli) == 2:
            c.set(sli[0], sli[1])
    await SOCKET.send(id+"#c2:set")
    
async def control_pump(id, detail):
    try:
        with pump.Pump() as c:
            sli = detail.split("|")
            if len(sli) == 2:         
                c.work(int(sli[1]))
            else:         
                c.work()
            await SOCKET.send(id+"#s4:set start")
            await asyncio.sleep(int(sli[0]))
            c.stop()
            await SOCKET.send(id+"#s4:set end")
    except:
        await SOCKET.send(id+"#c1:fail")
        


async def v_set_humi(id, details):
    with open("setting.txt", "w") as f:
        f.write(f"humi={details}")


# async def control_led(detail):
# if __name__ == "__main__":
#     asyncio.run(main())
