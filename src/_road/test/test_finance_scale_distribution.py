from src._road.finance import (
    allot_scale,
    _create_allot_dict,
    _allot_missing_scale,
    _get_missing_scale_list,
)
from pytest import raises as pytest_raises


def test_create_missing_distribution_list_ReturnsObjScenario00():
    # ESTABLISH
    x_missing_scale = 0
    x_grain = 0
    x_list_length = 0

    # WHEN
    missing_scale_list = _get_missing_scale_list(
        missing_scale=x_missing_scale, grain_unit=x_grain, list_length=x_list_length
    )

    # THEN
    assert missing_scale_list == []


def test_create_missing_distribution_list_ReturnsObjScenario01():
    # ESTABLISH
    x_missing_scale = 0
    x_grain = 5
    x_list_length = 3

    # WHEN
    missing_scale_list = _get_missing_scale_list(
        missing_scale=x_missing_scale, grain_unit=x_grain, list_length=x_list_length
    )

    # THEN
    assert missing_scale_list == []


def test_create_missing_distribution_list_ReturnsObjScenario02():
    # ESTABLISH
    x_missing = 60
    x_grain = 5
    x_list_length = 3

    # WHEN
    missing_scale_list = _get_missing_scale_list(x_missing, x_grain, x_list_length)

    # THEN
    assert missing_scale_list == [20, 20, 20]


def test_create_missing_distribution_list_ReturnsObjScenario03():
    # ESTABLISH
    x_missing_scale = 40
    x_grain = 5
    x_list_length = 3

    # WHEN
    missing_scale_list = _get_missing_scale_list(
        missing_scale=x_missing_scale, grain_unit=x_grain, list_length=x_list_length
    )

    # THEN
    assert missing_scale_list == [15, 15, 10]


def test_create_missing_distribution_list_ReturnsObjScenario04():
    # ESTABLISH
    x_missing_scale = -20
    x_grain = 5
    x_list_length = 4

    # WHEN
    missing_scale_list = _get_missing_scale_list(
        missing_scale=x_missing_scale, grain_unit=x_grain, list_length=x_list_length
    )

    # THEN
    assert missing_scale_list == [-5, -5, -5, -5]


def test_create_missing_distribution_list_ReturnsObjScenario05():
    # ESTABLISH
    x_missing_scale = -35
    x_grain = 5
    x_list_length = 4

    # WHEN
    missing_scale_list = _get_missing_scale_list(
        missing_scale=x_missing_scale, grain_unit=x_grain, list_length=x_list_length
    )

    # THEN
    assert missing_scale_list == [-10, -10, -10, -5]


def test_allot_missing_scale_DistributesTheMissingScale_scenario00():
    # ESTABLISH
    before_ledger = {}
    x_missing_scale = 10
    x_grain = 5
    full_before_allot = 0
    full_scale = full_before_allot + x_missing_scale

    # WHEN
    gen_ledger = _allot_missing_scale(
        ledger=before_ledger,
        scale_number=full_scale,
        grain_unit=x_grain,
        missing_scale=x_missing_scale,
    )

    # THEN
    after_ledger = {}
    assert gen_ledger == after_ledger


def test_allot_missing_scale_DistributesTheMissingScale_scenario01():
    # ESTABLISH
    bob_text = "Bob"
    sue_text = "Sue"
    yao_text = "Yao"
    bob_before_allot = 1000
    sue_before_allot = 900
    yao_allot = 800
    before_ledger = {
        yao_text: yao_allot,
        sue_text: sue_before_allot,
        bob_text: bob_before_allot,
    }
    x_missing_scale = 10
    x_grain = 5
    full_before_allot = bob_before_allot + sue_before_allot + yao_allot
    full_scale = full_before_allot + x_missing_scale

    # WHEN
    gen_ledger = _allot_missing_scale(
        ledger=before_ledger,
        scale_number=full_scale,
        grain_unit=x_grain,
        missing_scale=x_missing_scale,
    )

    # THEN
    bob_after_allot = bob_before_allot + x_grain
    sue_after_allot = sue_before_allot + x_grain
    assert gen_ledger.get(bob_text) == bob_after_allot
    assert gen_ledger.get(sue_text) == sue_after_allot
    after_ledger = {
        yao_text: yao_allot,
        sue_text: sue_after_allot,
        bob_text: bob_after_allot,
    }
    assert gen_ledger == after_ledger


