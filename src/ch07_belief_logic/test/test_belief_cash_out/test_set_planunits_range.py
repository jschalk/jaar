from src.ch01_rope_logic.rope import to_rope
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.example_beliefs import (
    get_beliefunit_with_4_levels_and_2reasons,
)


def test_BeliefUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_UnitDoesNotErrorWithEmptyBeliefUnit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    root_rope = to_rope(yao_belief.moment_label)
    root_plan = yao_belief.get_plan_obj(root_rope)
    assert not root_plan.begin
    assert not root_plan.close
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert not root_plan.begin
    assert not root_plan.close
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc


def test_BeliefUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_DoesNotErrorWhenNoMathLabels():
    # ESTABLISH
    yao_belief = get_beliefunit_with_4_levels_and_2reasons()
    root_rope = to_rope(yao_belief.moment_label)
    root_plan = yao_belief.get_plan_obj(root_rope)
    assert not root_plan.gogo_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert not root_plan.gogo_calc


def test_BeliefUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_SimpleLabel():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    root_rope = to_rope(yao_belief.moment_label)
    ziet0_begin = 7
    ziet0_close = 31
    yao_belief.edit_plan_attr(root_rope, begin=ziet0_begin, close=ziet0_close)
    yao_belief._set_plan_dict()
    root_plan = yao_belief.get_plan_obj(root_rope)
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert root_plan.gogo_calc == ziet0_begin
    assert root_plan.stop_calc == ziet0_close


def test_BeliefUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_LabelWith_denom():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    root_rope = to_rope(yao_belief.moment_label)
    ziet0_begin = 6
    ziet0_close = 21
    ziet0_denom = 3
    yao_belief.edit_plan_attr(
        root_rope,
        begin=ziet0_begin,
        close=ziet0_close,
        denom=ziet0_denom,
    )
    root_plan = yao_belief.get_plan_obj(root_rope)
    yao_belief._set_plan_dict()
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert root_plan.denom == ziet0_denom
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert root_plan.gogo_calc == ziet0_begin / ziet0_denom
    assert root_plan.stop_calc == ziet0_close / ziet0_denom
    assert root_plan.gogo_calc == 2
    assert root_plan.stop_calc == 7


def test_BeliefUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_LabelWith_denom_numor():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    root_rope = to_rope(yao_belief.moment_label)
    ziet0_begin = 6
    ziet0_close = 18
    ziet0_numor = 7
    ziet0_denom = 3
    yao_belief.edit_plan_attr(
        root_rope,
        begin=ziet0_begin,
        close=ziet0_close,
        numor=ziet0_numor,
        denom=ziet0_denom,
    )
    root_plan = yao_belief.get_plan_obj(root_rope)
    yao_belief._set_plan_dict()
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert root_plan.numor == ziet0_numor
    assert root_plan.denom == ziet0_denom
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert root_plan.gogo_calc == (ziet0_begin * ziet0_numor) / ziet0_denom
    assert root_plan.stop_calc == (ziet0_close * ziet0_numor) / ziet0_denom
    assert root_plan.gogo_calc == 14
    assert root_plan.stop_calc == 42


def test_BeliefUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    root_rope = to_rope(yao_belief.moment_label)
    ziet0_begin = 6
    ziet0_close = 18
    ziet0_addin = 7
    yao_belief.edit_plan_attr(
        root_rope,
        begin=ziet0_begin,
        close=ziet0_close,
        addin=ziet0_addin,
    )
    yao_belief._set_plan_dict()
    root_plan = yao_belief.get_plan_obj(root_rope)
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert root_plan.addin == ziet0_addin
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert root_plan.gogo_calc == ziet0_begin + ziet0_addin
    assert root_plan.stop_calc == ziet0_close + ziet0_addin
    assert root_plan.gogo_calc == 13
    assert root_plan.stop_calc == 25


