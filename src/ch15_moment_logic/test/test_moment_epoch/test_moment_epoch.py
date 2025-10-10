from src.ch08_epoch_logic.epoch_main import epochunit_shop
from src.ch08_epoch_logic.test._util.ch08_examples import get_creg_config
from src.ch15_moment_logic.moment_epoch import get_moment_beliefepochpoint
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch15_moment_logic.test._util.ch15_env import get_chapter_temp_dir


def test_get_moment_beliefepochpoint_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    fay_str = "Fay"
    fay_momentunit = momentunit_shop(fay_str, get_chapter_temp_dir())
    assert fay_momentunit.epoch == epochunit_shop(get_creg_config())
    assert not fay_momentunit._offi_time_max

    # WHEN
    fay_beliefepochpoint = get_moment_beliefepochpoint(fay_momentunit)

    # THEN
    assert fay_momentunit._offi_time_max == 0
    assert fay_beliefepochpoint.x_min == 0

    assert fay_beliefepochpoint
    # assert fay_beliefepochpoint.x_min == fay_offi_time_max
    fay_beliefunit = fay_beliefepochpoint.x_beliefunit
    assert fay_beliefunit.belief_name == "for_beliefepochpoint_calculation"
    assert fay_beliefunit.moment_label == fay_momentunit.moment_label
    assert fay_beliefunit.knot == fay_momentunit.knot
    assert fay_beliefunit.fund_grain == fay_momentunit.fund_grain
    assert fay_beliefunit.respect_grain == fay_momentunit.respect_grain
    assert fay_beliefunit.money_grain == fay_momentunit.money_grain
    assert fay_beliefepochpoint._month == "March"
    assert fay_beliefepochpoint._hour == "12am"
    assert fay_beliefepochpoint._minute == 0
    assert fay_beliefepochpoint._monthday == 1
    assert fay_beliefepochpoint._c400_number == 0
    assert fay_beliefepochpoint._year_num == 0


def test_get_moment_beliefepochpoint_ReturnsObj_Scenario1_MomentUnit_NonDefaultAttrs():
    # ESTABLISH
    fay_str = "Fay"
    slash_str = "/"
    fay_fund_grain = 5
    fay_respect_grain = 4
    fay_money_grain = 7
    fay_momentunit = momentunit_shop(
        fay_str,
        get_chapter_temp_dir(),
        knot=slash_str,
        fund_grain=fay_fund_grain,
        respect_grain=fay_respect_grain,
        money_grain=fay_money_grain,
    )
    assert fay_momentunit.epoch == epochunit_shop(get_creg_config())
    assert not fay_momentunit._offi_time_max

    # WHEN
    fay_beliefepochpoint = get_moment_beliefepochpoint(fay_momentunit)

    # THEN
    assert fay_momentunit._offi_time_max == 0
    assert fay_beliefepochpoint.x_min == 0

    assert fay_beliefepochpoint
    # assert fay_beliefepochpoint.x_min == fay_offi_time_max
    fay_beliefunit = fay_beliefepochpoint.x_beliefunit
    assert fay_beliefunit.belief_name == "for_beliefepochpoint_calculation"
    assert fay_beliefunit.moment_label == fay_momentunit.moment_label
    assert fay_beliefunit.knot == fay_momentunit.knot
    assert fay_beliefunit.fund_grain == fay_momentunit.fund_grain
    assert fay_beliefunit.respect_grain == fay_momentunit.respect_grain
    assert fay_beliefunit.money_grain == fay_momentunit.money_grain
    assert fay_beliefepochpoint._month == "March"
    assert fay_beliefepochpoint._hour == "12am"
    assert fay_beliefepochpoint._minute == 0
    assert fay_beliefepochpoint._monthday == 1
    assert fay_beliefepochpoint._c400_number == 0
    assert fay_beliefepochpoint._year_num == 0
    #  beliefunit_shop()
    #  beliefepochpoint_shop()
