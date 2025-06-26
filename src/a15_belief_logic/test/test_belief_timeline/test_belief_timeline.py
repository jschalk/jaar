from src.a06_plan_logic.plan import planunit_shop
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_conceptunit,
    get_creg_config,
)
from src.a07_timeline_logic.timeline import plantimelinepoint_shop, timelineunit_shop
from src.a15_belief_logic.belief import beliefunit_shop
from src.a15_belief_logic.belief_timeline import get_belief_plantimelinepoint
from src.a15_belief_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_get_belief_plantimelinepoint_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    fay_str = "Fay"
    fay_beliefunit = beliefunit_shop(fay_str, get_module_temp_dir())
    assert fay_beliefunit.timeline == timelineunit_shop(get_creg_config())
    assert not fay_beliefunit._offi_time_max

    # WHEN
    fay_plantimelinepoint = get_belief_plantimelinepoint(fay_beliefunit)

    # THEN
    assert fay_beliefunit._offi_time_max == 0
    assert fay_plantimelinepoint.x_min == 0

    assert fay_plantimelinepoint
    # assert fay_plantimelinepoint.x_min == fay_offi_time_max
    fay_planunit = fay_plantimelinepoint.x_planunit
    assert fay_planunit.owner_name == "for_plantimelinepoint_calculation"
    assert fay_planunit.belief_label == fay_beliefunit.belief_label
    assert fay_planunit.knot == fay_beliefunit.knot
    assert fay_planunit.fund_iota == fay_beliefunit.fund_iota
    assert fay_planunit.respect_bit == fay_beliefunit.respect_bit
    assert fay_planunit.penny == fay_beliefunit.penny
    assert fay_plantimelinepoint._month == "March"
    assert fay_plantimelinepoint._hour == "0-12am"
    assert fay_plantimelinepoint._minute == 0
    assert fay_plantimelinepoint._monthday == 1
    assert fay_plantimelinepoint._c400_number == 0
    assert fay_plantimelinepoint._year_num == 0


def test_get_belief_plantimelinepoint_ReturnsObj_Scenario1_BeliefUnit_NonDefaultAttrs():
    # ESTABLISH
    fay_str = "Fay"
    slash_str = "/"
    fay_fund_iota = 5
    fay_respect_bit = 4
    fay_penny = 7
    fay_beliefunit = beliefunit_shop(
        fay_str,
        get_module_temp_dir(),
        knot=slash_str,
        fund_iota=fay_fund_iota,
        respect_bit=fay_respect_bit,
        penny=fay_penny,
    )
    assert fay_beliefunit.timeline == timelineunit_shop(get_creg_config())
    assert not fay_beliefunit._offi_time_max

    # WHEN
    fay_plantimelinepoint = get_belief_plantimelinepoint(fay_beliefunit)

    # THEN
    assert fay_beliefunit._offi_time_max == 0
    assert fay_plantimelinepoint.x_min == 0

    assert fay_plantimelinepoint
    # assert fay_plantimelinepoint.x_min == fay_offi_time_max
    fay_planunit = fay_plantimelinepoint.x_planunit
    assert fay_planunit.owner_name == "for_plantimelinepoint_calculation"
    assert fay_planunit.belief_label == fay_beliefunit.belief_label
    assert fay_planunit.knot == fay_beliefunit.knot
    assert fay_planunit.fund_iota == fay_beliefunit.fund_iota
    assert fay_planunit.respect_bit == fay_beliefunit.respect_bit
    assert fay_planunit.penny == fay_beliefunit.penny
    assert fay_plantimelinepoint._month == "March"
    assert fay_plantimelinepoint._hour == "0-12am"
    assert fay_plantimelinepoint._minute == 0
    assert fay_plantimelinepoint._monthday == 1
    assert fay_plantimelinepoint._c400_number == 0
    assert fay_plantimelinepoint._year_num == 0
    #  planunit_shop()
    #  plantimelinepoint_shop()
