import qr
# from dht import Dht
from real.sensor.soil_humi import SoilHumiSensor
from real.sensor.temp_humi import TempHumiSensor
from real.sensor.water_level import WaterLevelSenSor
# from soil import ReadSoilHumi
import os
import drivers
import time
import subprocess
import asyncio

# sudo python3 Insam.py
async def main():
    display=drivers.Lcd()
    hostname="8.8.8.8"
    ROOMID= 6522
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

    display.lcd_clear()
    display.lcd_display_extended_string("Checking Network",1)
    if response== 1:
        display.lcd_clear()
        display.lcd_display_extended_string("Network is",1)
        display.lcd_display_extended_string("Enabled",2)
        
        with TempHumiSensor() as dht_task, SoilHumiSensor() as soil_task, WaterLevelSenSor() as water_task:
            while True:
                # soil_humi_task = asyncio.create_task(ReadSoilHumi())
                # dht_task = asyncio.create_task(Dht()) #맨 마지막
                try:
                    temp, hum= dht_task.get_data()
                    soil =  soil_task.get_data()
                    water = water_task.get_data()
                    # soil_humi = await soil_humi_task
                    if temp and hum:
                        print('temp:',temp,'humi',hum)
                        display.lcd_clear()
                        # display.lcd_display_extended_string("temp: {}C".format(temp),1)
                        # display.lcd_display_extended_string("hum: {}%".format(hum),2)
                    if soil:
                        print('soil', soil)
                    if water:
                        print('water_leverl', water)
                        display.lcd_clear()
                        display.lcd_display_extended_string("WaterLevel:"+water+'%',1)
                    time.sleep(0.3)
                    # if soil_humi != "ERROR":
                    #     print(soil_humi,"%")
                except Exception as e:
                    display.lcd_clear()
                    print(e)
                    display.lcd_display_extended_string("something",1)
                    display.lcd_display_extended_string("error",2)
                    time.sleep(2.0)
    else:
        qr.ResgistNetwork()

if __name__== '__main__':
    asyncio.run(main())