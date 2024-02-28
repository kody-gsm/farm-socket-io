import spidev
import sys
import math
sys.path.append('/home/kody/Documents/insam/real/sensor')
from sensor import Sensor

class WaterLevelSenSor(Sensor, object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.spi = spidev.SpiDev()
        return cls._instance
    
    def __init__(self) -> None:
        self.spi:spidev.SpiDev

    def __convertPercent(self, data):
        return 100.0-round(((data*100)/float(1023)),1)
    
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
            return str(round(math.ceil(self.__convertPercent(val)*100)/100*21)/10)
        else:
            return "err"
        
with WaterLevelSenSor() as s1:
    print(s1.get_data())