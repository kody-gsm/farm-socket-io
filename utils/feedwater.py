from sensor.soil_humi import SoilHumiSensor
from sensor.water_level import WaterLevelSenSor
from controller.pump import Pump
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(timezone='Asia/Seoul')

@sched.scheduled_job(trigger="cron", hour='12',minute='00', id='feed_water')
async def feed_water():
    with SoilHumiSensor() as soil_humi:
        with WaterLevelSenSor() as water_level:
            with Pump() as pump:
                with open("setting.txt", "r") as f:
                    humi = float(f.readline()[5:])
                while True:
                    if soil_humi.get_data() < humi:
                        break
                    if int(water_level.get_data()) < 10:
                        break
                    pump.work(50)
                    await asyncio.sleep(1)
                    pump.stop()
                    await asyncio.sleep(1)

# sched.start()

class feed_water(object):  
    dhtDevice = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.dhtDevice = adafruit_dht.DHT11(board.D18)
        return cls._instance
    
    def __init__(self) -> None:
        self.dhtDevice:adafruit_dht.DHT11
        
    def __enter__(self):
        try:
            return self
        finally:
            pass
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_data(self):
        try:
        # Print the __enter__values to the serial port
            temperature_c = self.dhtDevice.temperature
            humidity = self.dhtDevice.humidity
            return temperature_c, humidity
        except RuntimeError as error:
            raise Exception("err.",error)
        
