from controller import Controller
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.OUT)

class Led(Controller, object):
    PIN_NUMBER = 14
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.status = False
        return cls._instance
    
    def __init__(self) -> None:
        self.status:bool

    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Led.PIN_NUMBER, GPIO.OUT)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def set(self, light:bool):
        self.status = light
        if light:
            GPIO.output(Led.PIN_NUMBER, 1)
        else:
            GPIO.output(Led.PIN_NUMBER, 0)