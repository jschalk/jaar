from src.a01_term_logic.rope import to_rope
from src.a05_plan_logic.plan import planunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.example_owners import (
    get_ownerunit_with_4_levels_and_2reasons,
)


def test_OwnerUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_UnitDoesNotErrorWithEmptyOwnerUnit():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    root_rope = to_rope(yao_owner.belief_label)
    root_plan = yao_owner.get_plan_obj(root_rope)
    assert not root_plan.begin
    assert not root_plan.close
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert not root_plan.begin
    assert not root_plan.close
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc


def test_OwnerUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_DoesNotErrorWhenNoMathLabels():
    # ESTABLISH
    yao_owner = get_ownerunit_with_4_levels_and_2reasons()
    root_rope = to_rope(yao_owner.belief_label)
    root_plan = yao_owner.get_plan_obj(root_rope)
    assert not root_plan._gogo_calc

    # WHEM
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert not root_plan._gogo_calc


def test_OwnerUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_SimpleLabel():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    root_rope = to_rope(yao_owner.belief_label)
    time0_begin = 7
    time0_close = 31
    yao_owner.edit_plan_attr(root_rope, begin=time0_begin, close=time0_close)
    yao_owner._set_plan_dict()
    root_plan = yao_owner.get_plan_obj(root_rope)
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert root_plan._gogo_calc == time0_begin
    assert root_plan._stop_calc == time0_close


def test_OwnerUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_LabelWith_denom():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    root_rope = to_rope(yao_owner.belief_label)
    time0_begin = 6
    time0_close = 21
    time0_denom = 3
    yao_owner.edit_plan_attr(
        root_rope,
        begin=time0_begin,
        close=time0_close,
        denom=time0_denom,
    )
    root_plan = yao_owner.get_plan_obj(root_rope)
    yao_owner._set_plan_dict()
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert root_plan.denom == time0_denom
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert root_plan._gogo_calc == time0_begin / time0_denom
    assert root_plan._stop_calc == time0_close / time0_denom
    assert root_plan._gogo_calc == 2
    assert root_plan._stop_calc == 7


def test_OwnerUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_LabelWith_denom_numor():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    root_rope = to_rope(yao_owner.belief_label)
    time0_begin = 6
    time0_close = 18
    time0_numor = 7
    time0_denom = 3
    yao_owner.edit_plan_attr(
        root_rope,
        begin=time0_begin,
        close=time0_close,
        numor=time0_numor,
        denom=time0_denom,
    )
    root_plan = yao_owner.get_plan_obj(root_rope)
    yao_owner._set_plan_dict()
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert root_plan.numor == time0_numor
    assert root_plan.denom == time0_denom
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert root_plan._gogo_calc == (time0_begin * time0_numor) / time0_denom
    assert root_plan._stop_calc == (time0_close * time0_numor) / time0_denom
    assert root_plan._gogo_calc == 14
    assert root_plan._stop_calc == 42


def test_OwnerUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    root_rope = to_rope(yao_owner.belief_label)
    time0_begin = 6
    time0_close = 18
    time0_addin = 7
    yao_owner.edit_plan_attr(
        root_rope,
        begin=time0_begin,
        close=time0_close,
        addin=time0_addin,
    )
    yao_owner._set_plan_dict()
    root_plan = yao_owner.get_plan_obj(root_rope)
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert root_plan.addin == time0_addin
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert root_plan._gogo_calc == time0_begin + time0_addin
    assert root_plan._stop_calc == time0_close + time0_addin
    assert root_plan._gogo_calc == 13
    assert root_plan._stop_calc == 25


def test_OwnerUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_LabelWith_denom_addin():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    root_rope = to_rope(yao_owner.belief_label)
    time0_begin = 6
    time0_close = 18
    time0_denom = 3
    time0_addin = 60
    yao_owner.edit_plan_attr(
        root_rope,
        begin=time0_begin,
        close=time0_close,
        denom=time0_denom,
        addin=time0_addin,
    )
    yao_owner._set_plan_dict()
    root_plan = yao_owner.get_plan_obj(root_rope)
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert root_plan.denom == time0_denom
    assert root_plan.addin == time0_addin
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == time0_begin
    assert root_plan.close == time0_close
    assert root_plan._gogo_calc == (time0_begin + time0_addin) / time0_denom
    assert root_plan._stop_calc == (time0_close + time0_addin) / time0_denom
    assert root_plan._gogo_calc == 22
    assert root_plan._stop_calc == 26


