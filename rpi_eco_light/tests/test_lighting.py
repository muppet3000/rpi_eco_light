import pytest

from rpi_eco_light.lighting import Lighting


@pytest.mark.parametrize(('rgb_value', 'expected_pixels'), [
    (
        Lighting.BLUE,
        [[Lighting.BLUE] * 8] * 8
    ),
    (
        Lighting.GREEN,
        [[Lighting.GREEN] * 8] * 8
    ),
    (
        Lighting.YELLOW,
        [[Lighting.YELLOW] * 8] * 8
    ),
    (
        Lighting.ORANGE,
        [[Lighting.ORANGE] * 8] * 8
    ),
    (
        Lighting.RED,
        [[Lighting.RED] * 8] * 8
    ),
    (
        Lighting.PURPLE,
        [[Lighting.PURPLE] * 8] * 8
    )
])
def test_set_whole_grid(rgb_value, expected_pixels):
    lighting_controller = Lighting()
    actual_pixels = lighting_controller._set_whole_grid(rgb_value)
    assert actual_pixels == expected_pixels
