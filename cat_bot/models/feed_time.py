import time
import datetime

class FeedTime(object):
  '''
  The
    Attributes:
      hour_of_the_day: hour to be fed in 24 hour clock
      minute_of_the_day: minute of the hour to be fed
  '''

  def __init__(self, hour_of_the_day, minute_of_the_day):
    self.hour_of_the_day = hour_of_the_day
    self.minute_of_the_day = minute_of_the_day

  def to_epoch_time(self):
    '''
    Return time of feed as seconds since epoch
    '''
    return time.mktime(self.to_datetime().timetuple())

  def to_datetime(self):
    '''
    Return the feed time as a datetime
    Note that this will use the current date
    '''
    feed_time = datetime.time(self.hour_of_the_day, self.minute_of_the_day, 0)
    return datetime.datetime.combine(datetime.datetime.today(), feed_time)

  def __eq__(self, other):
    '''
    Override equality check to test against 'time.struct_time'
    TODO: fix this type problem here
    '''
    if type(other) is type(self):
      return self.hour_of_the_day == other.hour_of_the_day and self.minute_of_the_day == other.minute_of_the_day

    # TODO check for/coerce time/datetime type
    # for now assume its a time tuple https://docs.python.org/2/library/time.html#time.struct_time
    if self.hour_of_the_day == other[3] and self.minute_of_the_day == other[4]:
      return True
    else:
      return False

  def to_display(self):
    return "<FeedTime: hour={:d} minute={:d}>".format(self.hour_of_the_day, self.minute_of_the_day)
