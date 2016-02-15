import logging
import time

class Controller(object):
  '''
  A class to coordinate events

  '''

  def __init__(self, scheduler):
    '''
    Constructor

    Arguments:
      scheduler: initialized object that can schedule feeding events

    '''
    self.logger = logging.getLogger(__name__)
    self.scheduler = scheduler

  def start(self, io_adapter):
    '''
    Called when application is starting up

    Arguments:
      io_adapter: the initialized IO object

    '''
    self.io_adapter = io_adapter
    self.io_adapter.startup()

  def button_pressed(self):
    '''
    A callback from the IO adapter to state that a feed is requested

    '''
    self.logger.debug(">>> Button pressed >>>")
    if self.scheduler.can_feed():
      feeding = self.scheduler.feed()
      self.io_adapter.feed(feeding)

  def heartbeat(self):
    '''
    Each internal tick or heartbeat of application.
    Coordinate events such as checking for feeding time or resettting

    '''
    self.logger.debug(">>> heartbeat >>>")
    self.io_adapter.beat()

    time_now = time.localtime(time.time())
    if time_now.tm_hour == 0 and time_now.tm_min == 0:
      self.logger.debug("It's midnight - resettting!")
      self.scheduler.reset()

    if self.scheduler.time_to_feed():
      self.logger.debug("Time to feed !!!")
      feeding = self.scheduler.feed()
      self.io_adapter.feed(feeding)
    else:
      self.logger.debug("Not time yet...")

  def shutdown(self):
    '''
    Called when application is exiting, give IO adapter chance to clean up

    '''
    self.io_adapter.shutdown()
