import os
import time
import Queue

from models.feed_scheduler import FeedScheduler
from controller import Controller
from configuration import Configuration
from heartbeat_timer import HeartbeatTimer

'''
Entry point to application, run main loop

'''
APP_ENV = os.getenv("APP_ENV", "development")

CONFIG = Configuration.for_env(APP_ENV)
HEARTBEAT_TIME = CONFIG.heartbeat_time()
FEEDS = CONFIG.feeds()
HEARTBEAT_QUEUE = Queue.Queue()
OBSERVERS = CONFIG.build_observers()

def heartbeat_callback():
  HEARTBEAT_QUEUE.put(controller.heartbeat)

def read_from_heartbeat_queue():
  while True:
    try:
      callback = HEARTBEAT_QUEUE.get(False) # doesn't block
    except Queue.Empty:
      break
    callback()

if __name__ == "__main__":
  scheduler = FeedScheduler(FEEDS)
  io_adapter = CONFIG.build_io_adapter()
  controller = Controller(scheduler, io_adapter, OBSERVERS)
  heartbeat = HeartbeatTimer(HEARTBEAT_TIME, heartbeat_callback)

  try:
    controller.start()
    heartbeat.start()

    while True:
      read_from_heartbeat_queue()
      controller.run()

  finally:
    heartbeat.stop()
    controller.shutdown()
    print("Exiting...")
