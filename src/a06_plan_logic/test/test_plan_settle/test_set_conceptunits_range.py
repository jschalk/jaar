from src.a01_term_logic.rope import to_rope
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.example_plans import (
    get_planunit_with_4_levels_and_2reasons,
)


def test_PlanUnit_set_concepttree_range_attrs_SetsInitialConcept_gogo_calc_stop_calc_UnitDoesNotErrorWithEmptyPlanUnit():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    root_rope = to_rope(yao_plan.bank_label)
    root_concept = yao_plan.get_concept_obj(root_rope)
    assert not root_concept.begin
    assert not root_concept.close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert not root_concept.begin
    assert not root_concept.close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc


def test_PlanUnit_set_concepttree_range_attrs_SetsInitialConcept_gogo_calc_stop_calc_DoesNotErrorWhenNoMathLabels():
    # ESTABLISH
    yao_plan = get_planunit_with_4_levels_and_2reasons()
    root_rope = to_rope(yao_plan.bank_label)
    root_concept = yao_plan.get_concept_obj(root_rope)
    assert not root_concept._gogo_calc

    # WHEM
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert not root_concept._gogo_calc


def test_PlanUnit_set_concepttree_range_attrs_SetsInitialConcept_gogo_calc_stop_calc_SimpleLabel():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    root_rope = to_rope(yao_plan.bank_label)
    time0_begin = 7
    time0_close = 31
    yao_plan.edit_concept_attr(root_rope, begin=time0_begin, close=time0_close)
    yao_plan._set_concept_dict()
    root_concept = yao_plan.get_concept_obj(root_rope)
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert root_concept._gogo_calc == time0_begin
    assert root_concept._stop_calc == time0_close


def test_PlanUnit_set_concepttree_range_attrs_SetsInitialConcept_gogo_calc_stop_calc_LabelWith_denom():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    root_rope = to_rope(yao_plan.bank_label)
    time0_begin = 6
    time0_close = 21
    time0_denom = 3
    yao_plan.edit_concept_attr(
        root_rope,
        begin=time0_begin,
        close=time0_close,
        denom=time0_denom,
    )
    root_concept = yao_plan.get_concept_obj(root_rope)
    yao_plan._set_concept_dict()
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert root_concept.denom == time0_denom
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert root_concept._gogo_calc == time0_begin / time0_denom
    assert root_concept._stop_calc == time0_close / time0_denom
    assert root_concept._gogo_calc == 2
    assert root_concept._stop_calc == 7


def test_PlanUnit_set_concepttree_range_attrs_SetsInitialConcept_gogo_calc_stop_calc_LabelWith_denom_numor():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    root_rope = to_rope(yao_plan.bank_label)
    time0_begin = 6
    time0_close = 18
    time0_numor = 7
    time0_denom = 3
    yao_plan.edit_concept_attr(
        root_rope,
        begin=time0_begin,
        close=time0_close,
        numor=time0_numor,
        denom=time0_denom,
    )
    root_concept = yao_plan.get_concept_obj(root_rope)
    yao_plan._set_concept_dict()
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert root_concept.numor == time0_numor
    assert root_concept.denom == time0_denom
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert root_concept._gogo_calc == (time0_begin * time0_numor) / time0_denom
    assert root_concept._stop_calc == (time0_close * time0_numor) / time0_denom
    assert root_concept._gogo_calc == 14
    assert root_concept._stop_calc == 42


def test_PlanUnit_set_concepttree_range_attrs_SetsInitialConcept_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    root_rope = to_rope(yao_plan.bank_label)
    time0_begin = 6
    time0_close = 18
    time0_addin = 7
    yao_plan.edit_concept_attr(
        root_rope,
        begin=time0_begin,
        close=time0_close,
        addin=time0_addin,
    )
    yao_plan._set_concept_dict()
    root_concept = yao_plan.get_concept_obj(root_rope)
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert root_concept.addin == time0_addin
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert root_concept._gogo_calc == time0_begin + time0_addin
    assert root_concept._stop_calc == time0_close + time0_addin
    assert root_concept._gogo_calc == 13
    assert root_concept._stop_calc == 25


