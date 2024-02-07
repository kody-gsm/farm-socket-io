import spidev
import time
import math
import drivers
from sensor import Sensor

class WaterLevelSenSor(Sensor, object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)

        return cls._instance
    
    def __init__(self) -> None:
        self.spi:spidev.SpiDev

    def __enter__(self):
        self.spi.open(1,0)
        self.spi.max_speed_hz = 1000000 
        self.spi.mode = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spi.close()

# To read SPI data from MCP3008 chip
# Channel must be 0~7 integer
    def __readChannel(self, channel): 
        val = self.spi.xfer2([1, (8+channel)<<4, 0])
        data = ((val[1]&3) << 8) + val[2]
        return data

    def get_data(self):
        val = self.__readChannel(0)
        if (val != 0) : # filtering for meaningless num
            return val
        else:
            return "err"
        
with WaterLevelSenSorz() as s1:
    print(s1.get_data())