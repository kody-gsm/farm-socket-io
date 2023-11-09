import cv2
from pyzbar.pyzbar import decode

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

r = None
while cv2.waitKey(33) < 0:
    ret, frame = capture.read()
    # cv2.imshow('',frame)
    decoded_data = decode(frame)
    if not len(decoded_data) == 0:
        r = str(decoded_data[0][0])
        break

r = str(r).split("'")[1]
r = r.split(";") 
wifi_data = {}
r.pop();r.pop()
for i in r:
    i = i.split(":")
    wifi_data[i[-2]] = i[-1]

psk = ''
ssid = ''
key_mgmt = ''

if 'P' in wifi_data.keys():
    psk = '\n\tpsk="'+wifi_data['P']+'"'
ssid = '\n\tssid="'+wifi_data['S']+'"'
if not 'NONE' in wifi_data['T']:
    key_mgmt = '\n\tkey_mgmt='+wifi_data['T']+'-PSK'

Network_Obj = '{'+ssid+psk+key_mgmt+'\n}\n\n'
print("network="+Network_Obj)

exists = False

with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'r') as wpa_supplicant:
    datas = wpa_supplicant.read().split('network=')
    datas.pop(0)
    for network in datas:
        if(network == Network_Obj):
            exists = True
  
if not exists:
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'a') as wpa_supplicant:
        wpa_supplicant.writelines(['\nnetwork=',Network_Obj])
        wpa_supplicant.close()
        print('성공적으로 네트워크를 등록했습니다')
else:
    print("이미 존재하는 네트워크 입니다.")

cv2.destroyAllWindows()