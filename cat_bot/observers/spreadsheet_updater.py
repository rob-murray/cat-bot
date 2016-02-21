import requests

class SpreadsheetUpdater(object):
  '''
  Class that implements our observer interface to respond to events
  Updates a spreadsheet via Iftt for heartbeat and feed events, to collate logs really
  '''

  BASE_URL = "https://maker.ifttt.com/trigger/{ifttt_event_name}/with/key/{api_key}"

  def __init__(self, api_key, ifttt_event_name):
    self.api_key = api_key
    self.ifttt_event_name = ifttt_event_name

  def notify(self, event):
    '''
    Handle an event from the system
    '''
    if event.name == "heartbeat":
      self._update_with_heartbeat_event(event)
    elif event.name == "feeding":
      self._update_with_feeding_event(event)
    elif event.name == "startup":
      self._update_with_startup_event(event)

  def _update_with_heartbeat_event(self, event):
    next_feed = ""
    remaining_feeds = "Remaining feeds: {}".format(event.data["feeds_remaining"])
    if event.data["next_feed"] is not None:
      next_feed = "Next feed {}".format(event.data["next_feed"].to_display())
    data = {"value1": "heartbeat", "value2": remaining_feeds, "value3": next_feed}
    self._send_with_json_data(data)

  def _update_with_startup_event(self, event):
    next_feed = ""
    remaining_feeds = "Remaining feeds: {}".format(event.data["feeds_remaining"])
    if event.data["next_feed"] is not None:
      next_feed = "Next feed {}".format(event.data["next_feed"].to_display())
    data = {"value1": "startup", "value2": remaining_feeds, "value3": next_feed}
    self._send_with_json_data(data)

  def _update_with_feeding_event(self, event):
    feed = event.data
    data = {"value1": "feeding", "value2": feed.name}
    self._send_with_json_data(data)

  def _send_with_json_data(self, payload):
    requests.post(self._build_url(), json=payload)

  def _build_url(self):
    return SpreadsheetUpdater.BASE_URL.format(ifttt_event_name=self.ifttt_event_name, api_key=self.api_key)