def test_allot_missing_scale_DistributesTheMissingScale_scenario02():
    # ESTABLISH
    bob_text = "Bob"
    sue_text = "Sue"
    yao_text = "Yao"
    bob_before_allot = 1000
    sue_before_allot = 900
    yao_before_allot = 800
    before_ledger = {
        yao_text: yao_before_allot,
        sue_text: sue_before_allot,
        bob_text: bob_before_allot,
    }
    x_missing_scale = 40
    x_grain = 5
    full_before_allot = bob_before_allot + sue_before_allot + yao_before_allot
    full_scale = full_before_allot + x_missing_scale

    # WHEN
    gen_ledger = _allot_missing_scale(
        ledger=before_ledger,
        scale_number=full_scale,
        grain_unit=x_grain,
        missing_scale=x_missing_scale,
    )

    # THEN
    bob_after_allot = bob_before_allot + 15
    sue_after_allot = sue_before_allot + 15
    yao_after_allot = yao_before_allot + 10
    assert gen_ledger.get(bob_text) == bob_after_allot
    assert gen_ledger.get(sue_text) == sue_after_allot
    after_ledger = {
        yao_text: yao_after_allot,
        sue_text: sue_after_allot,
        bob_text: bob_after_allot,
    }
    assert gen_ledger == after_ledger


def test_allot_missing_scale_RaisesErrorWhen_ledgerSummationIsNot_scale_number():
    # ESTABLISH
    bob_text = "Bob"
    sue_text = "Sue"
    yao_text = "Yao"
    bob_before_allot = 1000
    sue_before_allot = 900
    yao_allot = 800
    before_ledger = {
        yao_text: yao_allot,
        sue_text: sue_before_allot,
        bob_text: bob_before_allot,
    }
    x_missing_scale = 10
    x_grain = 5
    full_before_allot = bob_before_allot + sue_before_allot + yao_allot
    correct_full_scale = full_before_allot + x_missing_scale
    wrong_full_scale = 1088

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        _allot_missing_scale(
            ledger=before_ledger,
            scale_number=wrong_full_scale,
            grain_unit=x_grain,
            missing_scale=x_missing_scale,
        )
    assert (
        str(excinfo.value)
        == f"Summation of output allots '{correct_full_scale}' is not equal to scale '{wrong_full_scale}'."
    )


def test_allot_missing_scale_CorrectlyReturnsEmpty_ledger():
    # ESTABLISH
    before_ledger = {}
    x_missing_scale = 44
    x_grain = 1
    wrong_full_scale = 1088

    # WHEN / THEN
    assert {} == _allot_missing_scale(
        ledger=before_ledger,
        scale_number=wrong_full_scale,
        grain_unit=x_grain,
        missing_scale=x_missing_scale,
    )


def test_allot_scale_v01():
    # ESTABLISH
    x_ledger = {"obj1": 1.0, "obj2": 2.0, "obj3": 3.0}
    print(f"{x_ledger=}")
    scale_number = 100
    grain_unit = 0.5

    # WHEN
    alloted_accts = allot_scale(x_ledger, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 16.5
    assert alloted_accts.get("obj2") == 33.5
    assert alloted_accts.get("obj3") == 50.0
    assert sum(alloted_accts.values()) == scale_number


def test_allot_scale_v02():
    # ESTABLISH
    accts = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
    }
    print(f"{accts=}")
    scale_number = 100
    grain_unit = 0.3

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        allot_scale(accts, scale_number, grain_unit)
    assert (
        str(excinfo.value)
        == f"The scale number '{scale_number}' must be a multiple of the grain unit '{grain_unit}'."
    )


