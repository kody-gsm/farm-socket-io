import time
import asyncio
import board
import adafruit_dht
from sensor import Sensor

class TempHumiSensor(Sensor, object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)

        return cls._instance
    
    def __init__(self) -> None:
        self.dhtDevice:adafruit_dht.DHT11

    def setting(self, func):
        self.dhtDevice = adafruit_dht.DHT11(board.D4)

        result = func()

        self.dhtDevice.exit()
        return result

    @setting
    def get_data(self):
        try:
        # Print the values to the serial port
            temperature_c = self.dhtDevice.temperature
            humidity = self.dhtDevice.humidity
            return temperature_c, humidity
        except RuntimeError as error:
            return "err"
        
s1 = TempHumiSensor()
print(s1.get_data())