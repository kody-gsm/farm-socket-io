from pyzbar.pyzbar import decode
import cv2
import os
import sys
sys.path.append('/home/insam/Documents/Insam_Rasp')
from sensor.cam import CamSenSor

def get_qr_info():
    with CamSenSor() as cam:
        # 시간초과 넣어야함
        while True: 
            data = cam.get_data(is_base64=False)
            # if data != None:
            decoded_data = decode(data)
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

    return ('{'+ssid+psk+key_mgmt+'\n}\n\n')

def connect_network():
    Network_Obj = get_qr_info()

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
            os.system("reboot")

    cv2.destroyAllWindows()
    
# connect_network()
