from src.ch05_plan_logic.plan import plans_calculated_range, planunit_shop
from src.ch05_plan_logic.range_toolbox import RangeUnit


def test_plans_calculated_range_ReturnsObj_EmptyList():
    # ESTABLISH
    x_rangeunit = RangeUnit(3, 8)

    # WHEN / THEN
    assert plans_calculated_range([], x_rangeunit.gogo, x_rangeunit.stop) == x_rangeunit


def test_plans_calculated_range_ReturnsObj_EmptyPlanUnit():
    # ESTABLISH
    wk_str = "wk"
    wk_plan = planunit_shop(wk_str)
    x_rangeunit = RangeUnit(3, 8)

    # WHEN / THEN
    assert (
        plans_calculated_range([wk_plan], x_rangeunit.gogo, x_rangeunit.stop)
        == x_rangeunit
    )


def test_plans_calculated_range_ReturnsObj_1PlanUnit_addin():
    # ESTABLISH
    wk_str = "wk"
    wk_addin = 5
    wk_plan = planunit_shop(wk_str, addin=wk_addin)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    # WHEN
    new_rangeunit = plans_calculated_range(
        [wk_plan], old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo + wk_addin
    new_stop = old_stop + wk_addin
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_plans_calculated_range_ReturnsObj_2PlanUnit_addin():
    # ESTABLISH
    wk_str = "wk"
    wk_addin = 5
    wk_plan = planunit_shop(wk_str, addin=wk_addin)
    tue_addin = 7
    tue_plan = planunit_shop("Tue", addin=tue_addin)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    # WHEN
    new_rangeunit = plans_calculated_range(
        [wk_plan, tue_plan], old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo + wk_addin + tue_addin
    new_stop = old_stop + wk_addin + tue_addin
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_plans_calculated_range_ReturnsObj_2PlanUnit_numor():
    # ESTABLISH
    wk_str = "wk"
    wk_numor = 5
    wk_plan = planunit_shop(wk_str, numor=wk_numor)
    tue_numor = 10
    tue_plan = planunit_shop("Tue", numor=tue_numor)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)
    plan_list = [wk_plan, tue_plan]

    # WHEN
    new_rangeunit = plans_calculated_range(
        plan_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo * wk_numor * tue_numor
    new_stop = old_stop * wk_numor * tue_numor
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_plans_calculated_range_ReturnsObj_2PlanUnit_denom():
    # ESTABLISH
    wk_str = "wk"
    wk_denom = 5
    wk_plan = planunit_shop(wk_str, denom=wk_denom)
    tue_denom = 2
    tue_plan = planunit_shop("Tue", denom=tue_denom)
    old_gogo = 30
    old_stop = 80
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    plan_list = [wk_plan, tue_plan]

    # WHEN
    new_rangeunit = plans_calculated_range(
        plan_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_rangeunit.gogo / wk_denom / tue_denom
    new_stop = old_rangeunit.stop / wk_denom / tue_denom
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop
    assert new_rangeunit.gogo == 3
    assert new_rangeunit.stop == 8


def test_plans_calculated_range_ReturnsObj_2PlanUnit_denom_morph():
    # ESTABLISH
    wk_str = "wk"
    wk_denom = 50
    wk_plan = planunit_shop(wk_str, denom=wk_denom, morph=True)
    tue_denom = 20
    tue_plan = planunit_shop("Tue", denom=tue_denom, morph=True)
    old_gogo = 175
    old_stop = 186
    old_rangeunit = RangeUnit(old_gogo, old_stop)
    plan_list = [wk_plan, tue_plan]

    # WHEN
    new_rangeunit = plans_calculated_range(
        plan_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = (old_rangeunit.gogo % wk_denom) % tue_denom
    new_stop = (old_rangeunit.stop % wk_denom) % tue_denom
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop
    assert new_rangeunit.gogo == 5
    assert new_rangeunit.stop == 16
