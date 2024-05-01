from controller.led import Led

with Led() as led:
    led.set(True)

    import time
    time.sleep(5)