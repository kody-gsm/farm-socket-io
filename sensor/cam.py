import cv2
import base64
import spidev

class CamSenSor(object):
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
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            if not self.cam.isOpened():
                raise Exception("can't get camera")
            return self
        except:
            raise Exception("fail why?")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cam.release()
    
    def get_data(self, is_base64=True):
        ret,frame = self.cam.read()
        if not ret:
            return None
        if not is_base64:
            return frame
        _, img_en = cv2.imencode('.jpg', frame)
        
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
