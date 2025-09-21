from src.a01_rope_logic.rope import create_rope
from src.a06_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.a07_timeline_logic.timeline_main import (
    BeliefTimelinePoint,
    add_newtimeline_planunit,
    belieftimelinepoint_shop,
    get_timeline_rope,
    timeline_config_shop,
)
from src.ch15_moment_logic.moment_main import MomentUnit


def get_moment_belieftimelinepoint(momentunit: MomentUnit) -> BeliefTimelinePoint:
    """Returns BeliefTimelinePoint from MomentUnit attributes."""
    momentunit.set_offi_time_max(0)
    # create empty beliefunit
    x_beliefunit = beliefunit_shop(
        belief_name="for_belieftimelinepoint_calculation",
        moment_label=momentunit.moment_label,
        knot=momentunit.knot,
        fund_iota=momentunit.fund_iota,
        respect_bit=momentunit.respect_bit,
        penny=momentunit.penny,
    )
    timeline_rope = get_timeline_rope(
        moment_label=momentunit.moment_label,
        timeline_label=momentunit.timeline.timeline_label,
        knot=momentunit.knot,
    )
    moment_timeline_config = momentunit.timeline.to_dict()
    # create timeline plan from momentunit.timeline_config
    add_newtimeline_planunit(x_beliefunit, moment_timeline_config)
    x_belieftimelinepoint = belieftimelinepoint_shop(x_beliefunit, timeline_rope, 0)
    x_belieftimelinepoint.calc_timeline()
    return x_belieftimelinepoint
