from sensor.soil_humi import SoilHumiSensor
from sensor.water_level import WaterLevelSenSor
from controller.pump import Pump
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(timezone='Asia/Seoul')

@sched.scheduled_job(trigger="corn", hour='12',minute='00', id='feed_water')
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