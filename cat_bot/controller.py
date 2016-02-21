import logging
import time
import Queue
import threading
from models.event import Event

class Controller(object):
  '''
  A class to coordinate events

  '''

  def __init__(self, scheduler, io_adapter, observers=None):
    '''
    Constructor

    Arguments:
      scheduler: initialized object that can schedule feeding events
      io_adapter: IO object

    '''
    self.logger = logging.getLogger(__name__)
    self.scheduler = scheduler
    self.io_adapter = io_adapter
    self.event_queue = Queue.Queue()
    if observers is None:
      self.observers = []
    else:
      self.observers = observers

  def start(self):
    '''
    Called when application is starting up
    Initiate IO adapter and start monitoring for events
    '''
    self.io_adapter.on_button_press(self.button_pressed)
    self.io_adapter.startup()
    self._notify_observers(Event("startup", self.scheduler.current_state()))

  def run(self):
    # Non-blocking fetch from queue
    while True:
      try:
        callback = self.event_queue.get(False)
      except Queue.Empty:
        break
      callback()


  def button_pressed(self):
    '''
    A callback from the IO adapter to state that a feed is requested
    Put message onto Queue and return
    '''
    self.event_queue.put(self._trigger_manual_feeding)

  def heartbeat(self):
    '''
    Each internal tick or heartbeat of application.
    Put message onto Queue and return
    '''
    self.event_queue.put(self._heartbeat_tick)

  def shutdown(self):
    '''
    Called when application is exiting, give IO adapter chance to clean up

    '''
    self.io_adapter.shutdown()

  def _trigger_manual_feeding(self):
    '''
    Private: Called to trigger a manual feeding upon button press or external event
    '''
    self.logger.debug(">>> Button pressed call >>>")
    if self.scheduler.can_feed():
      feeding = self.scheduler.feed()
      self._invoke_feeder(feeding)

  def _invoke_feeder(self, feeding):
    '''
    Private: set io adapter to feed;
    Call IO adapter to feed on another thread
    TODO: synchronise access to io_adapter; we could have race condition here
    '''
    self._notify_observers(Event("feeding", feeding))
    feeder_thread = threading.Thread(target=self.io_adapter.feed, args=(feeding,))
    feeder_thread.start()
    feeder_thread.join()

  def _heartbeat_tick(self):
    '''
    Private: internal callback for heartbeat
    Coordinate events such as checking for feeding time or resettting
    '''
    self.logger.debug(">>> heartbeat >>>")
    self.io_adapter.tick()
    self._notify_observers(Event("heartbeat", self.scheduler.current_state()))

    time_now = time.localtime(time.time())
    if time_now.tm_hour == 0 and time_now.tm_min == 0:
      self.logger.debug("It's midnight - resettting!")
      self.scheduler.reset()

    if self.scheduler.time_to_feed():
      self.logger.debug("Time to feed !!!")
      feeding = self.scheduler.feed()
      self._invoke_feeder(feeding)
    else:
      self.logger.debug("Not time yet...")

  def _notify_observers(self, event):
    '''
    For a given event, notify all observers.
    Run each case in another thread daemon so as not to block main program
    TODO: manage this in pool
    '''
    for observer in self.observers:
      t = threading.Thread(target=observer.notify, args=[event])
      t.setDaemon(True)
      t.start()
