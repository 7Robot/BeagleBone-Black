import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_12", GPIO.IN)

old_switch_state = 0

while True:
   new_switch_state = GPIO.input("P8_12")
   if new_switch_state :
      GPIO.output("P8_10", GPIO.HIGH)
   else :
      GPIO.output("P8_10", GPIO.LOW)


