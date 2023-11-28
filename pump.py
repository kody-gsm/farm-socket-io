import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define motor control pins
motor_in1 = 14  # Replace with the actual GPIO pin number
motor_in2 = 18  # Replace with the actual GPIO pin number

# Setup motor control pins
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)

# Motor forward
GPIO.output(motor_in1, GPIO.HIGH)
GPIO.output(motor_in2, GPIO.LOW)

# Run for 2 seconds
time.sleep(2)

# Stop motor
GPIO.output(motor_in1, GPIO.LOW)
GPIO.output(motor_in2, GPIO.LOW)

# Clean up GPIO
GPIO.cleanup()