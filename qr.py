import cv2
import drivers
import os
import time
import uuid
from pyzbar.pyzbar import decode

def ResgistNetwork():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    display = drivers.Lcd()
    display.lcd_clear()
    display.lcd_display_extended_string("Ready to regist",1)
    display.lcd_display_extended_string("Network with QR",2)
    r = None
    while cv2.waitKey(33) < 0:
        ret, frame = capture.read()
        # cv2.imshow('qr',frame)
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

    password = ''
    ssid = ''
    key_mgmt = ''

    if 'P' in wifi_data.keys():
        password = '\n\t'+wifi_data['P']
    ssid = '\n\t'+wifi_data['S']
    if not 'NONE' in wifi_data['T']:
        key_mgmt = '\n\t'+wifi_data['T'].lower()s+'-psk'
    
    connection = '[connection]\nid='+ssid+'\n'

    Network_Obj = '[connection]\n'+ssid+password+key_mgmt+'\n}\n\n'
    print("network="+Network_Obj)

    exists = False

    with open("/etc/NetworkManager/system-connections/", 'r') as file:
        datas = file.read().split('network=')
        datas.pop(0)
        for network in datas:
            if(network == Network_Obj):
                exists = True
    
    display.lcd_clear()
    if not exists:
        with open("/etc/NetworkManager/system-connections/", 'a') as file:
            file.writelines([Network_Obj])
            file.close()
            print('성공적으로 네트워크를 등록했습니다')

            display.lcd_display_string("Registration", 1)
            display.lcd_display_string("Succeeded", 2)
            for sec in [3,2,1]:
                print("리부트까지 {0}초 남음".format(sec))
                time.sleep(1)
            # os.system("reboot")
    else:
        print("이미 존재하는 네트워크 입니다.")
        display.lcd_display_string("Existed", 1)
        display.lcd_display_string("Network", 2)

    cv2.destroyAllWindows()

ResgistNetwork()