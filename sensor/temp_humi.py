import board
import adafruit_dht

class TempHumiSensor(object):  
    dhtDevice = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.dhtDevice = adafruit_dht.DHT11(board.D18)
        return cls._instance
    
    def __init__(self) -> None:
        self.dhtDevice:adafruit_dht.DHT11

    def get_data(self):
        try:
        # Print the __enter__values to the serial port
            temperature_c = self.dhtDevice.temperature
            humidity = self.dhtDevice.humidity
            return temperature_c, humidity
        except RuntimeError as error:
            print(error)
            return Exception("err.",error)
        

# import time
# while True:
#     ths = TempHumiSensor()
#     print(ths.get_data())
#     time.sleep(0.2)
