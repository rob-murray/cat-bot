# -*- coding: utf-8 -*-

import logging
import time

class LoggingIO(object):
  '''
  An IO implementation that just logs everything. Used for testing.
  '''
  def __init__(self, controller):
    self.logger = logging.getLogger(__name__)
    self.controller = controller

  def feed(self, feed):
    '''
    Command to initiate a feeding

    Args:
      feed: the feed instance
    '''
    self.logger.info("Feeding: {}".format(feed.to_display()))

  def button_pressed(self):
    self.logger.debug("Button pressed!")
    # TODO how to simulate this

  def startup(self):
    '''
    Called when application is starting up
    '''
    self.logger.info("Startup")

  def beat(self):
    '''
    Called for each internal tick or heartbeat
    '''
    self.logger.info("heartbeat felt 💓💓")

  def shutdown(self):
    '''
    Called when application is shutting down
    '''
    self.logger.info("Shutting down")
