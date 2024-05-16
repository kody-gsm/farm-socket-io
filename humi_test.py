import adafruit_dht
import board
import time
import RPi.GPIO as GPIO


h = adafruit_dht.DHT11(board.D18)

while True:
	try:
		print(h.temperature, h.humidity)
		time.sleep(0.2)
	except RuntimeError as error:
		print(error)
		time.sleep(0.5)
