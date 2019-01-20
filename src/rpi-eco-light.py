#!/usr/bin/python

import time
import sys
import signal

import logging
import logging.config

from conf.logging import LOGGING
from conf.conf_helper import ConfigHelper
from energy_usage_light import EnergyUsageLight

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

config_helper = ConfigHelper()

def signal_term_handler(signal, frame):
    logger.fatal("Handling SIGTERM")
    sys.exit(0)

if __name__ == "__main__":
    logger.info("Starting RPi ECO Light")
    signal.signal(signal.SIGINT, signal_term_handler)
    usage_light = EnergyUsageLight(config_helper)
    while True:
        current_config = config_helper.get_current_config()
        LOGGING['handlers']['console']['level'] = current_config.get('service','log_level')
        logging.config.dictConfig(LOGGING)

        usage_light.update()
        #Flush the stdout each time round the loop
        sys.stdout.flush()

        #Sleep for a bit before the next update
        time.sleep(float(current_config.get('service','update_interval_in_sec')))
