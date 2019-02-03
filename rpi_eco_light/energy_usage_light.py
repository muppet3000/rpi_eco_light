import logging

from db_comms import DBComms
from lighting import Lighting


logger = logging.getLogger(__name__)


def kw_to_rgb(kw, current_config):
    """
    Converts Power (KW) to a RGB value
    :param kw: power
    :param current_config: the current configuration file
    :return: a tuple for RGB values
    """
    lighting_value = kw
    if current_config.get('monitor', 'type') == 'PENCE':
        lighting_value = current_config.getfloat('monitor', 'cost_per_hour_in_pence') * kw
        logger.debug('KW in pence: %s' % lighting_value)
    else:
        logger.debug('KW: %s' % lighting_value)

    level_1 = current_config.getfloat('levels', 'level_1')
    level_2 = current_config.getfloat('levels', 'level_2')
    level_3 = current_config.getfloat('levels', 'level_3')
    level_4 = current_config.getfloat('levels', 'level_4')

    if lighting_value >= level_4:
        logger.debug('>= {:.2f} = RED'.format(level_4))
        rgb_value = Lighting.RED
    elif lighting_value >= level_3:
        logger.debug('< {:.2f} && >= {:.2f} = ORANGE'.format(level_4, level_3))
        rgb_value = Lighting.ORANGE
    elif lighting_value >= level_2:
        logger.debug('< {:.2f} && >= {:.2f} = YELLOW'.format(level_3, level_2))
        rgb_value = Lighting.YELLOW
    elif lighting_value >= level_1:
        logger.debug('< {:.2f} && >= {:.2f} = GREEN'.format(level_2, level_1))
        rgb_value = Lighting.GREEN
    elif 0 < lighting_value < level_1:
        logger.debug('< {:.2f} = BLUE'.format(level_1))
        rgb_value = Lighting.BLUE
    elif lighting_value == 0:
        logger.debug('==0 = PURPLE (No value yet)')
        rgb_value = Lighting.PURPLE
    else:
        rgb_value = Lighting.GREEN

    return rgb_value


class EnergyUsageLight(object):
    def __init__(self, config_helper):
        self._config_helper = config_helper
        self._comms = DBComms(config_helper)
        self._light = Lighting()

    def update(self):
        current_config = self._config_helper.get_current_config()

        if not self._comms.check_comms_status():
            self._light.set_error()
        else:
            kw = self._comms.get_current_kw()
            rgb_dict = kw_to_rgb(kw, current_config)
            self._light.set_light(rgb_dict)
