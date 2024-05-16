import os
import sys
sys.path.append('/home/insam/Documents/Insam_Rasp')
from controller.controller import Controller
import drivers
from typing import Union
import asyncio

class LcdDisplay(Controller, object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.display=drivers.Lcd()

        return cls._instance
    def __init__(self) -> None:
        self.display:drivers.Lcd

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def set(self, string1:str, string2:Union[str, None] = None):
        self.display.lcd_clear()
        self.display.lcd_display_extended_string(string1, 1)
        if string2:
            self.display.lcd_display_extended_string(string2, 2)
    
    async def five_second_clear(self):
        await asyncio.sleep(5)
        self.display.lcd_clear()
        
        
