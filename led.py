import board
import digitalio

# Initial the dht device, with data pin connected to:

d10=board.D10
led = digitalio.DigitalInOut(d10)
led.direction = digitalio.Direction.OUTPUT

led.value = False