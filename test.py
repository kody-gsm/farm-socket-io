data = "WIFI:T:WPA;S:micro_2_5G;P:#gsm_micro@;H:false;"
# data = 'WIFI:T:NONE;S:Ganggggg;P:H:true;'
r = data.split(";")
wifi_data = {}
r.pop()
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

Network_Obj = '{'+ssid+psk+key_mgmt+'\n}\n'
print(Network_Obj)

exists = False

with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'r') as wpa_supplicant:
    datas = wpa_supplicant.read().split('network=')
    datas.pop(0)
    for network in datas:
        if(network == Network_Obj):
            exists = True

if not exists:
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'a') as wpa_supplicant:
        datas = wpa_supplicant.writable()
        print(datas)
else:
    print("이미 존재하는 네트워크 입니다.")