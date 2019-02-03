import logging
import os
import time


class DBComms(object):
    def __init__(self, config_helper):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._config_helper = config_helper
        self._live_location = '.live'
        self._last_update_time = None
        self._update_checks = 0
        self._max_update_checks = 10

    @property
    def _current_config(self):
        return self._config_helper.get_current_config()

    def _db_file(self):
        return '{}/{}'.format(self._current_config.get('service', 'db_path'), self._live_location)

    def get_current_kw(self):
        with open(self._db_file(), 'r') as live_file:
            line = live_file.readline()
            splits = line.split()
            kw = 0
            if len(splits) >= 4:
                # This is a small tweak because the live file returns W not KW - Stoopid!
                kw = float(splits[3])
                kw /= 1000
            return kw

    def check_comms_status(self):
        comms_good = True
        self._max_update_checks = self._current_config.get('service', 'max_update_checks')
        temp_last_update_time = time.ctime(os.path.getmtime(self._db_file()))
        if not self._last_update_time:
            # not initialised
            self._last_update_time = temp_last_update_time
        else:
            if self._last_update_time != temp_last_update_time:
                # Last update time is different from new one, therefore all is good
                self._last_update_time = temp_last_update_time
                self._update_checks = 0
            else:
                # Update time has not changed, we should see when it last changed
                self._update_checks += 1
                if self._update_checks >= self._max_update_checks:
                    # We've reached our max attempts to query - something's gone wrong
                    self._logger.error('Max update checks reached, last update time: {!s}'.format(temp_last_update_time))
                    comms_good = False
                else:
                    self._logger.debug('Value has not been updated in {:d} queries, max queries before error: {:d}'.format(self._update_checks, self._max_update_checks))
        return comms_good
