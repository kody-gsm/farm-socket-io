import websockets

BACKEND_URL = '192.168.1.5:8000'

class WebsocketConnect():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.ws = 
        return cls._instance
    
    def __init__(self) -> None:
        self.ws:adafruit_dht.DHT11