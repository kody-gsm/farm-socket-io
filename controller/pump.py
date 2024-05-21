# from controller.controller import Controller
import RPi.GPIO as GPIO

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

class Pump(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.pwm:GPIO.PWM
    
    def __enter__(self):
        GPIO.setup(ENA, GPIO.OUT)
        GPIO.setup(IN1, GPIO.OUT)   
        GPIO.setup(IN2, GPIO.OUT)
        # 100khz 로 PWM 동작 시킴 
        self.pwm = GPIO.PWM(ENA, 100) 
        # 우선 PWM 멈춤.   
        self.pwm.start(0) 

        sleep(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        GPIO.setup(ENA, GPIO.IN)
        GPIO.setup(IN1, GPIO.IN)   
        GPIO.setup(IN2, GPIO.IN)

            
    def stop(self, speed = 80):
        self.pwm.ChangeDutyCycle(speed)
        GPIO.output(IN1, LOW)
        GPIO.output(IN2, LOW)

    def work(self, speed = 30, is_backword = False):
        self.pwm.ChangeDutyCycle(speed) 
        if is_backword:
            GPIO.output(IN1, LOW)
            GPIO.output(IN2, HIGH)
        else:
            GPIO.output(IN1, HIGH)
            GPIO.output(IN2, LOW)


from time import sleep
GPIO.setmode(GPIO.BCM)        
with Pump() as pump:
    pump.work()
    sleep(2)
    pump.stop()
