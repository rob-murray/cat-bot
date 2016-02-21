from datetime import datetime

class Event(object):
  '''
  Value object for something that has happened
    Attributes:
      name: name of event
      occured_at: the time it occured in UTC
      data: The data structure specific to event
  '''
  def __init__(self, name, data):
    self._name = name
    self._data = data
    self._occured_at = datetime.utcnow()

  @property
  def name(self):
    '''
    Get the event name
    '''
    return self._name

  @property
  def data(self):
    '''
    Get the event data
    '''
    return self._data

  @property
  def occured_at(self):
    '''
    Get the event occured_at datetime
    '''
    return self._occured_at
