# -*- coding: utf-8 -*-

import logging
import time

class LoggingIO(object):
  '''
  An IO implementation that just logs everything. Used for testing.
  '''
  def __init__(self):
    self.logger = logging.getLogger(__name__)

  def feed(self, feed):
    '''
    Command to initiate a feeding

    Args:
      feed: the feed instance
    '''
    self.logger.info("Feeding: {}".format(feed.to_display()))

  def on_button_press(self, callback):
    '''
    Add a callback for when feed button is pressed
    '''
    self.invoke_feed_callback = callback

  def button_pressed(self):
    self.logger.debug("Button pressed!")
    # TODO how to simulate this
    # self.invoke_feed_callback()

  def startup(self):
    '''
    Called when application is starting up
    '''
    self.logger.info("Startup")

  def tick(self):
    '''
    Called for each internal tick or heartbeat
    '''
    self.logger.info("heartbeat felt 💓💓")

  def shutdown(self):
    '''
    Called when application is shutting down
    '''
    self.logger.info("Shutting down")
