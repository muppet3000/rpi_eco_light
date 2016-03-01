import os
import time


class DBComms:
    def __init__(self, db_location):
        self._db_location = db_location
        self._live_location = ".live"
        self._last_update_time = None
        self._update_checks = 0
        self._max_update_checks = 10

    def get_current_kw(self):
        with open("{}/{}".format(self._db_location,
                                 self._live_location),
                  "r") as live_file:
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
        temp_last_update_time = time.ctime(os.path.getmtime(self._db_location + "/" + self._live_location))
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
                    print "Max update checks reached, last update time: %s" % temp_last_update_time
                    comms_good = False
        return comms_good
