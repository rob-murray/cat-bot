'''
A script to be used to calibrate feeding quantity; ie the servo rotation time
required for a desired weight of food.

Usage:
  $ python tests/calibrate.py -t 0.45
'''
import sys, getopt
import RPi.GPIO as GPIO
import time

feeding_time = 0.45 # default; fetched from args

SERVO_PIN = 18
CONTROL_FREQ = 50
LED_PIN = 25
FEED_BUTTON_PIN = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(FEED_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pwm = GPIO.PWM(SERVO_PIN, CONTROL_FREQ)

def light_on():
  GPIO.output(LED_PIN, True)

def light_off():
  GPIO.output(LED_PIN, False)

def button_pressed(channel):
  feed()

def feed():
  print("feeding with time: %0.2f" % feeding_time)
  light_on()
  pwm.start(1)
  time.sleep(feeding_time)
  pwm.stop()
  light_off()

myopts, args = getopt.getopt(sys.argv[1:],"t:")
for o, a in myopts:
  if o == '-t':
    rotation_time_val = a
  else:
    print("Usage: %s -t rotation time" % sys.argv[0])
    sys.exit()

feeding_time = float(rotation_time_val)
GPIO.add_event_detect(FEED_BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=1000)

try:
    while True:
      pass

finally:
    print("Cleaning up")
    pwm.stop()
    GPIO.cleanup()
