from threading import Timer

class HeartbeatTimer(object):
  '''
  A repeating Timer on separate thread.
  A wrapper around +threading.Timer+ to run new Timer at intervals.

  Usage:

def callback():
  print("message")

t = HeartbeatTimer(5.0, callback)
t.start()
# prints message
t.cancel()

  '''
  def __init__(self, interval, function, *args, **kwargs):
    self._timer     = None
    self.interval   = interval
    self.function   = function
    self.args       = args
    self.kwargs     = kwargs
    self.is_running = False

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self._timer = Timer(self.interval, self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    if self._timer:
      self._timer.cancel()
    self.is_running = False
