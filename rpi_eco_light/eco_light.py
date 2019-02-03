import argparse
import logging.config
import signal
import sys
import time

from rpi_eco_light.conf.conf_helper import ConfigHelper
from rpi_eco_light.conf.logging import LOGGING
from rpi_eco_light.energy_usage_light import EnergyUsageLight

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def signal_term_handler(signal, frame):
    logger.fatal('Handling SIGTERM')
    sys.exit(0)


def run_eco_light():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='The config file to use')
    args = parser.parse_args()

    logger.info('Starting RPi ECO Light - config: {}'.format(args.config))
    config_helper = ConfigHelper(args.config)
    signal.signal(signal.SIGINT, signal_term_handler)
    usage_light = EnergyUsageLight(config_helper)
    while True:
        current_config = config_helper.get_current_config()
        LOGGING['handlers']['console']['level'] = current_config.get('service', 'log_level')
        logging.config.dictConfig(LOGGING)

        usage_light.update()
        # Flush the stdout each time round the loop
        sys.stdout.flush()

        # Sleep for a bit before the next update
        time.sleep(float(current_config.get('service', 'update_interval_in_sec')))


if __name__ == '__main__':
    run_eco_light()
