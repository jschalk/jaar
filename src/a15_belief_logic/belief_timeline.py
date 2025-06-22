from src.a01_term_logic.rope import create_rope
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a07_timeline_logic.timeline import (
    PlanTimelinePoint,
    add_newtimeline_conceptunit,
    get_timeline_rope,
    plantimelinepoint_shop,
    timeline_config_shop,
)
from src.a15_belief_logic.belief import BeliefUnit


def get_belief_plantimelinepoint(beliefunit: BeliefUnit) -> PlanTimelinePoint:
    """Returns PlanTimelinePoint from BeliefUnit attributes."""
    beliefunit.set_offi_time_max(0)
    # create empty planunit
    x_planunit = planunit_shop(
        owner_name="for_plantimelinepoint_calculation",
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
    # create timeline concept from beliefunit.timeline_config
    add_newtimeline_conceptunit(x_planunit, belief_timeline_config)
    x_plantimelinepoint = plantimelinepoint_shop(x_planunit, timeline_rope, 0)
    x_plantimelinepoint.calc_timeline()
    return x_plantimelinepoint