def test_OwnerUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_Simple0():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    root_rope = to_rope(yao_owner.belief_label)
    time0_str = "time0"
    time0_rope = yao_owner.make_l1_rope(time0_str)
    time0_begin = 7
    time0_close = 31
    time0_plan = planunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_owner.set_l1_plan(time0_plan)

    time1_str = "time1"
    time1_rope = yao_owner.make_rope(time0_rope, time1_str)
    yao_owner.set_plan(planunit_shop(time1_str), time0_rope)
    time1_plan = yao_owner.get_plan_obj(time1_rope)
    root_plan = yao_owner.get_plan_obj(root_rope)
    yao_owner._set_plan_dict()
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert time0_plan.begin == time0_begin
    assert time0_plan.close == time0_close
    assert time1_plan.begin != time0_begin
    assert time1_plan.close != time0_close
    assert not time1_plan._gogo_calc
    assert not time1_plan._stop_calc
    assert yao_owner._range_inheritors == {}

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert time1_plan.begin != time0_begin
    assert time1_plan.close != time0_close
    assert not time1_plan.begin
    assert not time1_plan.close
    assert time1_plan._gogo_calc == time0_begin
    assert time1_plan._stop_calc == time0_close
    assert yao_owner._range_inheritors == {time1_rope: time0_rope}


def test_OwnerUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_LabelWith_denom():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_owner.make_l1_rope(time0_str)
    time0_begin = 14
    time0_close = 35
    time0_plan = planunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_owner.set_l1_plan(time0_plan)

    time1_str = "time1"
    time1_denom = 7
    time1_rope = yao_owner.make_rope(time0_rope, time1_str)
    yao_owner.set_plan(planunit_shop(time1_str, denom=time1_denom), time0_rope)
    time1_plan = yao_owner.get_plan_obj(time1_rope)
    root_rope = to_rope(yao_owner.belief_label)
    root_plan = yao_owner.get_plan_obj(root_rope)
    yao_owner._set_plan_dict()
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert time0_plan.begin == time0_begin
    assert time0_plan.close == time0_close
    assert time1_plan.begin != time0_begin
    assert time1_plan.close != time0_close
    assert not time1_plan._gogo_calc
    assert not time1_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert not time1_plan.begin
    assert not time1_plan.close
    assert time1_plan._gogo_calc == time0_begin / time1_denom
    assert time1_plan._stop_calc == time0_close / time1_denom
    assert time1_plan._gogo_calc == 2
    assert time1_plan._stop_calc == 5


def test_OwnerUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_LabelWith_denom_numor():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_owner.make_l1_rope(time0_str)
    time0_begin = 14
    time0_close = 35
    time0_plan = planunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_owner.set_l1_plan(time0_plan)

    time1_str = "time1"
    time1_denom = 7
    time1_numor = 3
    time1_rope = yao_owner.make_rope(time0_rope, time1_str)
    temp_plan = planunit_shop(time1_str, numor=time1_numor, denom=time1_denom)
    yao_owner.set_plan(temp_plan, time0_rope)
    time1_plan = yao_owner.get_plan_obj(time1_rope)
    root_rope = to_rope(yao_owner.belief_label)
    root_plan = yao_owner.get_plan_obj(root_rope)
    yao_owner._set_plan_dict()
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert time0_plan.begin == time0_begin
    assert time0_plan.close == time0_close
    assert time1_plan.begin != time0_begin
    assert time1_plan.close != time0_close
    assert not time1_plan._gogo_calc
    assert not time1_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert not time1_plan.begin
    assert not time1_plan.close
    assert time1_plan._gogo_calc == (time0_begin * time1_numor) / time1_denom
    assert time1_plan._stop_calc == (time0_close * time1_numor) / time1_denom
    assert time1_plan._gogo_calc == 6
    assert time1_plan._stop_calc == 15


def test_OwnerUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_owner.make_l1_rope(time0_str)
    time0_begin = 3
    time0_close = 7
    time0_plan = planunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_owner.set_l1_plan(time0_plan)

    time1_str = "time1"
    time1_addin = 5
    time1_rope = yao_owner.make_rope(time0_rope, time1_str)
    temp_plan = planunit_shop(time1_str, addin=time1_addin)
    yao_owner.set_plan(temp_plan, time0_rope)
    time1_plan = yao_owner.get_plan_obj(time1_rope)
    root_rope = to_rope(yao_owner.belief_label)
    root_plan = yao_owner.get_plan_obj(root_rope)
    yao_owner._set_plan_dict()
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert time0_plan.begin == time0_begin
    assert time0_plan.close == time0_close
    assert time1_plan.begin != time0_begin
    assert time1_plan.close != time0_close
    assert time1_plan.addin == time1_addin
    assert not time1_plan._gogo_calc
    assert not time1_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert not time1_plan.begin
    assert not time1_plan.close
    assert time1_plan._gogo_calc == time0_plan._gogo_calc + time1_addin
    assert time1_plan._stop_calc == time0_plan._stop_calc + time1_addin
    assert time1_plan._gogo_calc == 8
    assert time1_plan._stop_calc == 12


