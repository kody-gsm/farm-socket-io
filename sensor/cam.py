import cv2
from picamera2 import Picamera2
import base64

from sensor.sensor import Sensor

class CamSenSor(Sensor, object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self.cam:cv2.VideoCapture

    def __enter__(self):
        picam2 = Picamera2()
        picam2.preview_configuration.main.size = (640,480)
        picam2.preview_configuration.main.format = "RGB888"
        picam2.preview_configuration.align()
        picam2.configure("preview")
        picam2.start()


    def __exit__(self, exc_type, exc_val, exc_tb):
        cv2.destroyAllWindows()
    
    def get_data(self, is_base64=True):
        im= picam2.capture_array()
        if not is_base64:
            return im
        _, img_en = cv2.imencode('.jpg', im)
        
        img_64 =base64.b64encode(img_en)
        img_str = img_64.decode('utf-8')
        return img_str
    
# with CamSenSor() as cam:
#     try:
#         data = cam.get_data()
#         if data:
#             print(len(data))
#         else:
#             print("cam none")
#     except:
#         print("error")
