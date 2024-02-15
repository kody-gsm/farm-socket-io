from controller import Controller

class Pump(Controller,object):
    STOP  = 0
    FORWARD  = 1
    BACKWORD = 2

    # 모터 채널
    CH1 = 0
    CH2 = 1

    # PIN 입출력 설정
    OUTPUT = 1
    INPUT = 0

    # PIN 설정
    HIGH = 1
    LOW = 0

    # 실제 핀 정의
    #PWM PIN
    ENA = 25  #37 pin

    #GPIO PIN
    IN1 = 23  #37 pin
    IN2 = 24  #35 pin
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __enter__(self):
        STOP  = 0
FORWARD  = 1
BACKWORD = 2

# 모터 채널
CH1 = 0
CH2 = 1

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

# 실제 핀 정의
#PWM PIN
ENA = 25  #37 pin

#GPIO PIN
IN1 = 23  #37 pin
IN2 = 24  #35 pin