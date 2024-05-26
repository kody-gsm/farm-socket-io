from controller.led import Led
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

with Led() as c:
	c.set(light=True)
	time.sleep(5)
