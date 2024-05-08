# from sensor.cam import CamSenSor

# with CamSenSor() as cam:
#     try:
#         data = cam.get_data()
#         while not data:
#             print("cam none")
#             data = cam.get_data()
#         print(len(data))
#     except Exception as e:
#         print(e)

from sensor.temp_humi import TempHumiSensor

with TempHumiSensor() as s:
    print(s.get_data())