from dataclasses import dataclass


@dataclass
class RangeUnit:
    gogo: float
    stop: float


def morph_rangeunit(x_rangeunit: RangeUnit, x_denom: float):
    gogo_calc_stop_calc_diff = x_rangeunit.stop - x_rangeunit.gogo
    if x_rangeunit.gogo == 0 and x_rangeunit.stop == 0:
        x_rangeunit.gogo = 0
        x_rangeunit.stop = 0
    elif x_rangeunit.gogo == x_denom and x_rangeunit.stop == x_denom:
        x_rangeunit.gogo = x_denom
        x_rangeunit.stop = x_denom
    elif gogo_calc_stop_calc_diff >= x_denom:
        x_rangeunit.gogo = 0
        x_rangeunit.stop = x_denom
    else:
        x_rangeunit.gogo = x_rangeunit.gogo % x_denom
        morphed_stop = x_rangeunit.stop % x_denom
        x_rangeunit.stop = x_denom if morphed_stop == 0 else morphed_stop


def get_morphed_rangeunit(x_gogo: float, x_stop: float, x_denom: float) -> RangeUnit:
    x_rangeunit = RangeUnit(x_gogo, x_stop)
    morph_rangeunit(x_rangeunit, x_denom)
    return x_rangeunit