def test_PlanUnit_set_concepttree_range_attrs_SetsInitialConcept_gogo_calc_stop_calc_LabelWith_denom_addin():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    root_rope = to_rope(yao_plan.bank_label)
    time0_begin = 6
    time0_close = 18
    time0_denom = 3
    time0_addin = 60
    yao_plan.edit_concept_attr(
        root_rope,
        begin=time0_begin,
        close=time0_close,
        denom=time0_denom,
        addin=time0_addin,
    )
    yao_plan._set_concept_dict()
    root_concept = yao_plan.get_concept_obj(root_rope)
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert root_concept.denom == time0_denom
    assert root_concept.addin == time0_addin
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert root_concept.begin == time0_begin
    assert root_concept.close == time0_close
    assert root_concept._gogo_calc == (time0_begin + time0_addin) / time0_denom
    assert root_concept._stop_calc == (time0_close + time0_addin) / time0_denom
    assert root_concept._gogo_calc == 22
    assert root_concept._stop_calc == 26


def test_PlanUnit_set_concepttree_range_attrs_SetsDescendentConcept_gogo_calc_stop_calc_Simple0():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    root_rope = to_rope(yao_plan.bank_label)
    time0_str = "time0"
    time0_rope = yao_plan.make_l1_rope(time0_str)
    time0_begin = 7
    time0_close = 31
    time0_concept = conceptunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_plan.set_l1_concept(time0_concept)

    time1_str = "time1"
    time1_rope = yao_plan.make_rope(time0_rope, time1_str)
    yao_plan.set_concept(conceptunit_shop(time1_str), time0_rope)
    time1_concept = yao_plan.get_concept_obj(time1_rope)
    root_concept = yao_plan.get_concept_obj(root_rope)
    yao_plan._set_concept_dict()
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert time0_concept.begin == time0_begin
    assert time0_concept.close == time0_close
    assert time1_concept.begin != time0_begin
    assert time1_concept.close != time0_close
    assert not time1_concept._gogo_calc
    assert not time1_concept._stop_calc
    assert yao_plan._range_inheritors == {}

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert time1_concept.begin != time0_begin
    assert time1_concept.close != time0_close
    assert not time1_concept.begin
    assert not time1_concept.close
    assert time1_concept._gogo_calc == time0_begin
    assert time1_concept._stop_calc == time0_close
    assert yao_plan._range_inheritors == {time1_rope: time0_rope}


def test_PlanUnit_set_concepttree_range_attrs_SetsDescendentConcept_gogo_calc_stop_calc_LabelWith_denom():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_plan.make_l1_rope(time0_str)
    time0_begin = 14
    time0_close = 35
    time0_concept = conceptunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_plan.set_l1_concept(time0_concept)

    time1_str = "time1"
    time1_denom = 7
    time1_rope = yao_plan.make_rope(time0_rope, time1_str)
    yao_plan.set_concept(conceptunit_shop(time1_str, denom=time1_denom), time0_rope)
    time1_concept = yao_plan.get_concept_obj(time1_rope)
    root_rope = to_rope(yao_plan.bank_label)
    root_concept = yao_plan.get_concept_obj(root_rope)
    yao_plan._set_concept_dict()
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert time0_concept.begin == time0_begin
    assert time0_concept.close == time0_close
    assert time1_concept.begin != time0_begin
    assert time1_concept.close != time0_close
    assert not time1_concept._gogo_calc
    assert not time1_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert not time1_concept.begin
    assert not time1_concept.close
    assert time1_concept._gogo_calc == time0_begin / time1_denom
    assert time1_concept._stop_calc == time0_close / time1_denom
    assert time1_concept._gogo_calc == 2
    assert time1_concept._stop_calc == 5


