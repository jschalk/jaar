from src.ch08_epoch.epoch_main import epochunit_shop
from src.ch08_epoch.test._util.ch08_examples import get_creg_config
from src.ch15_moment.moment_epoch import get_moment_beliefEpochInstant
from src.ch15_moment.moment_main import momentunit_shop
from src.ch15_moment.test._util.ch15_env import get_temp_dir


def test_get_moment_beliefEpochInstant_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    fay_str = "Fay"
    fay_momentunit = momentunit_shop(fay_str, get_temp_dir())
    assert fay_momentunit.epoch == epochunit_shop(get_creg_config())
    assert not fay_momentunit.offi_time_max

    # WHEN
    fay_beliefEpochInstant = get_moment_beliefEpochInstant(fay_momentunit)

    # THEN
    assert fay_momentunit.offi_time_max == 0
    assert fay_beliefEpochInstant.x_min == 0

    assert fay_beliefEpochInstant
    # assert fay_beliefEpochInstant.x_min == fay_offi_time_max
    fay_beliefunit = fay_beliefEpochInstant.x_beliefunit
    assert fay_beliefunit.belief_name == "for_beliefEpochInstant_calculation"
    assert fay_beliefunit.moment_label == fay_momentunit.moment_label
    assert fay_beliefunit.knot == fay_momentunit.knot
    assert fay_beliefunit.fund_grain == fay_momentunit.fund_grain
    assert fay_beliefunit.respect_grain == fay_momentunit.respect_grain
    assert fay_beliefunit.mana_grain == fay_momentunit.mana_grain
    assert fay_beliefEpochInstant._month == "March"
    assert fay_beliefEpochInstant._hour == "12am"
    assert fay_beliefEpochInstant._minute == 0
    assert fay_beliefEpochInstant._monthday == 1
    assert fay_beliefEpochInstant._c400_number == 0
    assert fay_beliefEpochInstant._year_num == 0


def test_get_moment_beliefEpochInstant_ReturnsObj_Scenario1_MomentUnit_NonDefaultAttrs():
    # ESTABLISH
    fay_str = "Fay"
    slash_str = "/"
    fay_fund_grain = 5
    fay_respect_grain = 4
    fay_mana_grain = 7
    fay_momentunit = momentunit_shop(
        fay_str,
        get_temp_dir(),
        knot=slash_str,
        fund_grain=fay_fund_grain,
        respect_grain=fay_respect_grain,
        mana_grain=fay_mana_grain,
    )
    assert fay_momentunit.epoch == epochunit_shop(get_creg_config())
    assert not fay_momentunit.offi_time_max

    # WHEN
    fay_beliefEpochInstant = get_moment_beliefEpochInstant(fay_momentunit)

    # THEN
    assert fay_momentunit.offi_time_max == 0
    assert fay_beliefEpochInstant.x_min == 0

    assert fay_beliefEpochInstant
    # assert fay_beliefEpochInstant.x_min == fay_offi_time_max
    fay_beliefunit = fay_beliefEpochInstant.x_beliefunit
    assert fay_beliefunit.belief_name == "for_beliefEpochInstant_calculation"
    assert fay_beliefunit.moment_label == fay_momentunit.moment_label
    assert fay_beliefunit.knot == fay_momentunit.knot
    assert fay_beliefunit.fund_grain == fay_momentunit.fund_grain
    assert fay_beliefunit.respect_grain == fay_momentunit.respect_grain
    assert fay_beliefunit.mana_grain == fay_momentunit.mana_grain
    assert fay_beliefEpochInstant._month == "March"
    assert fay_beliefEpochInstant._hour == "12am"
    assert fay_beliefEpochInstant._minute == 0
    assert fay_beliefEpochInstant._monthday == 1
    assert fay_beliefEpochInstant._c400_number == 0
    assert fay_beliefEpochInstant._year_num == 0
    #  beliefunit_shop()
    #  beliefEpochInstant_shop()
