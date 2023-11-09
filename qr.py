import cv2
from pyzbar.pyzbar import decode

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
detector = cv2.QRCodeDetector()

r = None
while cv2.waitKey(33) < 0:
    ret, frame = capture.read()
    cv2.imshow('',frame)
    decoded_data = decode(frame)
    if not len(decoded_data) == 0:
        r = str(decoded_data[0][0])
        break

r = r.split(";") #분리용
wifi_data = {}
r.pop()
for i in r:
    i = i.split(":")
    wifi_data[i[-2]] = i[-1]
print(wifi_data['P'], wifi_data['S'], wifi_data['T'])
capture.release()

cv2.destroyAllWindows()