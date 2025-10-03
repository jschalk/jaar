from src.ch08_timeline_logic.test._util.ch08_examples import get_creg_config
from src.ch08_timeline_logic.timeline_main import timelineunit_shop
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch15_moment_logic.moment_timeline import get_moment_belieftimelinepoint
from src.ch15_moment_logic.test._util.ch15_env import get_chapter_temp_dir


def test_get_moment_belieftimelinepoint_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    fay_str = "Fay"
    fay_momentunit = momentunit_shop(fay_str, get_chapter_temp_dir())
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
    assert fay_beliefunit.fund_grain == fay_momentunit.fund_grain
    assert fay_beliefunit.respect_grain == fay_momentunit.respect_grain
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
    fay_fund_grain = 5
    fay_respect_grain = 4
    fay_penny = 7
    fay_momentunit = momentunit_shop(
        fay_str,
        get_chapter_temp_dir(),
        knot=slash_str,
        fund_grain=fay_fund_grain,
        respect_grain=fay_respect_grain,
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
    assert fay_beliefunit.fund_grain == fay_momentunit.fund_grain
    assert fay_beliefunit.respect_grain == fay_momentunit.respect_grain
    assert fay_beliefunit.penny == fay_momentunit.penny
    assert fay_belieftimelinepoint._month == "March"
    assert fay_belieftimelinepoint._hour == "12am"
    assert fay_belieftimelinepoint._minute == 0
    assert fay_belieftimelinepoint._monthday == 1
    assert fay_belieftimelinepoint._c400_number == 0
    assert fay_belieftimelinepoint._year_num == 0
    #  beliefunit_shop()
    #  belieftimelinepoint_shop()