def test_BeliefUnit_set_plantree_range_attrs_SetsInitialPlan_gogo_calc_stop_calc_LabelWith_denom_addin():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    root_rope = to_rope(yao_belief.moment_label)
    ziet0_begin = 6
    ziet0_close = 18
    ziet0_denom = 3
    ziet0_addin = 60
    yao_belief.edit_plan_attr(
        root_rope,
        begin=ziet0_begin,
        close=ziet0_close,
        denom=ziet0_denom,
        addin=ziet0_addin,
    )
    yao_belief._set_plan_dict()
    root_plan = yao_belief.get_plan_obj(root_rope)
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert root_plan.denom == ziet0_denom
    assert root_plan.addin == ziet0_addin
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert root_plan.begin == ziet0_begin
    assert root_plan.close == ziet0_close
    assert root_plan.gogo_calc == (ziet0_begin + ziet0_addin) / ziet0_denom
    assert root_plan.stop_calc == (ziet0_close + ziet0_addin) / ziet0_denom
    assert root_plan.gogo_calc == 22
    assert root_plan.stop_calc == 26


def test_BeliefUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_Simple0():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    root_rope = to_rope(yao_belief.moment_label)
    ziet0_str = "ziet0"
    ziet0_rope = yao_belief.make_l1_rope(ziet0_str)
    ziet0_begin = 7
    ziet0_close = 31
    ziet0_plan = planunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_belief.set_l1_plan(ziet0_plan)

    ziet1_str = "ziet1"
    ziet1_rope = yao_belief.make_rope(ziet0_rope, ziet1_str)
    yao_belief.set_plan(planunit_shop(ziet1_str), ziet0_rope)
    ziet1_plan = yao_belief.get_plan_obj(ziet1_rope)
    root_plan = yao_belief.get_plan_obj(root_rope)
    yao_belief._set_plan_dict()
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert ziet0_plan.begin == ziet0_begin
    assert ziet0_plan.close == ziet0_close
    assert ziet1_plan.begin != ziet0_begin
    assert ziet1_plan.close != ziet0_close
    assert not ziet1_plan.gogo_calc
    assert not ziet1_plan.stop_calc
    assert yao_belief._range_inheritors == {}

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert ziet1_plan.begin != ziet0_begin
    assert ziet1_plan.close != ziet0_close
    assert not ziet1_plan.begin
    assert not ziet1_plan.close
    assert ziet1_plan.gogo_calc == ziet0_begin
    assert ziet1_plan.stop_calc == ziet0_close
    assert yao_belief._range_inheritors == {ziet1_rope: ziet0_rope}


def test_BeliefUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_LabelWith_denom():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_belief.make_l1_rope(ziet0_str)
    ziet0_begin = 14
    ziet0_close = 35
    ziet0_plan = planunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_belief.set_l1_plan(ziet0_plan)

    ziet1_str = "ziet1"
    ziet1_denom = 7
    ziet1_rope = yao_belief.make_rope(ziet0_rope, ziet1_str)
    yao_belief.set_plan(planunit_shop(ziet1_str, denom=ziet1_denom), ziet0_rope)
    ziet1_plan = yao_belief.get_plan_obj(ziet1_rope)
    root_rope = to_rope(yao_belief.moment_label)
    root_plan = yao_belief.get_plan_obj(root_rope)
    yao_belief._set_plan_dict()
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert ziet0_plan.begin == ziet0_begin
    assert ziet0_plan.close == ziet0_close
    assert ziet1_plan.begin != ziet0_begin
    assert ziet1_plan.close != ziet0_close
    assert not ziet1_plan.gogo_calc
    assert not ziet1_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert not ziet1_plan.begin
    assert not ziet1_plan.close
    assert ziet1_plan.gogo_calc == ziet0_begin / ziet1_denom
    assert ziet1_plan.stop_calc == ziet0_close / ziet1_denom
    assert ziet1_plan.gogo_calc == 2
    assert ziet1_plan.stop_calc == 5


