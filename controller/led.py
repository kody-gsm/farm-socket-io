from controller import Controller
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.OUT)

class Led(Controller, object):
    PIN_NUMBER = 14
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Led.PIN_NUMBER, GPIO.OUT)
        self.status = False

    def set(self, is_light:bool):
        self.status = is_light
        if is_light:
            GPIO.output(Led.PIN_NUMBER, 1)
        else:
            GPIO.output(Led.PIN_NUMBER, 0)