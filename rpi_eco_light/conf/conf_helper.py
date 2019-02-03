import ConfigParser


class ConfigHelper(object):
    def __init__(self, config_file):
        self._config_file_location = config_file

    def get_current_config(self):
        config = ConfigParser.ConfigParser()
        config.read(self._config_file_location)
        return config
