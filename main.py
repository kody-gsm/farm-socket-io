import os
import subprocess

from controller import led
from controller import pump
from controller import lcd
from sensor import cam
from sensor import sensor
from sensor import soil_humi
from sensor import temp_humi
from sensor import water_level
from utils import r_qr
from utils import get_mac

import asyncio, websockets, drivers

import typing

import RPi.GPIO as GPIO

SOCKET:websockets.WebSocketClientProtocol

SERVER_URL = "ws://insam-api.dodojini.shop/pot/connect"

async def main():
    
    GPIO.setmode(GPIO.BCM)

    display=lcd.LcdDisplay()
    
    hostname="8.8.8.8"
    POT_ID= 'sds'
    response= 0
    
    with open(os.devnull, 'w') as dev:
        try:
            subprocess.check_call(
                ['ping', '-c','1', hostname],
                stdout=dev,
                stderr=dev
            )
            response = 1
        except subprocess.CalledProcessError:
            response = 0

    display.set("Checking Network")
        
    if response== 1:
        display.set("Network is", "Enabled")
        asyncio.create_task(display.five_second_clear())
        
        # socket 연결
        try:
            async with websockets.connect(SERVER_URL, extra_headers={"pot_code":POT_ID}) as socket:
                print('test')
                global SOCKET
                SOCKET = socket
                while True:
                    msg = await socket.recv()
                    print(msg)
                    await msg_switch(msg)
                    
        except Exception as e:
            os.system("reboot")
        
        finally:
            GPIO.cleanup()
    
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
            cmd = controll_led
        elif msg[1] == "2": # lcd
            cmd = controll_lcd
        elif msg[1] == "3": # pump
            cmd = controll_pump

    elif msg[0] == "s": # 설정
        if msg[1] == "1": # 미정
            pass

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
            print(1)
            global send_cam_task
            send_cam_task = task


async def send_temp_humi(id, details):
    s = temp_humi.TempHumiSensor()
    data = s.get_data()
    await SOCKET.send(id+"#s1:"+str(data))

async def send_soil_humi(id, details):
    with soil_humi.SoilHumiSensor() as s:
        data = s.get_data()
        await SOCKET.send(id+"#s2:"+data)

async def send_water_level(id, details):
    with water_level.WaterLevelSenSor() as s:
        data = s.get_data()
        await SOCKET.send(id+"#s3:"+data)

async def send_cam(id, details):
    global send_cam_task
    print(send_cam_task)
    if details == "stream":
        print("asd")
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
        print("dksl")
        with cam.CamSenSor() as s:
            data = s.get_data()
            await SOCKET.send(id+"#s4:"+data)

async def controll_led(id, detail):
    with led.Led() as c:
        if detail == "True":  
            c.set(light=True)
        elif detail == "False":  
            c.set(light=False)
    await SOCKET.send(id+"#c1:set")

async def controll_lcd(id, detail):
    with lcd.LcdDisplay() as c:
        sli = detail.split("|")
        if len(sli) == 1:
            c.set(sli[0])
        elif len(sli) == 2:
            c.set(sli[0], sli[1])
    await SOCKET.send(id+"#c2:set")
    
async def controll_pump(id, detail):
    try:
        with pump.Pump() as c:
            sli = detail.split("|")         
            c.work(int(sli[1]))
            await SOCKET.send(id+"#s4:set start")
            await asyncio.sleep(int(sli[0]))
            c.stop()
            await SOCKET.send(id+"#s4:set end")
    except:
        await SOCKET.send(id+"#c1:fail")

async def test_1(id, details):
    await SOCKET.send(id+"#good")

async def test_2(id, details):
    global send_cam_task
    print(send_cam_task)
    if details == "stream":
        await SOCKET.send(id+"#start")

        while True:
            await SOCKET.send(id+"#test")
            await asyncio.sleep(1)
    elif details == "stop":
        if not send_cam_task:
            raise "task is None"
        send_cam_task.cancel()

        await SOCKET.send(id+"#stop")
    print(send_cam_task)


# async def control_led(detail):
if __name__ == "__main__":
    asyncio.run(main())
