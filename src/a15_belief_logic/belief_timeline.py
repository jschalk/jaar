from src.a01_term_logic.rope import create_rope
from src.a06_believer_logic.believer_main import BelieverUnit, believerunit_shop
from src.a07_timeline_logic.timeline_main import (
    BelieverTimelinePoint,
    add_newtimeline_planunit,
    believertimelinepoint_shop,
    get_timeline_rope,
    timeline_config_shop,
)
from src.a15_belief_logic.belief_main import BeliefUnit


def get_belief_believertimelinepoint(beliefunit: BeliefUnit) -> BelieverTimelinePoint:
    """Returns BelieverTimelinePoint from BeliefUnit attributes."""
    beliefunit.set_offi_time_max(0)
    # create empty believerunit
    x_believerunit = believerunit_shop(
        believer_name="for_believertimelinepoint_calculation",
        belief_label=beliefunit.belief_label,
        knot=beliefunit.knot,
        fund_iota=beliefunit.fund_iota,
        respect_bit=beliefunit.respect_bit,
        penny=beliefunit.penny,
    )
    timeline_rope = get_timeline_rope(
        belief_label=beliefunit.belief_label,
        timeline_label=beliefunit.timeline.timeline_label,
        knot=beliefunit.knot,
    )
    belief_timeline_config = beliefunit.timeline.get_dict()
    # create timeline plan from beliefunit.timeline_config
    add_newtimeline_planunit(x_believerunit, belief_timeline_config)
    x_believertimelinepoint = believertimelinepoint_shop(
        x_believerunit, timeline_rope, 0
    )
    x_believertimelinepoint.calc_timeline()
    return x_believertimelinepoint
