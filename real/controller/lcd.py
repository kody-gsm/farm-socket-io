from controller import Controller
import drivers

class LcdDisplay(Controller, object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)

        return cls._instance
    def __init__(self) -> None:
        self.display=drivers.Lcd()

    def __set(self, string1:str, string2:str|None = None):
        self.display.lcd_clear()
        self.display.lcd_display_extended_string(string1, 1)
        if string2:
            self.display.lcd_display_extended_string(string2, 2)

    def network_enable(self):
        self.__set("network is", "enable")
    def temp_humi(self, temp, humi):
        self.__set(f"temp : {temp}", f"humi : {humi}")
    def soil_humi_water_level(self, soil_humi, water_level):
        self.__set(f"soil : {soil_humi}", f"water : {water_level}")
    def rpi_code(self):
        self.__set("rpi code", "code")