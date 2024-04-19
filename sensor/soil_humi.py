import sys
sys.path.append('/home/kody/Documents/insam/sensor')

from sensor.sensor import Sensor
import spidev
import math

class SoilHumiSensor(Sensor, object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.spi = spidev.SpiDev()
        return cls._instance
    
    def __init__(self) -> None:
        self.spi:spidev.SpiDev

    def __enter__(self):
        self.spi.open(1,0)
        self.spi.max_speed_hz = 1000000 
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spi.close()

    def __readChannel(self, channel): 
        val = self.spi.xfer2([1, (8+channel)<<4, 0])
        data = ((val[1]&3) << 8) + val[2]
        return data
    
    def __convertPercent(self, data):
        return 100.0-round(((data*100)/float(1023)),1)
    
    def get_data(self):
        val = self.__readChannel(1)
        if val != 0 : # filtering for meaningless num
            return math.ceil(self.__convertPercent(val)*100)/100
        else:
            raise Exception("err")

# with SoilHumiSensor() as s1:s
    