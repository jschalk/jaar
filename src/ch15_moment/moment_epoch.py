from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch14_epoch.epoch_main import (
    BeliefEpochTime,
    add_epoch_planunit,
    beliefEpochTime_shop,
    get_epoch_rope,
)
from src.ch15_moment.moment_main import MomentUnit


def get_moment_beliefEpochTime(momentunit: MomentUnit) -> BeliefEpochTime:
    """Returns BeliefEpochTime from MomentUnit attrs."""
    momentunit.set_offi_time_max(0)
    # create empty beliefunit
    x_beliefunit = beliefunit_shop(
        belief_name="for_beliefEpochTime_calculation",
        moment_label=momentunit.moment_label,
        knot=momentunit.knot,
        fund_grain=momentunit.fund_grain,
        respect_grain=momentunit.respect_grain,
        mana_grain=momentunit.mana_grain,
    )
    moment_epoch_label = momentunit.epoch.epoch_label
    epoch_rope = get_epoch_rope(
        moment_label=momentunit.moment_label,
        epoch_label=moment_epoch_label,
        knot=momentunit.knot,
    )
    moment_epoch_config = momentunit.epoch.to_dict()
    # create epoch plan from momentunit.epoch_config
    add_epoch_planunit(x_beliefunit, moment_epoch_config)
    x_beliefEpochTime = beliefEpochTime_shop(x_beliefunit, moment_epoch_label, 0)
    x_beliefEpochTime.calc_epoch()
    return x_beliefEpochTime
