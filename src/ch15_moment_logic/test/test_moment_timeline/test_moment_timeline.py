from src.ch06_belief_logic.belief_main import beliefunit_shop
from src.ch07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_planunit,
    get_creg_config,
)
from src.ch07_timeline_logic.timeline_main import (
    belieftimelinepoint_shop,
    timelineunit_shop,
)
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch15_moment_logic.moment_timeline import get_moment_belieftimelinepoint
from src.ch15_moment_logic.test._util.ch15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_get_moment_belieftimelinepoint_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    fay_str = "Fay"
    fay_momentunit = momentunit_shop(fay_str, get_module_temp_dir())
    assert fay_momentunit.timeline == timelineunit_shop(get_creg_config())
    assert not fay_momentunit._offi_time_max

    # WHEN
    fay_belieftimelinepoint = get_moment_belieftimelinepoint(fay_momentunit)

    # THEN
    assert fay_momentunit._offi_time_max == 0
    assert fay_belieftimelinepoint.x_min == 0

    assert fay_belieftimelinepoint
    # assert fay_belieftimelinepoint.x_min == fay_offi_time_max
    fay_beliefunit = fay_belieftimelinepoint.x_beliefunit
    assert fay_beliefunit.belief_name == "for_belieftimelinepoint_calculation"
    assert fay_beliefunit.moment_label == fay_momentunit.moment_label
    assert fay_beliefunit.knot == fay_momentunit.knot
    assert fay_beliefunit.fund_iota == fay_momentunit.fund_iota
    assert fay_beliefunit.respect_bit == fay_momentunit.respect_bit
    assert fay_beliefunit.penny == fay_momentunit.penny
    assert fay_belieftimelinepoint._month == "March"
    assert fay_belieftimelinepoint._hour == "12am"
    assert fay_belieftimelinepoint._minute == 0
    assert fay_belieftimelinepoint._monthday == 1
    assert fay_belieftimelinepoint._c400_number == 0
    assert fay_belieftimelinepoint._year_num == 0


def test_get_moment_belieftimelinepoint_ReturnsObj_Scenario1_MomentUnit_NonDefaultAttrs():
    # ESTABLISH
    fay_str = "Fay"
    slash_str = "/"
    fay_fund_iota = 5
    fay_respect_bit = 4
    fay_penny = 7
    fay_momentunit = momentunit_shop(
        fay_str,
        get_module_temp_dir(),
        knot=slash_str,
        fund_iota=fay_fund_iota,
        respect_bit=fay_respect_bit,
        penny=fay_penny,
    )
    assert fay_momentunit.timeline == timelineunit_shop(get_creg_config())
    assert not fay_momentunit._offi_time_max

    # WHEN
    fay_belieftimelinepoint = get_moment_belieftimelinepoint(fay_momentunit)

    # THEN
    assert fay_momentunit._offi_time_max == 0
    assert fay_belieftimelinepoint.x_min == 0

    assert fay_belieftimelinepoint
    # assert fay_belieftimelinepoint.x_min == fay_offi_time_max
    fay_beliefunit = fay_belieftimelinepoint.x_beliefunit
    assert fay_beliefunit.belief_name == "for_belieftimelinepoint_calculation"
    assert fay_beliefunit.moment_label == fay_momentunit.moment_label
    assert fay_beliefunit.knot == fay_momentunit.knot
    assert fay_beliefunit.fund_iota == fay_momentunit.fund_iota
    assert fay_beliefunit.respect_bit == fay_momentunit.respect_bit
    assert fay_beliefunit.penny == fay_momentunit.penny
    assert fay_belieftimelinepoint._month == "March"
    assert fay_belieftimelinepoint._hour == "12am"
    assert fay_belieftimelinepoint._minute == 0
    assert fay_belieftimelinepoint._monthday == 1
    assert fay_belieftimelinepoint._c400_number == 0
    assert fay_belieftimelinepoint._year_num == 0
    #  beliefunit_shop()
    #  belieftimelinepoint_shop()
