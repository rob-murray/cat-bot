import os
import logging
import logging.config
import yaml
from log_factory import LogFactory
from models.feed import Feed

class Configuration(object):
  '''
  Configuration object to provide config from file for environment
  '''

  DEV_CONFIG  = "config/development.yaml"
  PROD_CONFIG = "config/production.yaml"

  @staticmethod
  def for_env(environment_name):
    '''
    Create Configuration instance by parsing config file based on environment name
    '''
    if environment_name == "production":
      file = Configuration.PROD_CONFIG
    else:
      file = Configuration.DEV_CONFIG

    if os.path.exists(file):
      with open(file, "rt") as f:
        return Configuration(yaml.load(f.read()))
    else:
      raise Exception("Config file '%s' missing!" % file)

  def __init__(self, config):
    self.config = config
    self.setup_logging()

  def setup_logging(self):
    '''
    Set up Pythons logger for this environment
    '''
    LogFactory.from_config(default_path=self.config["logging_config"])

  def heartbeat_time(self):
    '''
    Time inteval for heartbeat tick
    '''
    return float(self.config["heartbeat_time"])

  def feeds(self):
    '''
    Return list of all Feeds
    '''
    return map(lambda feed_config: self._create_feed_from_config(feed_config), self.config["feeds"])

  def build_io_adapter(self):
    '''
    Create a new instance of configured IO adapter
    '''
    io_adapter_config = self.config["io_adapter"]

    if io_adapter_config == "RaspberryPi":
      from io_adapters.raspberry_pi import RaspberryPi
      return RaspberryPi()
    elif io_adapter_config == "LoggingIO":
      from io_adapters.logging_io import LoggingIO
      return LoggingIO()
    else:
      raise Exception("Unknown io_adapter: '%s'" % io_adapter_config)

  def _create_feed_from_config(self, feed_config):
    '''
    Private: create a Feed from a dictionary of values
    '''
    return Feed.build(feed_config)
