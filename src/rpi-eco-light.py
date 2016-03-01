#!/usr/bin/python

import time
import sys
import signal

import logging
import logging.config

from conf.logging import LOGGING
from energy_usage_light import EnergyUsageLight


DB_PATH = "/opt/eagleowl"
SLEEP_TIME_IN_SECS = 5
COST_PER_HOUR_IN_PENCE = 13.37

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def signal_term_handler(signal, frame):
    logger.fatal("Handling SIGTERM")
    sys.exit(0)


if __name__ == "__main__":
    logger.info("Starting RPi ECO Light")
    signal.signal(signal.SIGINT, signal_term_handler)
    usage_light = EnergyUsageLight(DB_PATH, COST_PER_HOUR_IN_PENCE)
    while True:
        usage_light.update()
        #Flush the stdout each time round the loop
        sys.stdout.flush()

        #Sleep for a bit before the next update
        time.sleep(SLEEP_TIME_IN_SECS)
