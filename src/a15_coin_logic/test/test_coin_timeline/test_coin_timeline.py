from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_planunit,
    get_creg_config,
)
from src.a07_timeline_logic.timeline_main import (
    belieftimelinepoint_shop,
    timelineunit_shop,
)
from src.a15_coin_logic.coin_main import coinunit_shop
from src.a15_coin_logic.coin_timeline import get_coin_belieftimelinepoint
from src.a15_coin_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_get_coin_belieftimelinepoint_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    fay_str = "Fay"
    fay_coinunit = coinunit_shop(fay_str, get_module_temp_dir())
    assert fay_coinunit.timeline == timelineunit_shop(get_creg_config())
    assert not fay_coinunit._offi_time_max

    # WHEN
    fay_belieftimelinepoint = get_coin_belieftimelinepoint(fay_coinunit)

    # THEN
    assert fay_coinunit._offi_time_max == 0
    assert fay_belieftimelinepoint.x_min == 0

    assert fay_belieftimelinepoint
    # assert fay_belieftimelinepoint.x_min == fay_offi_time_max
    fay_beliefunit = fay_belieftimelinepoint.x_beliefunit
    assert fay_beliefunit.belief_name == "for_belieftimelinepoint_calculation"
    assert fay_beliefunit.coin_label == fay_coinunit.coin_label
    assert fay_beliefunit.knot == fay_coinunit.knot
    assert fay_beliefunit.fund_iota == fay_coinunit.fund_iota
    assert fay_beliefunit.respect_bit == fay_coinunit.respect_bit
    assert fay_beliefunit.penny == fay_coinunit.penny
    assert fay_belieftimelinepoint._month == "March"
    assert fay_belieftimelinepoint._hour == "12am"
    assert fay_belieftimelinepoint._minute == 0
    assert fay_belieftimelinepoint._monthday == 1
    assert fay_belieftimelinepoint._c400_number == 0
    assert fay_belieftimelinepoint._year_num == 0


def test_get_coin_belieftimelinepoint_ReturnsObj_Scenario1_CoinUnit_NonDefaultAttrs():
    # ESTABLISH
    fay_str = "Fay"
    slash_str = "/"
    fay_fund_iota = 5
    fay_respect_bit = 4
    fay_penny = 7
    fay_coinunit = coinunit_shop(
        fay_str,
        get_module_temp_dir(),
        knot=slash_str,
        fund_iota=fay_fund_iota,
        respect_bit=fay_respect_bit,
        penny=fay_penny,
    )
    assert fay_coinunit.timeline == timelineunit_shop(get_creg_config())
    assert not fay_coinunit._offi_time_max

    # WHEN
    fay_belieftimelinepoint = get_coin_belieftimelinepoint(fay_coinunit)

    # THEN
    assert fay_coinunit._offi_time_max == 0
    assert fay_belieftimelinepoint.x_min == 0

    assert fay_belieftimelinepoint
    # assert fay_belieftimelinepoint.x_min == fay_offi_time_max
    fay_beliefunit = fay_belieftimelinepoint.x_beliefunit
    assert fay_beliefunit.belief_name == "for_belieftimelinepoint_calculation"
    assert fay_beliefunit.coin_label == fay_coinunit.coin_label
    assert fay_beliefunit.knot == fay_coinunit.knot
    assert fay_beliefunit.fund_iota == fay_coinunit.fund_iota
    assert fay_beliefunit.respect_bit == fay_coinunit.respect_bit
    assert fay_beliefunit.penny == fay_coinunit.penny
    assert fay_belieftimelinepoint._month == "March"
    assert fay_belieftimelinepoint._hour == "12am"
    assert fay_belieftimelinepoint._minute == 0
    assert fay_belieftimelinepoint._monthday == 1
    assert fay_belieftimelinepoint._c400_number == 0
    assert fay_belieftimelinepoint._year_num == 0
    #  beliefunit_shop()
    #  belieftimelinepoint_shop()
