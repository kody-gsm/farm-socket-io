# from sensor.cam import CamSenSor

# with CamSenSor() as cam:
#     try:
#         data = cam.get_data()
#         while not data:
#             print("cam none")
#             data = cam.get_data()
#         print(len(data))
#     except Exception as e:
#         print(e)

# from sensor.temp_humi import TempHumiSensor

# with TempHumiSensor() as s:
#     print(s.get_data())

import RPi.GPIO as GPIO
from controller import led
from controller import pump
import time

with led.Led() as l:
	l.set(True)
	time.sleep(2.0)

with pump.Pump() as P:
	print('gkgk')

time.sleep(2.0)

with led.Led() as l:
	l.set(True)
	time.sleep(2.0)

with led.Led() as l:
	l.set(False)
	time.sleep(2.0)
	
GPIO.cleanup()