def test_allot_scale_v03():
    # ESTABLISH
    accts = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
    }
    print(f"{accts=}")
    scale_number = 100.5
    grain_unit = 0.5

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 17
    assert alloted_accts.get("obj2") == 33.5
    assert alloted_accts.get("obj3") == 50.0
    assert sum(alloted_accts.values()) == scale_number


def test_allot_scale_v04():
    # ESTABLISH
    accts = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
    }
    print(f"{accts=}")
    scale_number = 101
    grain_unit = 0.5

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 17
    assert alloted_accts.get("obj2") == 33.5
    assert alloted_accts.get("obj3") == 50.5
    assert sum(alloted_accts.values()) == scale_number


def test_allot_scale_v05():
    # ESTABLISH
    accts = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
        "obj4": 7.0,
        "obj5": 13.0,
        "obj6": 99.0,
        "obj7": 41.0,
    }
    print(f"{accts=}")
    scale_number = 101
    grain_unit = 0.5

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 0.5
    assert alloted_accts.get("obj2") == 1
    assert alloted_accts.get("obj3") == 2
    assert alloted_accts.get("obj4") == 4.5
    assert alloted_accts.get("obj5") == 8
    assert alloted_accts.get("obj6") == 60
    assert alloted_accts.get("obj7") == 25
    assert sum(alloted_accts.values()) == scale_number


def test_allot_scale_v06():
    # ESTABLISH
    accts = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
        "obj4": 7.0,
        "obj5": 13.0,
        "obj6": 99.0,
        "obj7": 100000000.0,
    }
    print(f"{accts=}")
    scale_number = 101
    grain_unit = 0.5

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 0
    assert alloted_accts.get("obj2") == 0
    assert alloted_accts.get("obj3") == 0
    assert alloted_accts.get("obj4") == 0
    assert alloted_accts.get("obj5") == 0
    assert alloted_accts.get("obj6") == 0
    assert alloted_accts.get("obj7") == 101
    assert sum(alloted_accts.values()) == scale_number


def test_allot_scale_v07():
    # ESTABLISH
    accts = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
        "obj4": 7.0,
        "obj5": 13.0,
        "obj6": 99.0,
        "obj7": 100000000.0,
    }
    print(f"{accts=}")
    scale_number = 1
    grain_unit = 0.5

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 0
    assert alloted_accts.get("obj2") == 0
    assert alloted_accts.get("obj3") == 0
    assert alloted_accts.get("obj4") == 0
    assert alloted_accts.get("obj5") == 0
    assert alloted_accts.get("obj6") == 0
    assert alloted_accts.get("obj7") == 1
    assert sum(alloted_accts.values()) == scale_number


def test_allot_scale_v08():
    # ESTABLISH
    accts = {
        "obj1": 0,
        "obj2": 0,
        "obj3": 0,
        "obj4": 0,
        "obj5": 0,
        "obj6": 0,
    }
    print(f"{accts=}")
    scale_number = 1
    grain_unit = 0.5

    # WHEN / THEN
    # with pytest_raises(Exception) as excinfo:
    #     allot_scale(accts, scale_number, grain_unit)
    # assert (
    #     str(excinfo.value)
    #     == f"If the summation of ledger values is zero the scale_number '{scale_number}' needs to be zero."
    # )

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 0
    assert alloted_accts.get("obj2") == 0
    assert alloted_accts.get("obj3") == 0
    assert alloted_accts.get("obj4") == 0
    assert alloted_accts.get("obj5") == 0
    assert alloted_accts.get("obj6") == 0
    assert sum(alloted_accts.values()) == 0
    assert sum(alloted_accts.values()) != scale_number


