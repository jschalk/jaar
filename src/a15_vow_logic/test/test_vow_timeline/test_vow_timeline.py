from src.a06_plan_logic.plan import planunit_shop
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_conceptunit,
    get_creg_config,
)
from src.a07_timeline_logic.timeline import plantimelinepoint_shop, timelineunit_shop
from src.a15_vow_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_vow_logic.vow import vowunit_shop
from src.a15_vow_logic.vow_timeline import get_vow_plantimelinepoint


def test_get_vow_plantimelinepoint_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    fizz_str = "fizz"
    fizz_vowunit = vowunit_shop(fizz_str, get_module_temp_dir())
    assert fizz_vowunit.timeline == timelineunit_shop(get_creg_config())
    assert not fizz_vowunit._offi_time_max

    # WHEN
    fizz_plantimelinepoint = get_vow_plantimelinepoint(fizz_vowunit)

    # THEN
    assert fizz_vowunit._offi_time_max == 0
    assert fizz_plantimelinepoint.x_min == 0

    assert fizz_plantimelinepoint
    # assert fizz_plantimelinepoint.x_min == fizz_offi_time_max
    fizz_planunit = fizz_plantimelinepoint.x_planunit
    assert fizz_planunit.owner_name == "for_plantimelinepoint_calculation"
    assert fizz_planunit.vow_label == fizz_vowunit.vow_label
    assert fizz_planunit.knot == fizz_vowunit.knot
    assert fizz_planunit.fund_iota == fizz_vowunit.fund_iota
    assert fizz_planunit.respect_bit == fizz_vowunit.respect_bit
    assert fizz_planunit.penny == fizz_vowunit.penny
    assert fizz_planunit.vow_label == fizz_vowunit.vow_label
    assert fizz_plantimelinepoint._month == "March"
    assert fizz_plantimelinepoint._hour == "0-12am"
    assert fizz_plantimelinepoint._minute == 0
    assert fizz_plantimelinepoint._monthday == 1
    assert fizz_plantimelinepoint._c400_number == 0
    assert fizz_plantimelinepoint._year_num == 0


# def test_get_vow_plantimelinepoint_ReturnsObj_Scenario1_VowUnit_NonDefaultAttrs():
#     # ESTABLISH
#     fizz_str = "fizz"
#     slash_str = "/"
#     fizz_fund_iota = 5
#     fizz_respect_bit = 3
#     fizz_penny = 7
#     fizz_vowunit = vowunit_shop(
#         fizz_str,
#         get_module_temp_dir(),
#         knot=slash_str,
#         fund_iota=fizz_fund_iota,
#         respect_bit=fizz_respect_bit,
#         penny=fizz_penny,
#     )
#     assert fizz_vowunit.timeline == timelineunit_shop(get_creg_config())
#     assert not fizz_vowunit._offi_time_max

#     # WHEN
#     fizz_plantimelinepoint = get_vow_plantimelinepoint(fizz_vowunit)

#     # THEN
#     assert fizz_vowunit._offi_time_max == 0
#     assert fizz_plantimelinepoint.x_min == 0

#     assert fizz_plantimelinepoint
#     # assert fizz_plantimelinepoint.x_min == fizz_offi_time_max
#     fizz_planunit = fizz_plantimelinepoint.x_planunit
#     assert fizz_planunit.owner_name == "for_plantimelinepoint_calculation"
#     assert fizz_planunit.vow_label == fizz_vowunit.vow_label
#     assert fizz_planunit.knot == fizz_vowunit.knot
#     assert fizz_planunit.fund_iota == fizz_vowunit.fund_iota
#     assert fizz_planunit.respect_bit == fizz_vowunit.respect_bit
#     assert fizz_planunit.penny == fizz_vowunit.penny
#     assert fizz_planunit.vow_label == fizz_vowunit.vow_label
#     assert fizz_plantimelinepoint._month == "March"
#     assert fizz_plantimelinepoint._hour == 0
#     assert fizz_plantimelinepoint._minute == 0
#     assert fizz_plantimelinepoint._monthday == 1
#     assert fizz_plantimelinepoint._c400_number == 0
#     assert fizz_plantimelinepoint._year_num == 0
#     #  planunit_shop()
#     #  plantimelinepoint_shop()
#     assert 1 == 2