def test_OwnerUnit_set_plantree_range_attrs_Sets2LevelsDescendentPlan_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_owner.make_l1_rope(time0_str)
    time0_begin = 3
    time0_close = 7
    time0_plan = planunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_owner.set_l1_plan(time0_plan)

    time1_str = "time1"
    time1_rope = yao_owner.make_rope(time0_rope, time1_str)
    yao_owner.add_plan(time1_rope)
    time2_str = "time2"
    time2_rope = yao_owner.make_rope(time1_rope, time2_str)
    time2_addin = 5
    x_time2_plan = planunit_shop(time2_str, addin=time2_addin)
    yao_owner.set_plan(x_time2_plan, time1_rope)
    time2_plan = yao_owner.get_plan_obj(time2_rope)
    root_rope = to_rope(yao_owner.belief_label)
    root_plan = yao_owner.get_plan_obj(root_rope)
    yao_owner._set_plan_dict()
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert time0_plan.begin == time0_begin
    assert time0_plan.close == time0_close
    assert time2_plan.begin != time0_begin
    assert time2_plan.close != time0_close
    assert time2_plan.addin == time2_addin
    assert not time2_plan._gogo_calc
    assert not time2_plan._stop_calc
    assert yao_owner._range_inheritors == {}

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert not time2_plan.begin
    assert not time2_plan.close
    assert time2_plan._gogo_calc == time0_plan._gogo_calc + time2_addin
    assert time2_plan._stop_calc == time0_plan._stop_calc + time2_addin
    assert time2_plan._gogo_calc == 8
    assert time2_plan._stop_calc == 12
    assert yao_owner._range_inheritors == {
        time1_rope: time0_rope,
        time2_rope: time0_rope,
    }


def test_OwnerUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_LabelWith_denom_addin():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_owner.make_l1_rope(time0_str)
    time0_begin = 21
    time0_close = 35
    time0_plan = planunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_owner.set_l1_plan(time0_plan)

    time1_str = "time1"
    time1_addin = 70
    time1_denom = 7
    time1_rope = yao_owner.make_rope(time0_rope, time1_str)
    temp_plan = planunit_shop(time1_str, denom=time1_denom, addin=time1_addin)
    yao_owner.set_plan(temp_plan, time0_rope)
    time1_plan = yao_owner.get_plan_obj(time1_rope)
    root_rope = to_rope(yao_owner.belief_label)
    root_plan = yao_owner.get_plan_obj(root_rope)
    yao_owner._set_plan_dict()
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert time0_plan.begin == time0_begin
    assert time0_plan.close == time0_close
    assert time1_plan.begin != time0_begin
    assert time1_plan.close != time0_close
    assert time1_plan.addin == time1_addin
    assert not time1_plan._gogo_calc
    assert not time1_plan._stop_calc

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert not time1_plan.begin
    assert not time1_plan.close
    assert time1_plan._gogo_calc == (time0_plan._gogo_calc + time1_addin) / time1_denom
    assert time1_plan._stop_calc == (time0_plan._stop_calc + time1_addin) / time1_denom
    assert time1_plan._gogo_calc == 13
    assert time1_plan._stop_calc == 15


def test_OwnerUnit_set_plantree_range_attrs_SetsDescendentPlan_When_knot_IsNonDefault():
    # ESTABLISH
    slash_str = "/"
    yao_owner = ownerunit_shop("Yao", knot=slash_str)
    root_rope = to_rope(yao_owner.belief_label, knot=slash_str)
    time0_str = "time0"
    time0_rope = yao_owner.make_l1_rope(time0_str)
    time0_begin = 7
    time0_close = 31
    time0_plan = planunit_shop(
        time0_str, begin=time0_begin, close=time0_close, knot=slash_str
    )
    yao_owner.set_l1_plan(time0_plan)

    time1_str = "time1"
    time1_rope = yao_owner.make_rope(time0_rope, time1_str)
    yao_owner.set_plan(planunit_shop(time1_str), time0_rope)
    time1_plan = yao_owner.get_plan_obj(time1_rope)
    root_plan = yao_owner.get_plan_obj(root_rope)
    yao_owner._set_plan_dict()
    assert not root_plan._gogo_calc
    assert not root_plan._stop_calc
    assert time0_plan.begin == time0_begin
    assert time0_plan.close == time0_close
    assert time1_plan.begin != time0_begin
    assert time1_plan.close != time0_close
    assert not time1_plan._gogo_calc
    assert not time1_plan._stop_calc
    assert yao_owner._range_inheritors == {}

    # WHEN
    yao_owner._set_plantree_range_attrs()

    # THEN
    assert time1_plan.begin != time0_begin
    assert time1_plan.close != time0_close
    assert not time1_plan.begin
    assert not time1_plan.close
    assert time1_plan._gogo_calc == time0_begin
    assert time1_plan._stop_calc == time0_close
    assert yao_owner._range_inheritors == {time1_rope: time0_rope}
