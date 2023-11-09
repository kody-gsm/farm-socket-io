import cv2

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
detector = cv2.QRCodeDetector()

r = None
while cv2.waitKey(33) < 0:
    ret, frame = capture.read()
    cv2.imshow('',frame)
    if ret:
        retval, points_set, qrcode = detector.detectAndDecode(frame)
        if len(retval)>0:
            print(retval)
            r = retval
            break
        key = cv2.waitKey(100)
        print(key)
        if key == ord('q'):
            break
        if key ==ord('c'):
            cv2.imwrite('test.jpg'. frame)

r = r.split(";") #분리용
wifi_data = {}
r.pop()
for i in r:
    i = i.split(":")
    wifi_data[i[-2]] = i[-1]
print(wifi_data['P'], wifi_data['S'], wifi_data['T'])
capture.release()

cv2.destroyAllWindows()