import ConfigParser
import os


class ConfigHelper(object):
    def __init__(self):
        dir_path = os.path.dirname(__file__)
        self._config_file_location = dir_path + '/rpi-eco-light.ini'

    def get_current_config(self):
        config = ConfigParser.ConfigParser()
        config.read(self._config_file_location)
        return config
