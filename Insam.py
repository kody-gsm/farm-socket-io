import qr
from dht import Dht
import os
import drivers
import time
import asyncio

# sudo python3 Insam.py
async def main():
    display=drivers.Lcd()
    hostname="8.8.8.8"
    response= os.system("ping -c 1 "+hostname)

    display.lcd_clear()
    display.lcd_display_extended_string("Checking Network",1)
    if response== 0:
        display.lcd_clear()
        display.lcd_display_extended_string("Network is",1)
        display.lcd_display_extended_string("Enabled",2)
        while True:
            dht_task = asyncio.create_task(Dht()) #맨 마지막
            dht_task = asyncio.create_task(Dht())
            temp, hum=await dht_task
            if temp and hum:
                print(temp,hum)
                display.lcd_clear()
                display.lcd_display_extended_string("temp: {}C".format(temp),1)
                display.lcd_display_extended_string("hum: {}%".format(hum),2)
                time.sleep(0.5)
            else:
                time.sleep(2.0)
    else:
        qr.ResgistNetwork()

if __name__== '__main__':
    asyncio.run(main())