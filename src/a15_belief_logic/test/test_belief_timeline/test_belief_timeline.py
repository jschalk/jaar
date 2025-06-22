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
    fizz_str = "fizz"
    fizz_beliefunit = beliefunit_shop(fizz_str, get_module_temp_dir())
    assert fizz_beliefunit.timeline == timelineunit_shop(get_creg_config())
    assert not fizz_beliefunit._offi_time_max

    # WHEN
    fizz_plantimelinepoint = get_belief_plantimelinepoint(fizz_beliefunit)

    # THEN
    assert fizz_beliefunit._offi_time_max == 0
    assert fizz_plantimelinepoint.x_min == 0

    assert fizz_plantimelinepoint
    # assert fizz_plantimelinepoint.x_min == fizz_offi_time_max
    fizz_planunit = fizz_plantimelinepoint.x_planunit
    assert fizz_planunit.owner_name == "for_plantimelinepoint_calculation"
    assert fizz_planunit.belief_label == fizz_beliefunit.belief_label
    assert fizz_planunit.knot == fizz_beliefunit.knot
    assert fizz_planunit.fund_iota == fizz_beliefunit.fund_iota
    assert fizz_planunit.respect_bit == fizz_beliefunit.respect_bit
    assert fizz_planunit.penny == fizz_beliefunit.penny
    assert fizz_plantimelinepoint._month == "March"
    assert fizz_plantimelinepoint._hour == "0-12am"
    assert fizz_plantimelinepoint._minute == 0
    assert fizz_plantimelinepoint._monthday == 1
    assert fizz_plantimelinepoint._c400_number == 0
    assert fizz_plantimelinepoint._year_num == 0


def test_get_belief_plantimelinepoint_ReturnsObj_Scenario1_BeliefUnit_NonDefaultAttrs():
    # ESTABLISH
    fizz_str = "fizz"
    slash_str = "/"
    fizz_fund_iota = 5
    fizz_respect_bit = 4
    fizz_penny = 7
    fizz_beliefunit = beliefunit_shop(
        fizz_str,
        get_module_temp_dir(),
        knot=slash_str,
        fund_iota=fizz_fund_iota,
        respect_bit=fizz_respect_bit,
        penny=fizz_penny,
    )
    assert fizz_beliefunit.timeline == timelineunit_shop(get_creg_config())
    assert not fizz_beliefunit._offi_time_max

    # WHEN
    fizz_plantimelinepoint = get_belief_plantimelinepoint(fizz_beliefunit)

    # THEN
    assert fizz_beliefunit._offi_time_max == 0
    assert fizz_plantimelinepoint.x_min == 0

    assert fizz_plantimelinepoint
    # assert fizz_plantimelinepoint.x_min == fizz_offi_time_max
    fizz_planunit = fizz_plantimelinepoint.x_planunit
    assert fizz_planunit.owner_name == "for_plantimelinepoint_calculation"
    assert fizz_planunit.belief_label == fizz_beliefunit.belief_label
    assert fizz_planunit.knot == fizz_beliefunit.knot
    assert fizz_planunit.fund_iota == fizz_beliefunit.fund_iota
    assert fizz_planunit.respect_bit == fizz_beliefunit.respect_bit
    assert fizz_planunit.penny == fizz_beliefunit.penny
    assert fizz_plantimelinepoint._month == "March"
    assert fizz_plantimelinepoint._hour == "0-12am"
    assert fizz_plantimelinepoint._minute == 0
    assert fizz_plantimelinepoint._monthday == 1
    assert fizz_plantimelinepoint._c400_number == 0
    assert fizz_plantimelinepoint._year_num == 0
    #  planunit_shop()
    #  plantimelinepoint_shop()
