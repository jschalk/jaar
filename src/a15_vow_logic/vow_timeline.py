from src.a01_term_logic.rope import create_rope
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a07_timeline_logic.timeline import (
    PlanTimelinePoint,
    add_newtimeline_conceptunit,
    get_timeline_rope,
    plantimelinepoint_shop,
    timeline_config_shop,
)
from src.a15_vow_logic.vow import VowUnit


def get_vow_plantimelinepoint(vowunit: VowUnit) -> PlanTimelinePoint:
    """Returns PlanTimelinePoint from VowUnit attributes."""
    vowunit.set_offi_time_max(0)
    # create empty planunit
    x_planunit = planunit_shop(
        owner_name="for_plantimelinepoint_calculation",
        vow_label=vowunit.vow_label,
        knot=vowunit.knot,
    )
    timeline_rope = get_timeline_rope(
        vow_label=vowunit.vow_label,
        timeline_label=vowunit.timeline.timeline_label,
        knot=vowunit.knot,
    )
    vow_timeline_config = vowunit.timeline.get_dict()
    # create timeline concept from vowunit.timeline_config
    add_newtimeline_conceptunit(x_planunit, vow_timeline_config)
    x_plantimelinepoint = plantimelinepoint_shop(x_planunit, timeline_rope, 0)
    x_plantimelinepoint.calc_timeline()
    return x_plantimelinepoint
