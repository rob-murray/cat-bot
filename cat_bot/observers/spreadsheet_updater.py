# -*- coding: utf-8 -*-


class SpreadsheetUpdater(object):
  '''
  Class that implements our observer interface to respond to events
  Updates Spreadsheet via Iftt for heartbeat and feed events
  '''
  # def __init__(self):
  #   # todo

  def notify(self, event):
    if event.name == "heartbeat":
      print("send heartbeat update")
    elsif event.name == "feed":
      print("feeding time")

