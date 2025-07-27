from src.a06_believer_logic.believer_main import believerunit_shop
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_planunit,
    get_creg_config,
)
from src.a07_timeline_logic.timeline_main import (
    believertimelinepoint_shop,
    timelineunit_shop,
)
from src.a15_belief_logic.belief import beliefunit_shop
from src.a15_belief_logic.belief_timeline import get_belief_believertimelinepoint
from src.a15_belief_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_get_belief_believertimelinepoint_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    fay_str = "Fay"
    fay_beliefunit = beliefunit_shop(fay_str, get_module_temp_dir())
    assert fay_beliefunit.timeline == timelineunit_shop(get_creg_config())
    assert not fay_beliefunit._offi_time_max

    # WHEN
    fay_believertimelinepoint = get_belief_believertimelinepoint(fay_beliefunit)

    # THEN
    assert fay_beliefunit._offi_time_max == 0
    assert fay_believertimelinepoint.x_min == 0

    assert fay_believertimelinepoint
    # assert fay_believertimelinepoint.x_min == fay_offi_time_max
    fay_believerunit = fay_believertimelinepoint.x_believerunit
    assert fay_believerunit.believer_name == "for_believertimelinepoint_calculation"
    assert fay_believerunit.belief_label == fay_beliefunit.belief_label
    assert fay_believerunit.knot == fay_beliefunit.knot
    assert fay_believerunit.fund_iota == fay_beliefunit.fund_iota
    assert fay_believerunit.respect_bit == fay_beliefunit.respect_bit
    assert fay_believerunit.penny == fay_beliefunit.penny
    assert fay_believertimelinepoint._month == "March"
    assert fay_believertimelinepoint._hour == "0-12am"
    assert fay_believertimelinepoint._minute == 0
    assert fay_believertimelinepoint._monthday == 1
    assert fay_believertimelinepoint._c400_number == 0
    assert fay_believertimelinepoint._year_num == 0


def test_get_belief_believertimelinepoint_ReturnsObj_Scenario1_BeliefUnit_NonDefaultAttrs():
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
    fay_believertimelinepoint = get_belief_believertimelinepoint(fay_beliefunit)

    # THEN
    assert fay_beliefunit._offi_time_max == 0
    assert fay_believertimelinepoint.x_min == 0

    assert fay_believertimelinepoint
    # assert fay_believertimelinepoint.x_min == fay_offi_time_max
    fay_believerunit = fay_believertimelinepoint.x_believerunit
    assert fay_believerunit.believer_name == "for_believertimelinepoint_calculation"
    assert fay_believerunit.belief_label == fay_beliefunit.belief_label
    assert fay_believerunit.knot == fay_beliefunit.knot
    assert fay_believerunit.fund_iota == fay_beliefunit.fund_iota
    assert fay_believerunit.respect_bit == fay_beliefunit.respect_bit
    assert fay_believerunit.penny == fay_beliefunit.penny
    assert fay_believertimelinepoint._month == "March"
    assert fay_believertimelinepoint._hour == "0-12am"
    assert fay_believertimelinepoint._minute == 0
    assert fay_believertimelinepoint._monthday == 1
    assert fay_believertimelinepoint._c400_number == 0
    assert fay_believertimelinepoint._year_num == 0
    #  believerunit_shop()
    #  believertimelinepoint_shop()
