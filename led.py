import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.OUT)

while True:
    GPIO.output(14, 1)
    sleep(1)
    GPIO.output(14, 0)
    sleep(1)