def test_allot_scale_v09():
    # ESTABLISH
    accts = {
        "obj1": 0,
        "obj2": 0,
        "obj3": 0,
        "obj4": 0,
        "obj5": 0,
        "obj6": 0,
    }
    print(f"{accts=}")
    scale_number = 0
    grain_unit = 0.5

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 0
    assert alloted_accts.get("obj2") == 0
    assert alloted_accts.get("obj3") == 0
    assert alloted_accts.get("obj4") == 0
    assert alloted_accts.get("obj5") == 0
    assert alloted_accts.get("obj6") == 0
    assert sum(alloted_accts.values()) == scale_number


def test_allot_scale_v10():
    # ESTABLISH
    accts = {
        "obj1": 0,
        "obj2": 0,
        "obj3": 0,
        "obj4": 34,
        "obj5": 55,
        "obj6": 55,
        "obj7": 55,
    }
    print(f"{accts=}")
    scale_number = 6
    grain_unit = 3

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 0
    assert alloted_accts.get("obj2") == 0
    assert alloted_accts.get("obj3") == 0
    assert alloted_accts.get("obj4") == 0
    assert alloted_accts.get("obj5") == 0
    assert alloted_accts.get("obj6") == 3
    assert alloted_accts.get("obj7") == 3
    assert sum(alloted_accts.values()) == scale_number


def test_allot_scale_v11():
    # ESTABLISH
    accts = {}
    print(f"{accts=}")
    scale_number = 6
    grain_unit = 3

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts == {}


def test_allot_scale_v12():
    # ESTABLISH
    accts = {
        "obj1": 1,
        "obj2": 0,
        "obj3": 0,
        "obj4": 34,
        "obj5": 55,
        "obj6": 55,
        "obj7": 55,
    }
    print(f"{accts=}")
    scale_number = 6
    grain_unit = 3

    # WHEN
    alloted_accts = allot_scale(accts, scale_number, grain_unit)

    # THEN
    print(alloted_accts)
    assert alloted_accts.get("obj1") == 0
    assert alloted_accts.get("obj2") == 0
    assert alloted_accts.get("obj3") == 0
    assert alloted_accts.get("obj4") == 0
    assert alloted_accts.get("obj5") == 0
    assert alloted_accts.get("obj6") == 3
    assert alloted_accts.get("obj7") == 3
    assert sum(alloted_accts.values()) == scale_number


def test_get_missing_scale_list_RaisesErrorIfWhileLoopFails_Scenario0():
    # ESTABLISH
    x_missing_scale = 10
    x_grain_unit = 7
    x_list_length = 3

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        _get_missing_scale_list(x_missing_scale, x_grain_unit, x_list_length)
    assert (
        str(excinfo.value)
        == f"missing_base_residual calculation failed probably due to missing_scale not being a multiple of grain_unit. missing_scale={x_missing_scale} grain_unit={x_grain_unit}."
    )


def test_get_missing_scale_list_RaisesErrorIfWhileLoopFails_Scenario1():
    # ESTABLISH
    x_missing_scale = -10
    x_grain_unit = 7
    x_list_length = 3

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        _get_missing_scale_list(x_missing_scale, x_grain_unit, x_list_length)
    assert (
        str(excinfo.value)
        == f"missing_base_residual calculation failed probably due to missing_scale not being a multiple of grain_unit. missing_scale={x_missing_scale} grain_unit={x_grain_unit}."
    )


