from db_comms import DBComms
from lighting import Lighting


def kw_to_rgb(kw, pence_per_hour):
    """
    Converts Power (KW) to a RGB value
    :param kw: power
    :param pence_per_hour: the cost in pence per kw per hour
    :return: a dict for RGB values
    """
    kw_in_pence = pence_per_hour * kw
    print "KW in pence: %s" % kw_in_pence
    if kw_in_pence >= 20:
        print(">= 20 = RED")
        rgb_dict = Lighting.RED
    elif kw_in_pence >= 15:
        print("< 20 && >= 15 = ORANGE")
        rgb_dict = Lighting.ORANGE
    elif kw_in_pence >= 10:
        print("< 15 && >= 10 = YELLOW")
        rgb_dict = Lighting.YELLOW
    elif kw_in_pence >= 8:
        print("< 10 && >= 8 = GREEN")
        rgb_dict = Lighting.GREEN
    elif 0 > kw_in_pence < 8:
        print("< 8 = BLUE")
        rgb_dict = Lighting.BLUE
    elif kw_in_pence == 0:
        print("==0 = PURPLE (No value yet)")
        rgb_dict = Lighting.PURPLE
    else:
        rgb_dict = Lighting.GREEN

    return rgb_dict


class EnergyUsageLight(object):
    def __init__(self, db_path, pence_per_hour):
        self._comms = DBComms(db_path)
        self._light = Lighting()
        self._pence_per_hour = pence_per_hour

    def update(self):
        if not self._comms.check_comms_status():
            self._light.set_error()
        else:
            kw = self._comms.get_current_kw()
            rgb_dict = kw_to_rgb(kw, self._pence_per_hour)
            self._light.set_light(rgb_dict)