def test_BeliefUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_LabelWith_denom_numor():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_belief.make_l1_rope(ziet0_str)
    ziet0_begin = 14
    ziet0_close = 35
    ziet0_plan = planunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_belief.set_l1_plan(ziet0_plan)

    ziet1_str = "ziet1"
    ziet1_denom = 7
    ziet1_numor = 3
    ziet1_rope = yao_belief.make_rope(ziet0_rope, ziet1_str)
    temp_plan = planunit_shop(ziet1_str, numor=ziet1_numor, denom=ziet1_denom)
    yao_belief.set_plan(temp_plan, ziet0_rope)
    ziet1_plan = yao_belief.get_plan_obj(ziet1_rope)
    root_rope = to_rope(yao_belief.moment_label)
    root_plan = yao_belief.get_plan_obj(root_rope)
    yao_belief._set_plan_dict()
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert ziet0_plan.begin == ziet0_begin
    assert ziet0_plan.close == ziet0_close
    assert ziet1_plan.begin != ziet0_begin
    assert ziet1_plan.close != ziet0_close
    assert not ziet1_plan.gogo_calc
    assert not ziet1_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert not ziet1_plan.begin
    assert not ziet1_plan.close
    assert ziet1_plan.gogo_calc == (ziet0_begin * ziet1_numor) / ziet1_denom
    assert ziet1_plan.stop_calc == (ziet0_close * ziet1_numor) / ziet1_denom
    assert ziet1_plan.gogo_calc == 6
    assert ziet1_plan.stop_calc == 15


def test_BeliefUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_belief.make_l1_rope(ziet0_str)
    ziet0_begin = 3
    ziet0_close = 7
    ziet0_plan = planunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_belief.set_l1_plan(ziet0_plan)

    ziet1_str = "ziet1"
    ziet1_addin = 5
    ziet1_rope = yao_belief.make_rope(ziet0_rope, ziet1_str)
    temp_plan = planunit_shop(ziet1_str, addin=ziet1_addin)
    yao_belief.set_plan(temp_plan, ziet0_rope)
    ziet1_plan = yao_belief.get_plan_obj(ziet1_rope)
    root_rope = to_rope(yao_belief.moment_label)
    root_plan = yao_belief.get_plan_obj(root_rope)
    yao_belief._set_plan_dict()
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert ziet0_plan.begin == ziet0_begin
    assert ziet0_plan.close == ziet0_close
    assert ziet1_plan.begin != ziet0_begin
    assert ziet1_plan.close != ziet0_close
    assert ziet1_plan.addin == ziet1_addin
    assert not ziet1_plan.gogo_calc
    assert not ziet1_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert not ziet1_plan.begin
    assert not ziet1_plan.close
    assert ziet1_plan.gogo_calc == ziet0_plan.gogo_calc + ziet1_addin
    assert ziet1_plan.stop_calc == ziet0_plan.stop_calc + ziet1_addin
    assert ziet1_plan.gogo_calc == 8
    assert ziet1_plan.stop_calc == 12


def test_BeliefUnit_set_plantree_range_attrs_Sets2LevelsDescendentPlan_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_belief.make_l1_rope(ziet0_str)
    ziet0_begin = 3
    ziet0_close = 7
    ziet0_plan = planunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_belief.set_l1_plan(ziet0_plan)

    ziet1_str = "ziet1"
    ziet1_rope = yao_belief.make_rope(ziet0_rope, ziet1_str)
    yao_belief.add_plan(ziet1_rope)
    ziet2_str = "ziet2"
    ziet2_rope = yao_belief.make_rope(ziet1_rope, ziet2_str)
    ziet2_addin = 5
    x_ziet2_plan = planunit_shop(ziet2_str, addin=ziet2_addin)
    yao_belief.set_plan(x_ziet2_plan, ziet1_rope)
    ziet2_plan = yao_belief.get_plan_obj(ziet2_rope)
    root_rope = to_rope(yao_belief.moment_label)
    root_plan = yao_belief.get_plan_obj(root_rope)
    yao_belief._set_plan_dict()
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert ziet0_plan.begin == ziet0_begin
    assert ziet0_plan.close == ziet0_close
    assert ziet2_plan.begin != ziet0_begin
    assert ziet2_plan.close != ziet0_close
    assert ziet2_plan.addin == ziet2_addin
    assert not ziet2_plan.gogo_calc
    assert not ziet2_plan.stop_calc
    assert yao_belief._range_inheritors == {}

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert not ziet2_plan.begin
    assert not ziet2_plan.close
    assert ziet2_plan.gogo_calc == ziet0_plan.gogo_calc + ziet2_addin
    assert ziet2_plan.stop_calc == ziet0_plan.stop_calc + ziet2_addin
    assert ziet2_plan.gogo_calc == 8
    assert ziet2_plan.stop_calc == 12
    assert yao_belief._range_inheritors == {
        ziet1_rope: ziet0_rope,
        ziet2_rope: ziet0_rope,
    }


