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
    display.lcd_display_extended_string("WIFI with QR",2)
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
        password = ''+wifi_data['P']
    ssid = ''+wifi_data['S']
    if not 'NONE' in wifi_data['T']:
        key_mgmt = 'key-mgmt='+wifi_data['T'].lower()+'-psk\n'
    
    connection = '[connection]\nid='+ssid+'\nuuid='+str(uuid.uuid4())+"\ntype=wifi\ninterface-name=wlan0\n\n"
    wifi_str='[wifi]\nmode=infrastructure\nssid='+ssid+'\n\n'
    wifi_security='[wifi-security]\nauth-alg=open\n'+key_mgmt+"psk="+password+"\n\n"
    ip_setting='[ipv4]\nmethod=auto\n\n[ipv6]\naddr-gen-mode=default\nmethod=auto\n\n[proxy]'

    Network_Obj = connection+wifi_str+wifi_security+ip_setting
    cv2.destroyAllWindows()
    display.lcd_clear()
    try:
        with open("/etc/NetworkManager/system-connections/"+ssid+".nmconnection", 'r+') as file:
            datas = file.read().split('\n\n')[1]
            print(datas == wifi_str.split('\n\n')[0])
            if datas == wifi_str.split('\n\n')[0]:
                display.lcd_display_string("Existed", 1)
                display.lcd_display_string("Network", 2)
                file.close()
                return
    except:   
        with open("/etc/NetworkManager/system-connections/"+ssid+".nmconnection", 'w+') as file:
            file.writelines([Network_Obj])
            file.close()
            display.lcd_display_string("Succeeded", 1)

            for sec in [3,2,1]:
                display.lcd_display_string(str(sec), 2)
                time.sleep(1)
            os.system("reboot")
            return

ResgistNetwork()