def test__create_allot_dict_SummationFailsInConsistentWay():
    # ESTABLISH
    ledger = {
        "ACME": 1,
        "Aaron Donald things effected by him": 1,
        "Asset management": 1,
        "Bob Dylan Root": 1,
        "D&B": 1,
        "Freelancing": 1,
        "Internet": 1,
        "Moods": 1,
        "Nation-States": 1,
        "No Movie playing": 1,
        "Seasons": 1,
        "Tired Status": 1,
        "Ultimate Frisbee": 1,
        "Water Living": 1,
        "WaterExistence": 1,
        "casa": 1,
        "ced_day": 40,
        "ced_week": 40,
        "ced_year": 40,
        "day_hour": 40,
        "day_minute": 40,
        "month_day": 40,
        "month_week": 40,
        "weekdays": 40,
        "year_month": 40,
        "year_week": 40,
    }
    scale_number = 1000000000.0
    grain_unit = 1

    # WHEN
    gen_alloted_dict = _create_allot_dict(ledger, scale_number, grain_unit)

    # THEN
    # wrongsum_allot_dict = {
    #     "ACME": 2192982,
    #     "Aaron Donald things effected by him": 2192982,
    #     "Asset management": 2192982,
    #     "Bob Dylan Root": 2192982,
    #     "D&B": 2192982,
    #     "Freelancing": 2192982,
    #     "Internet": 2192982,
    #     "Moods": 2192982,
    #     "Nation-States": 2192982,
    #     "No Movie playing": 2192982,
    #     "Seasons": 2192982,
    #     "Tired Status": 2192982,
    #     "Ultimate Frisbee": 2192982,
    #     "Water Living": 2192982,
    #     "WaterExistence": 2192982,
    #     "casa": 2192982,
    #     "ced_day": 87719298,
    #     "ced_week": 87719298,
    #     "ced_year": 87719298,
    #     "day_hour": 87719298,
    #     "day_minute": 87719298,
    #     "month_day": 87719298,
    #     "month_week": 87719298,
    #     "weekdays": 87719298,
    #     "year_month": 87719298,
    #     "year_week": 87719298,
    # }
    # assert gen_alloted_dict == wrongsum_allot_dict
    assert sum(gen_alloted_dict.values()) != scale_number
    assert sum(gen_alloted_dict.values()) + 4 == scale_number


def test_allot_scale_Summation():
    # ESTABLISH
    ledger = {
        "ACME": 1,
        "Aaron Donald things effected by him": 1,
        "Asset management": 1,
        "Bob Dylan Root": 1,
        "D&B": 1,
        "Freelancing": 1,
        "Internet": 1,
        "Moods": 1,
        "Nation-States": 1,
        "No Movie playing": 1,
        "Seasons": 1,
        "Tired Status": 1,
        "Ultimate Frisbee": 1,
        "Water Living": 1,
        "WaterExistence": 1,
        "casa": 1,
        "ced_day": 40,
        "ced_week": 40,
        "ced_year": 40,
        "day_hour": 40,
        "day_minute": 40,
        "month_day": 40,
        "month_week": 40,
        "weekdays": 40,
        "year_month": 40,
        "year_week": 40,
    }
    scale_number = 1000000000.0
    grain_unit = 1

    # WHEN
    sub_function_alloted_dict = _create_allot_dict(ledger, scale_number, grain_unit)
    top_function_alloted_dict = allot_scale(ledger, scale_number, grain_unit)

    # THEN
    assert sum(sub_function_alloted_dict.values()) + 4 == scale_number
    assert sum(top_function_alloted_dict.values()) == scale_number

    # correct_sum_allot_dict = {
    #     "ACME": 2192983,
    #     "Aaron Donald things effected by him": 2192983,
    #     "Asset management": 2192983,
    #     "Bob Dylan Root": 2192983,
    #     "D&B": 2192983,
    #     "Freelancing": 2192983,
    #     "Internet": 2192983,
    #     "Moods": 2192983,
    #     "Nation-States": 2192983,
    #     "No Movie playing": 2192983,
    #     "Seasons": 2192982,
    #     "Tired Status": 2192982,
    #     "Ultimate Frisbee": 2192982,
    #     "Water Living": 2192982,
    #     "WaterExistence": 2192982,
    #     "casa": 2192982,
    #     "ced_day": 87719298,
    #     "ced_week": 87719298,
    #     "ced_year": 87719298,
    #     "day_hour": 87719298,
    #     "day_minute": 87719298,
    #     "month_day": 87719298,
    #     "month_week": 87719298,
    #     "weekdays": 87719298,
    #     "year_month": 87719298,
    #     "year_week": 87719298,
    # }
    # assert sub_function_alloted_dict != correct_sum_allot_dict
    # assert top_function_alloted_dict == correct_sum_allot_dict
    assert sum(top_function_alloted_dict.values()) == scale_number
