import ConfigParser

class ConfigHelper:
    def __init__(self):
        self._config_file_location = "conf/rpi-eco-light.ini"

    def get_current_config(self):
      config = ConfigParser.ConfigParser()
      config.read(self._config_file_location)
      return config
