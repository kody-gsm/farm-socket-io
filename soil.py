import spidev
import time
import math

delay = 1 

# Open Spi Bus
# SPI 버스 0과 디바이스 0을 열고
# 최대 전송 속도를 1MHz로 설정
spi = spidev.SpiDev()
spi.open(0,0) # open(bus, device)
spi.max_speed_hz = 1000000 # set transfer speed

# To read SPI data from MCP3008 chip
# Channel must be 0~7 integer

# 0~1023 value가 들어옴. 1023이 수분함량 min값

async def ReadSoilHumi():
  try:
    channel = 0
    val = spi.xfer2([1, (8+channel)<<4, 0])
    val = ((val[1]&3) << 8) + val[2]
    val = 100.0-round(((val*100)/float(1023)),1)
    if (val != 0) : # filtering for meaningless num
      return math.ceil(val*100)/10
  except RuntimeError as error:
    return error

if __name__== '__main__':
  try:
    while True:
      print(ReadSoilHumi())
      time.sleep(delay)
  except KeyboardInterrupt:
    spi.close()
    print("Keyboard Interrupt!!!!")