def test_PlanUnit_set_concepttree_range_attrs_SetsDescendentConcept_gogo_calc_stop_calc_LabelWith_denom_numor():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_plan.make_l1_rope(time0_str)
    time0_begin = 14
    time0_close = 35
    time0_concept = conceptunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_plan.set_l1_concept(time0_concept)

    time1_str = "time1"
    time1_denom = 7
    time1_numor = 3
    time1_rope = yao_plan.make_rope(time0_rope, time1_str)
    temp_concept = conceptunit_shop(time1_str, numor=time1_numor, denom=time1_denom)
    yao_plan.set_concept(temp_concept, time0_rope)
    time1_concept = yao_plan.get_concept_obj(time1_rope)
    root_rope = to_rope(yao_plan.bank_label)
    root_concept = yao_plan.get_concept_obj(root_rope)
    yao_plan._set_concept_dict()
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert time0_concept.begin == time0_begin
    assert time0_concept.close == time0_close
    assert time1_concept.begin != time0_begin
    assert time1_concept.close != time0_close
    assert not time1_concept._gogo_calc
    assert not time1_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert not time1_concept.begin
    assert not time1_concept.close
    assert time1_concept._gogo_calc == (time0_begin * time1_numor) / time1_denom
    assert time1_concept._stop_calc == (time0_close * time1_numor) / time1_denom
    assert time1_concept._gogo_calc == 6
    assert time1_concept._stop_calc == 15


def test_PlanUnit_set_concepttree_range_attrs_SetsDescendentConcept_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_plan.make_l1_rope(time0_str)
    time0_begin = 3
    time0_close = 7
    time0_concept = conceptunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_plan.set_l1_concept(time0_concept)

    time1_str = "time1"
    time1_addin = 5
    time1_rope = yao_plan.make_rope(time0_rope, time1_str)
    temp_concept = conceptunit_shop(time1_str, addin=time1_addin)
    yao_plan.set_concept(temp_concept, time0_rope)
    time1_concept = yao_plan.get_concept_obj(time1_rope)
    root_rope = to_rope(yao_plan.bank_label)
    root_concept = yao_plan.get_concept_obj(root_rope)
    yao_plan._set_concept_dict()
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert time0_concept.begin == time0_begin
    assert time0_concept.close == time0_close
    assert time1_concept.begin != time0_begin
    assert time1_concept.close != time0_close
    assert time1_concept.addin == time1_addin
    assert not time1_concept._gogo_calc
    assert not time1_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert not time1_concept.begin
    assert not time1_concept.close
    assert time1_concept._gogo_calc == time0_concept._gogo_calc + time1_addin
    assert time1_concept._stop_calc == time0_concept._stop_calc + time1_addin
    assert time1_concept._gogo_calc == 8
    assert time1_concept._stop_calc == 12


def test_PlanUnit_set_concepttree_range_attrs_Sets2LevelsDescendentConcept_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_plan.make_l1_rope(time0_str)
    time0_begin = 3
    time0_close = 7
    time0_concept = conceptunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_plan.set_l1_concept(time0_concept)

    time1_str = "time1"
    time1_rope = yao_plan.make_rope(time0_rope, time1_str)
    yao_plan.add_concept(time1_rope)
    time2_str = "time2"
    time2_rope = yao_plan.make_rope(time1_rope, time2_str)
    time2_addin = 5
    x_time2_concept = conceptunit_shop(time2_str, addin=time2_addin)
    yao_plan.set_concept(x_time2_concept, time1_rope)
    time2_concept = yao_plan.get_concept_obj(time2_rope)
    root_rope = to_rope(yao_plan.bank_label)
    root_concept = yao_plan.get_concept_obj(root_rope)
    yao_plan._set_concept_dict()
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert time0_concept.begin == time0_begin
    assert time0_concept.close == time0_close
    assert time2_concept.begin != time0_begin
    assert time2_concept.close != time0_close
    assert time2_concept.addin == time2_addin
    assert not time2_concept._gogo_calc
    assert not time2_concept._stop_calc
    assert yao_plan._range_inheritors == {}

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert not time2_concept.begin
    assert not time2_concept.close
    assert time2_concept._gogo_calc == time0_concept._gogo_calc + time2_addin
    assert time2_concept._stop_calc == time0_concept._stop_calc + time2_addin
    assert time2_concept._gogo_calc == 8
    assert time2_concept._stop_calc == 12
    assert yao_plan._range_inheritors == {
        time1_rope: time0_rope,
        time2_rope: time0_rope,
    }


