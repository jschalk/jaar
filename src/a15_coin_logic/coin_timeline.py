from src.a01_term_logic.rope import create_rope
from src.a06_believer_logic.believer_main import BelieverUnit, believerunit_shop
from src.a07_timeline_logic.timeline_main import (
    BelieverTimelinePoint,
    add_newtimeline_planunit,
    believertimelinepoint_shop,
    get_timeline_rope,
    timeline_config_shop,
)
from src.a15_coin_logic.coin_main import CoinUnit


def get_coin_believertimelinepoint(coinunit: CoinUnit) -> BelieverTimelinePoint:
    """Returns BelieverTimelinePoint from CoinUnit attributes."""
    coinunit.set_offi_time_max(0)
    # create empty believerunit
    x_believerunit = believerunit_shop(
        believer_name="for_believertimelinepoint_calculation",
        coin_label=coinunit.coin_label,
        knot=coinunit.knot,
        fund_iota=coinunit.fund_iota,
        respect_bit=coinunit.respect_bit,
        penny=coinunit.penny,
    )
    timeline_rope = get_timeline_rope(
        coin_label=coinunit.coin_label,
        timeline_label=coinunit.timeline.timeline_label,
        knot=coinunit.knot,
    )
    coin_timeline_config = coinunit.timeline.to_dict()
    # create timeline plan from coinunit.timeline_config
    add_newtimeline_planunit(x_believerunit, coin_timeline_config)
    x_believertimelinepoint = believertimelinepoint_shop(
        x_believerunit, timeline_rope, 0
    )
    x_believertimelinepoint.calc_timeline()
    return x_believertimelinepoint
