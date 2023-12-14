import RPi.GPIO as GPIO
import time
import spidev
GPIO.setmode(GPIO.BCM)
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=50000
def read_spi_adc(adcChannel):
    buff=spi.xfer2([1,(0+ adcChannel)<<4,0])
    adcValue=((buff[1]&3)<<8)+buff[2]
    return adcValue

try:
    while True:
        adcValue=(read_spi_adc(0))
        print(adcValue)
        time.sleep(0.5)
finally:
    GPIO.cleanup()
    spi.close()