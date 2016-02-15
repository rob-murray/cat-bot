import os
import logging
import logging.config
import yaml

class LogFactory(object):
  '''
  Build logging from configuration

  @example
  LogFactory.from_config(default_path="path to config")

  logger = logging.getLogger(__name__)
  '''

  @staticmethod
  def from_config(
      default_path="config/logging-prod.yaml",
      default_level=logging.DEBUG
    ):
    path = default_path

    if os.path.exists(path):
      with open(path, "rt") as f:
        config = yaml.load(f.read())
      print("Starting with logger config from '%s'" % path)

      logging.config.dictConfig(config)
    else:
      print("Starting with basic logger config")

      logging.basicConfig(level=default_level)
