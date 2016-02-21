import time
from feed_time import FeedTime

class Feed(object):
  '''
  A Feed; the mealtime for the cat
    Attributes:
      name: name of the feed, eg morning
      quantity: time for servo to rotate ;)
      feed_time: The FeedTime instance containing time of feed
  '''

  '''
  This is currently the time for the servo to rotate which equates to quantity of food
  '''
  DEFAULT_QUANTITY = 0.60 # This is OK with low food
  #DEFAULT_QUANTITY = 0.45 This worked OK with slightly more food in

  @staticmethod
  def build(feed_config):
    '''
    Factory method to create feed from dictionary
    '''
    return Feed(
      feed_config["name"],
      FeedTime(feed_config["hour"], feed_config["minute"]),
      Feed.DEFAULT_QUANTITY
    )

  def __init__(self, name, feed_time, quantity):
    self.name = name
    self.feed_time = feed_time
    self.quantity = quantity

  def time_to_feed(self):
    '''
    Is it time to feed this feed? TODO Hmmm, sounds odd; rename this method
    Delegates to FeedTime.
    Returns boolean
    '''
    time_now = time.localtime(time.time())
    return time_now == self.feed_time

  def feed_epoch_time(self):
    '''
    Return the feed time as seconds since epoch. Delegates to FeedTime.
    '''
    return self.feed_time.to_epoch_time()

  def to_display(self):
    return "<Feed: name={} quantity={:.2f} {}>".format(self.name, self.quantity, self.feed_time.to_display())
