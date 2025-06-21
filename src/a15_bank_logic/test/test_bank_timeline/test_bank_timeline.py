from src.a06_plan_logic.plan import planunit_shop
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_conceptunit,
    get_creg_config,
)
from src.a07_timeline_logic.timeline import plantimelinepoint_shop, timelineunit_shop
from src.a15_bank_logic.bank import bankunit_shop
from src.a15_bank_logic.bank_timeline import get_bank_plantimelinepoint
from src.a15_bank_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_get_bank_plantimelinepoint_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    fizz_str = "fizz"
    fizz_bankunit = bankunit_shop(fizz_str, get_module_temp_dir())
    assert fizz_bankunit.timeline == timelineunit_shop(get_creg_config())
    assert not fizz_bankunit._offi_time_max

    # WHEN
    fizz_plantimelinepoint = get_bank_plantimelinepoint(fizz_bankunit)

    # THEN
    assert fizz_bankunit._offi_time_max == 0
    assert fizz_plantimelinepoint.x_min == 0

    assert fizz_plantimelinepoint
    # assert fizz_plantimelinepoint.x_min == fizz_offi_time_max
    fizz_planunit = fizz_plantimelinepoint.x_planunit
    assert fizz_planunit.owner_name == "for_plantimelinepoint_calculation"
    assert fizz_planunit.bank_label == fizz_bankunit.bank_label
    assert fizz_planunit.knot == fizz_bankunit.knot
    assert fizz_planunit.fund_iota == fizz_bankunit.fund_iota
    assert fizz_planunit.respect_bit == fizz_bankunit.respect_bit
    assert fizz_planunit.penny == fizz_bankunit.penny
    assert fizz_planunit.bank_label == fizz_bankunit.bank_label
    assert fizz_plantimelinepoint._month == "March"
    assert fizz_plantimelinepoint._hour == "0-12am"
    assert fizz_plantimelinepoint._minute == 0
    assert fizz_plantimelinepoint._monthday == 1
    assert fizz_plantimelinepoint._c400_number == 0
    assert fizz_plantimelinepoint._year_num == 0


# def test_get_bank_plantimelinepoint_ReturnsObj_Scenario1_BankUnit_NonDefaultAttrs():
#     # ESTABLISH
#     fizz_str = "fizz"
#     slash_str = "/"
#     fizz_fund_iota = 5
#     fizz_respect_bit = 3
#     fizz_penny = 7
#     fizz_bankunit = bankunit_shop(
#         fizz_str,
#         get_module_temp_dir(),
#         knot=slash_str,
#         fund_iota=fizz_fund_iota,
#         respect_bit=fizz_respect_bit,
#         penny=fizz_penny,
#     )
#     assert fizz_bankunit.timeline == timelineunit_shop(get_creg_config())
#     assert not fizz_bankunit._offi_time_max

#     # WHEN
#     fizz_plantimelinepoint = get_bank_plantimelinepoint(fizz_bankunit)

#     # THEN
#     assert fizz_bankunit._offi_time_max == 0
#     assert fizz_plantimelinepoint.x_min == 0

#     assert fizz_plantimelinepoint
#     # assert fizz_plantimelinepoint.x_min == fizz_offi_time_max
#     fizz_planunit = fizz_plantimelinepoint.x_planunit
#     assert fizz_planunit.owner_name == "for_plantimelinepoint_calculation"
#     assert fizz_planunit.bank_label == fizz_bankunit.bank_label
#     assert fizz_planunit.knot == fizz_bankunit.knot
#     assert fizz_planunit.fund_iota == fizz_bankunit.fund_iota
#     assert fizz_planunit.respect_bit == fizz_bankunit.respect_bit
#     assert fizz_planunit.penny == fizz_bankunit.penny
#     assert fizz_planunit.bank_label == fizz_bankunit.bank_label
#     assert fizz_plantimelinepoint._month == "March"
#     assert fizz_plantimelinepoint._hour == 0
#     assert fizz_plantimelinepoint._minute == 0
#     assert fizz_plantimelinepoint._monthday == 1
#     assert fizz_plantimelinepoint._c400_number == 0
#     assert fizz_plantimelinepoint._year_num == 0
#     #  planunit_shop()
#     #  plantimelinepoint_shop()
#     assert 1 == 2
