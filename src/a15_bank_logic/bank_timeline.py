from src.a01_term_logic.rope import create_rope
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a07_timeline_logic.timeline import (
    PlanTimelinePoint,
    add_newtimeline_conceptunit,
    get_timeline_rope,
    plantimelinepoint_shop,
    timeline_config_shop,
)
from src.a15_bank_logic.bank import BankUnit


def get_bank_plantimelinepoint(bankunit: BankUnit) -> PlanTimelinePoint:
    """Returns PlanTimelinePoint from BankUnit attributes."""
    bankunit.set_offi_time_max(0)
    # create empty planunit
    x_planunit = planunit_shop(
        owner_name="for_plantimelinepoint_calculation",
        bank_label=bankunit.bank_label,
        knot=bankunit.knot,
    )
    timeline_rope = get_timeline_rope(
        bank_label=bankunit.bank_label,
        timeline_label=bankunit.timeline.timeline_label,
        knot=bankunit.knot,
    )
    bank_timeline_config = bankunit.timeline.get_dict()
    # create timeline concept from bankunit.timeline_config
    add_newtimeline_conceptunit(x_planunit, bank_timeline_config)
    x_plantimelinepoint = plantimelinepoint_shop(x_planunit, timeline_rope, 0)
    x_plantimelinepoint.calc_timeline()
    return x_plantimelinepoint
