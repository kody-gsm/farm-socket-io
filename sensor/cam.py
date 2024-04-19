import cv2
import base64

from sensor.sensor import Sensor
import spidev

class CamSenSor(Sensor, object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self.cam:cv2.VideoCapture

    def __enter__(self):
        try:
            if not cv2.waitKey(33) < 0:
                raise Exception("fail waitkey is small")
            self.cam = cv2.VideoCapture(0)
            if not self.cam.isOpened():
                raise Exception("can't get camera")
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            return self
        except:
            return Exception("fail why?")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cam.release()
    
    def get_data(self):
        ret,frame = self.cam.read()
        if not ret:
            return None
        _, img_en = cv2.imencode('.jpg', frame)
        img_64 =base64.b64encode(img_en)
        img_str = img_64.decode('utf-8')
        return img_str
    
with CamSenSor() as cam:
    try:
        data = cam.get_data()
        if data:
            print(len(data))
        else:
            print("cam none")
    except:
        print("error")