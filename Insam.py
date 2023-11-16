import qr
import os
import drivers

# sudo python3 Insam.py
display=drivers.Lcd()
hostname="8.8.8.8"
response= os.system("ping -c 1 "+hostname)

display.lcd_clear()
display.lcd_display_extended_string("Checking Network",1)
if __name__== '__main__':
    if response== 0:
        display.lcd_clear()
        display.lcd_display_extended_string("Network is",1)
        display.lcd_display_extended_string("Enabled",2)
    else:
        qr.ResgistNetwork()