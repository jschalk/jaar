from src.a01_term_logic.rope import create_rope
from src.a06_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.a07_timeline_logic.timeline_main import (
    BeliefTimelinePoint,
    add_newtimeline_planunit,
    belieftimelinepoint_shop,
    get_timeline_rope,
    timeline_config_shop,
)
from src.a15_coin_logic.coin_main import CoinUnit


def get_coin_belieftimelinepoint(coinunit: CoinUnit) -> BeliefTimelinePoint:
    """Returns BeliefTimelinePoint from CoinUnit attributes."""
    coinunit.set_offi_time_max(0)
    # create empty beliefunit
    x_beliefunit = beliefunit_shop(
        belief_name="for_belieftimelinepoint_calculation",
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
    add_newtimeline_planunit(x_beliefunit, coin_timeline_config)
    x_belieftimelinepoint = belieftimelinepoint_shop(x_beliefunit, timeline_rope, 0)
    x_belieftimelinepoint.calc_timeline()
    return x_belieftimelinepoint
