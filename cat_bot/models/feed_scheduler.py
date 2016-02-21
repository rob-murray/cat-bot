import logging
import time

class FeedScheduler(object):
  MANUAL_ONLY = False # No automatic feeding; only triggered by button

  def __init__(self, feeds):
    self.logger = logging.getLogger(__name__)
    self.current_feed_index = 0
    self.feeds = feeds
    self.max_feeds = len(feeds)
    self.__set_next_feed()

  def reset(self):
    '''
    A command to reset FeedScheduler to next set.
    This is a bit of a hack to go from one day to another.
    '''
    if self.__any_remaining_feeds():
      self.logger.debug("Reset called after completing all feeds")
    else:
      self.logger.error("Reset called without reaching required number of feeds")
    self.current_feed_index = 0

  def time_to_feed(self):
    '''
    Query if it is currently time for a Feed.
    This will be the case if;
      * The time currently matches a set feeding time.
      * There are remaining feeds
      * Not currently set to manual only

    Returns:
      True if all preconditions are met
    '''
    if not self.can_feed():
      return False

    if FeedScheduler.MANUAL_ONLY:
      self.logger.debug("Sorry. MANUAL_ONLY is set")
      return False

    feed = self.__next_feed()
    return feed.time_to_feed()

  def can_feed(self):
    '''
    Query if any feeds are available.

    Returns:
      True if it is possible to feed.
    '''
    if self.__any_remaining_feeds():
      return True
    else:
      self.logger.debug("Cannot feed; reached maximum feeds")
      return False

  def feed(self):
    '''
    Command to feed, returns the next feed instance and marks as completed.
    Raises Error if not permitted to feed.

    Returns:
      the Feed instance
    '''
    if not self.can_feed():
      raise AssertionError("Request to feed but not permitted. See any previous errors.")

    feed = self.__next_feed()
    self.logger.info("Preparing to feed: {}".format(feed.to_display()))
    self.__increment_feed_index()
    self.logger.debug("There are now {:d} feeds left".format(self.__feeds_remaining_count()))

    return feed

  def current_state(self):
    '''
    Query for the current state.

    Returns:
      structure with:
        * feeds_remaining
        * previous_feed (empty if none for this period)
        * next_feed (empty if none remaining for this period)
    '''
    return {
      "feeds_remaining": self.__feeds_remaining_count(),
      "previous_feed": self.__previous_feed(),
      "next_feed": self.__next_feed()
    }

  def __any_remaining_feeds(self):
    return self.current_feed_index < self.max_feeds

  def __next_feed(self):
    if self.__any_remaining_feeds():
      return self.feeds[self.current_feed_index]

  def __previous_feed(self):
    if self.current_feed_index > 0:
      return self.feeds[self.current_feed_index - 1]

  def __increment_feed_index(self):
    self.current_feed_index += 1

  def __feeds_remaining_count(self):
    return self.max_feeds - self.current_feed_index

  def __set_next_feed(self):
    '''
    Set the current_feed_index to that of the next feed.

    Find the closest to the time now as seconds since epoch.
    Note: we're not worried about O(n) here as there are so few.
    '''
    time_now = int(time.time()) # TODO this is utc i beleive :(

    # Find the min positive distance from current epoch to feed epoch; if negative (in the past) ignore it
    next_feed = min(self.feeds, key=lambda x: x.feed_epoch_time() if (x.feed_epoch_time() - time_now) > 0 else float('inf'))
    # Set to the last feed (ie max feeds reached) if the next feed is the first but its in the past
    if self.feeds.index(next_feed) == 0 and (next_feed.feed_epoch_time() - time_now) < 0:
      self.current_feed_index = len(self.feeds)
    else:
      self.current_feed_index = self.feeds.index(next_feed)

    self.logger.debug("Setting next feed to: {}".format(next_feed.to_display()))
    self.logger.debug("There are now {:d} feeds left".format(self.__feeds_remaining_count()))

