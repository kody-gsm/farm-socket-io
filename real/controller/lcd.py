from controller import Controller
import drivers

class LcdDisplay(Controller, object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)

        return cls._instance
    def __init__(self) -> None:
        self.display=drivers.Lcd()

    def set(self, string1:str, string2:str|None = None):
        self.display.lcd_clear()
        self.display.lcd_display_extended_string(string1, 1)
        if string2:
            self.display.lcd_display_extended_string(string2, 2)
