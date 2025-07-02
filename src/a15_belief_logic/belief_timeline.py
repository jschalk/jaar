from src.a01_term_logic.rope import create_rope
from src.a06_owner_logic.owner import OwnerUnit, ownerunit_shop
from src.a07_timeline_logic.timeline import (
    OwnerTimelinePoint,
    add_newtimeline_planunit,
    get_timeline_rope,
    ownertimelinepoint_shop,
    timeline_config_shop,
)
from src.a15_belief_logic.belief import BeliefUnit


def get_belief_ownertimelinepoint(beliefunit: BeliefUnit) -> OwnerTimelinePoint:
    """Returns OwnerTimelinePoint from BeliefUnit attributes."""
    beliefunit.set_offi_time_max(0)
    # create empty ownerunit
    x_ownerunit = ownerunit_shop(
        owner_name="for_ownertimelinepoint_calculation",
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
    add_newtimeline_planunit(x_ownerunit, belief_timeline_config)
    x_ownertimelinepoint = ownertimelinepoint_shop(x_ownerunit, timeline_rope, 0)
    x_ownertimelinepoint.calc_timeline()
    return x_ownertimelinepoint