def test_PlanUnit_set_concepttree_range_attrs_SetsDescendentConcept_gogo_calc_stop_calc_LabelWith_denom_addin():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    time0_str = "time0"
    time0_rope = yao_plan.make_l1_rope(time0_str)
    time0_begin = 21
    time0_close = 35
    time0_concept = conceptunit_shop(time0_str, begin=time0_begin, close=time0_close)
    yao_plan.set_l1_concept(time0_concept)

    time1_str = "time1"
    time1_addin = 70
    time1_denom = 7
    time1_rope = yao_plan.make_rope(time0_rope, time1_str)
    temp_concept = conceptunit_shop(time1_str, denom=time1_denom, addin=time1_addin)
    yao_plan.set_concept(temp_concept, time0_rope)
    time1_concept = yao_plan.get_concept_obj(time1_rope)
    root_rope = to_rope(yao_plan.bank_label)
    root_concept = yao_plan.get_concept_obj(root_rope)
    yao_plan._set_concept_dict()
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert time0_concept.begin == time0_begin
    assert time0_concept.close == time0_close
    assert time1_concept.begin != time0_begin
    assert time1_concept.close != time0_close
    assert time1_concept.addin == time1_addin
    assert not time1_concept._gogo_calc
    assert not time1_concept._stop_calc

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert not time1_concept.begin
    assert not time1_concept.close
    assert (
        time1_concept._gogo_calc
        == (time0_concept._gogo_calc + time1_addin) / time1_denom
    )
    assert (
        time1_concept._stop_calc
        == (time0_concept._stop_calc + time1_addin) / time1_denom
    )
    assert time1_concept._gogo_calc == 13
    assert time1_concept._stop_calc == 15


def test_PlanUnit_set_concepttree_range_attrs_SetsDescendentConcept_When_knot_IsNonDefault():
    # ESTABLISH
    slash_str = "/"
    yao_plan = planunit_shop("Yao", knot=slash_str)
    root_rope = to_rope(yao_plan.bank_label, knot=slash_str)
    time0_str = "time0"
    time0_rope = yao_plan.make_l1_rope(time0_str)
    time0_begin = 7
    time0_close = 31
    time0_concept = conceptunit_shop(
        time0_str, begin=time0_begin, close=time0_close, knot=slash_str
    )
    yao_plan.set_l1_concept(time0_concept)

    time1_str = "time1"
    time1_rope = yao_plan.make_rope(time0_rope, time1_str)
    yao_plan.set_concept(conceptunit_shop(time1_str), time0_rope)
    time1_concept = yao_plan.get_concept_obj(time1_rope)
    root_concept = yao_plan.get_concept_obj(root_rope)
    yao_plan._set_concept_dict()
    assert not root_concept._gogo_calc
    assert not root_concept._stop_calc
    assert time0_concept.begin == time0_begin
    assert time0_concept.close == time0_close
    assert time1_concept.begin != time0_begin
    assert time1_concept.close != time0_close
    assert not time1_concept._gogo_calc
    assert not time1_concept._stop_calc
    assert yao_plan._range_inheritors == {}

    # WHEN
    yao_plan._set_concepttree_range_attrs()

    # THEN
    assert time1_concept.begin != time0_begin
    assert time1_concept.close != time0_close
    assert not time1_concept.begin
    assert not time1_concept.close
    assert time1_concept._gogo_calc == time0_begin
    assert time1_concept._stop_calc == time0_close
    assert yao_plan._range_inheritors == {time1_rope: time0_rope}
