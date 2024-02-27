import qr
from dht import Dht
# from soil import ReadSoilHumi
import os
import drivers
import time
import asyncio
from real.sensor.temp_humi import TempHumiSensor

# sudo python3 Insam.py
async def main():
    display=drivers.Lcd()
    hostname="8.8.8.8"
    ROOMID= 6522
    response= os.system("ping -c 1 "+hostname)

    display.lcd_clear()
    display.lcd_display_extended_string("Checking Network",1)
    if response== 0:
        display.lcd_clear()
        display.lcd_display_extended_string("Network is",1)
        display.lcd_display_extended_string("Enabled",2)
        temp_humi = TempHumiSensor()
        while True:
            # soil_humi_task = asyncio.create_task(ReadSoilHumi())
            # dht_task = asyncio.create_task(Dht()) #맨 마지막
            try:
                temp, hum=temp_humi
                # soil_humi = await soil_humi_task
                if temp and hum:
                    print(temp,hum)
                    display.lcd_clear()
                    display.lcd_display_extended_string("temp: {}C".format(temp),1)
                    display.lcd_display_extended_string("hum: {}%".format(hum),2)
                    time.sleep(0.3)
                # if soil_humi != "ERROR":
                #     print(soil_humi,"%")
            except:
                time.sleep(2.0)
    else:
        qr.ResgistNetwork()

if __name__== '__main__':
    asyncio.run(main())