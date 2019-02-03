from mock import Mock
import pytest

from rpi_eco_light import energy_usage_light
from rpi_eco_light.energy_usage_light import EnergyUsageLight, kw_to_rgb
from rpi_eco_light.lighting import Lighting


class MockConfig(object):
    def __init__(self, config):
        self._config = {}
        self._set_config(config)

    def _set_config(self, config):
        for section, key_values in config.items():
            self._config[section] = key_values

    def get(self, section, key):
        return self._config[section][key]

    def getfloat(self, section, key):
        return float(self._config[section][key])


class MockConfigHelper(object):
    def __init__(self, config):
        self.config = config

    def get_current_config(self):
        return self.config


@pytest.fixture
def config_values():
    return {
        'monitor': {
            'type': 'KW'
        },
        'levels': {
            'level_1': 0.6,
            'level_2': 0.75,
            'level_3': 1.1,
            'level_4': 1.46
        }
    }


@pytest.mark.parametrize(('kw', 'expected_rgb'), [
    (
        0,
        Lighting.PURPLE
    ),
    (
        0.5,
        Lighting.BLUE
    ),
    (
        0.6,
        Lighting.GREEN
    ),
    (
        0.7,
        Lighting.GREEN
    ),
    (
        0.75,
        Lighting.YELLOW
    ),
    (
        1.0,
        Lighting.YELLOW
    ),
    (
        1.1,
        Lighting.ORANGE
    ),
    (
        1.4,
        Lighting.ORANGE
    ),
    (
        1.46,
        Lighting.RED
    ),
    (
        2,
        Lighting.RED
    ),
    (
        100,
        Lighting.RED
    )
])
def test_kw_to_rgb(kw, config_values, expected_rgb):
    mock_config = MockConfig(config_values)
    actual_rgb = kw_to_rgb(kw, mock_config)
    assert actual_rgb == expected_rgb, 'Expected {} KW to convert to RGB {}, got {} instead'.format(
        kw,
        expected_rgb,
        actual_rgb)


def test_update_respects_config_changes(monkeypatch):
    config_values = {
        'monitor': {
            'type': 'KW'
        },
        'levels': {
            'level_1': 0.6,
            'level_2': 0.75,
            'level_3': 1.1,
            'level_4': 1.46
        }
    }

    class MockDBComms(object):
        def __init__(self):
            self._kw = 0

        def __call__(self, *args, **kwargs):
            return self

        def check_comms_status(self):
            return True

        def get_current_kw(self):
            return self._kw

    mock_lighting_set_light = Mock()
    monkeypatch.setattr(Lighting, 'set_light', mock_lighting_set_light)
    mock_db_comms = MockDBComms()
    monkeypatch.setattr(energy_usage_light, 'DBComms', mock_db_comms)
    mock_config = MockConfig(config_values)
    mock_config_helper = MockConfigHelper(mock_config)

    light = EnergyUsageLight(mock_config_helper)
    mock_db_comms._kw = 0.6
    light.update()
    mock_lighting_set_light.assert_called_once_with(Lighting.GREEN)
    mock_config_helper.config._config['levels']['level_1'] = 0.7  # update config levels
    mock_lighting_set_light.reset_mock()
    light.update()
    mock_lighting_set_light.assert_called_once_with(Lighting.BLUE)
