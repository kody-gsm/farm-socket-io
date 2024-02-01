from sensor import Senser
import spidev

class SoilHumiSensor(Senser, object):


    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)

            cls._instance.spi = spidev.SpiDev()
            cls._instance.spi.open(1,0) # open(bus, device)
            cls._instance.spi.max_speed_hz = 1000000

        return cls._instance
    
    def __init__(self) -> None:
        self.spi:spidev.SpiDev

    def readChannel(self, channel): 
        val = self.spi.xfer2([1, (8+channel)<<4, 0])
        data = ((val[1]&3) << 8) + val[2]
        return data

    def get_data(self):
        val = self.readChannel(1)
        if (val != 0) : # filtering for meaningless num
            return val
        else:
            return "err"


    
    
s1 = SoilHumiSensor()
s2 = SoilHumiSensor()
print(s1.get_data())
    