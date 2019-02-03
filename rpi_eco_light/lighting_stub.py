import logging
import time


class Lighting(object):
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (177, 142, 52)
    ORANGE = (255, 165, 0)
    RED = (255, 0, 0)
    PURPLE = (148, 0, 211)

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._current_value = self.BLUE
        self._set_whole_grid(self._current_value)

    def set_light(self, target_value):
        set_to_value = self._current_value
        while set_to_value != target_value:
            set_to_value = self._fade_between_rgb(set_to_value, target_value, 1)
            self._set_whole_grid(set_to_value)
            time.sleep(0.01)
        self._current_value = set_to_value

    def set_error(self):
        self._current_value = self.PURPLE
        self._logger.error('Light set to error state')

    def _set_whole_grid(self, rgb_val):
        pixels = []
        for _ in range(8):
            pixels.append([])
            for _ in range(8):
                pixels[len(pixels) - 1].append(rgb_val)
        return pixels

    def _fade_between_rgb(self, current_rgb, desired_rgb, change_step=2):
        r = 0
        g = 0
        b = 0
        for i in range(0, change_step):
            r = self._inc_dec(current_rgb[0], desired_rgb[0])
            g = self._inc_dec(current_rgb[1], desired_rgb[1])
            b = self._inc_dec(current_rgb[2], desired_rgb[2])
        return r, g, b

    def _inc_dec(self, curr_val, des_val):
        ret_val = curr_val
        if curr_val < des_val:
            ret_val += 1
        elif curr_val > des_val:
            ret_val -= 1
        return ret_val