def test_BeliefUnit_set_plantree_range_attrs_SetsDescendentPlan_gogo_calc_stop_calc_LabelWith_denom_addin():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_belief.make_l1_rope(ziet0_str)
    ziet0_begin = 21
    ziet0_close = 35
    ziet0_plan = planunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_belief.set_l1_plan(ziet0_plan)

    ziet1_str = "ziet1"
    ziet1_addin = 70
    ziet1_denom = 7
    ziet1_rope = yao_belief.make_rope(ziet0_rope, ziet1_str)
    temp_plan = planunit_shop(ziet1_str, denom=ziet1_denom, addin=ziet1_addin)
    yao_belief.set_plan(temp_plan, ziet0_rope)
    ziet1_plan = yao_belief.get_plan_obj(ziet1_rope)
    root_rope = to_rope(yao_belief.moment_label)
    root_plan = yao_belief.get_plan_obj(root_rope)
    yao_belief._set_plan_dict()
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert ziet0_plan.begin == ziet0_begin
    assert ziet0_plan.close == ziet0_close
    assert ziet1_plan.begin != ziet0_begin
    assert ziet1_plan.close != ziet0_close
    assert ziet1_plan.addin == ziet1_addin
    assert not ziet1_plan.gogo_calc
    assert not ziet1_plan.stop_calc

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert not ziet1_plan.begin
    assert not ziet1_plan.close
    assert ziet1_plan.gogo_calc == (ziet0_plan.gogo_calc + ziet1_addin) / ziet1_denom
    assert ziet1_plan.stop_calc == (ziet0_plan.stop_calc + ziet1_addin) / ziet1_denom
    assert ziet1_plan.gogo_calc == 13
    assert ziet1_plan.stop_calc == 15


def test_BeliefUnit_set_plantree_range_attrs_SetsDescendentPlan_When_knot_IsNonDefault():
    # ESTABLISH
    slash_str = "/"
    yao_belief = beliefunit_shop("Yao", knot=slash_str)
    root_rope = to_rope(yao_belief.moment_label, knot=slash_str)
    ziet0_str = "ziet0"
    ziet0_rope = yao_belief.make_l1_rope(ziet0_str)
    ziet0_begin = 7
    ziet0_close = 31
    ziet0_plan = planunit_shop(
        ziet0_str, begin=ziet0_begin, close=ziet0_close, knot=slash_str
    )
    yao_belief.set_l1_plan(ziet0_plan)

    ziet1_str = "ziet1"
    ziet1_rope = yao_belief.make_rope(ziet0_rope, ziet1_str)
    yao_belief.set_plan(planunit_shop(ziet1_str), ziet0_rope)
    ziet1_plan = yao_belief.get_plan_obj(ziet1_rope)
    root_plan = yao_belief.get_plan_obj(root_rope)
    yao_belief._set_plan_dict()
    assert not root_plan.gogo_calc
    assert not root_plan.stop_calc
    assert ziet0_plan.begin == ziet0_begin
    assert ziet0_plan.close == ziet0_close
    assert ziet1_plan.begin != ziet0_begin
    assert ziet1_plan.close != ziet0_close
    assert not ziet1_plan.gogo_calc
    assert not ziet1_plan.stop_calc
    assert yao_belief._range_inheritors == {}

    # WHEN
    yao_belief._set_plantree_range_attrs()

    # THEN
    assert ziet1_plan.begin != ziet0_begin
    assert ziet1_plan.close != ziet0_close
    assert not ziet1_plan.begin
    assert not ziet1_plan.close
    assert ziet1_plan.gogo_calc == ziet0_begin
    assert ziet1_plan.stop_calc == ziet0_close
    assert yao_belief._range_inheritors == {ziet1_rope: ziet0_rope}
