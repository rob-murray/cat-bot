import RPi.GPIO as GPIO
import time
import logging

SERVO_PIN = 18
CONTROL_FREQ = 50
LED_PIN = 25
BUZZER_PIN = 24
FEED_BUTTON_PIN = 8

# TODO configurise
SOUND_BUZZER = True
PITCH = 500

class RaspberryPi(object):

  def __init__(self, controller):
    self.logger = logging.getLogger(__name__)
    self.controller = controller

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(FEED_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    self.pwm = GPIO.PWM(SERVO_PIN, CONTROL_FREQ)

    # This callback will be run in another thread; irl we will need to synchronise getting and setting feeding schedule
    GPIO.add_event_detect(FEED_BUTTON_PIN, GPIO.FALLING, callback=self.button_pressed, bouncetime=1000)

  def buzz(self, pitch, duration):
    pitch = float(pitch)
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
      GPIO.output(BUZZER_PIN, True)
      time.sleep(delay)
      GPIO.output(BUZZER_PIN, False)
      time.sleep(delay)

  def light_on(self):
    GPIO.output(LED_PIN, True)

  def light_off(self):
    GPIO.output(LED_PIN, False)

  def feed(self, feed):
    '''
    Command to initiate a feeding

    Args:
      feed: the feed instance
    '''
    self.logger.debug("Feeding: {}".format(feed.to_display()))

    if SOUND_BUZZER:
        self.buzz(PITCH, 1)
    self.light_on()
    self.pwm.start(1)
    time.sleep(feed.quantity)
    self.pwm.stop()
    self.light_off()
    self.logger.debug("Feed ended")

  def button_pressed(self, channel):
    self.logger.debug("Button pressed!")
    self.controller.button_pressed()

  def startup(self):
    '''
    Called when application is starting up
    '''
    self.logger.debug("Startup")
    self.light_off()
    GPIO.output(BUZZER_PIN, False)

  def beat(self):
    '''
    Called for each internal tick or heartbeat
    '''
    self.logger.debug("heartbeat felt")
    self.light_on()
    time.sleep(0.5)
    self.light_off()

  def shutdown(self):
    '''
    Called when application is shutting down
    '''
    self.logger.info("Shutting down GPIO")
    self.pwm.stop()
    GPIO.output(BUZZER_PIN, False)
    self.light_off()
    GPIO.cleanup()
