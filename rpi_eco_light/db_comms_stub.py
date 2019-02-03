import logging


class DBComms(object):
    def __init__(self, config_helper):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._config_helper = config_helper
        self._live_location = '.live'
        self._last_update_time = None
        self._update_checks = 0
        self._max_update_checks = 10
        self._current_kw = 0.3

    def get_current_kw(self):
        ret_val = self._current_kw
        self._current_kw += 0.1
        if self._current_kw > 1.8:
            self._current_kw = 0.3
        return ret_val

    def check_comms_status(self):
        comms_good = True
        return comms_good
