import RPi.GPIO as GPIO

class Led(object):
    PIN_NUMBER = 14
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.status = False
        return cls._instance
    
    def __init__(self) -> None:
        self.status:bool

    def __enter__(self):
        GPIO.setup(Led.PIN_NUMBER, GPIO.OUT)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #GPIO.setup(Led.PIN_NUMBER, GPIO.IN)
        pass

    def set(self, light:bool):
        self.status = light
        if light:
            GPIO.output(Led.PIN_NUMBER, 1)
        else:
            GPIO.output(Led.PIN_NUMBER, 0)


import time
GPIO.setmode(GPIO.BCM)
with Led() as led:
    while True:
        led.set(True)
        time.sleep(1)
