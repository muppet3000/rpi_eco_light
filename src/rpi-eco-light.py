#!/usr/bin/python

import time
import sys
import signal

from energy_usage_light import EnergyUsageLight

DB_PATH = "/opt/eagleowl"
SLEEP_TIME_IN_SECS = 5
COST_PER_HOUR_IN_PENCE = 13.37


def signal_term_handler(signal, frame):
    print 'got SIGTERM'
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_term_handler)
    usage_light = EnergyUsageLight(DB_PATH, COST_PER_HOUR_IN_PENCE)
    while True:
        usage_light.update()
        #Flush the stdout each time round the loop
        sys.stdout.flush()

        #Sleep for a bit before the next update
        time.sleep(SLEEP_TIME_IN_SECS)
