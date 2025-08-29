from src.a01_term_logic.rope import create_rope
from src.a03_group_logic.group import awardheir_shop, awardunit_shop
from src.a03_group_logic.labor import laborheir_shop, laborunit_shop
from src.a04_reason_logic.reason import (
    caseunit_shop,
    factheir_shop,
    factunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.a05_plan_logic.plan import (
    get_default_moment_label as root_label,
    planunit_shop,
)


def test_PlanUnit_clear_all_voice_cred_debt_ClearsAttrs():
    # ESTABLISH
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, all_voice_cred=55, all_voice_debt=33)
    assert ball_plan.all_voice_cred == 55
    assert ball_plan.all_voice_debt == 33

    # WHEN
    ball_plan.clear_all_voice_cred_debt()

    # THEN
    assert ball_plan.all_voice_cred is None
    assert ball_plan.all_voice_debt is None


def test_PlanUnit_get_fund_share_ReturnsObj():
    # ESTABLISH
    texas_str = "texas"
    texas_plan = planunit_shop(texas_str, root_label())

    # WHEN / THEN
    assert texas_plan.get_fund_share() == 0

    # WHEN / THEN
    texas_plan.fund_onset = 3
    texas_plan.fund_cease = 14
    assert texas_plan.get_fund_share() == 11


def test_PlanUnit_set_awardunit_SetsAttr():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_planunit = planunit_shop(sport_str)
    assert not sport_planunit.awardunits.get(biker_str)

    # WHEN
    sport_planunit.set_awardunit(awardunit_shop(biker_str))

    # THEN
    assert sport_planunit.awardunits.get(biker_str)


def test_PlanUnit_awardunit_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_planunit = planunit_shop(sport_str)
    assert not sport_planunit.awardunit_exists(biker_str)

    # WHEN
    sport_planunit.set_awardunit(awardunit_shop(biker_str))

    # THEN
    assert sport_planunit.awardunit_exists(biker_str)


def test_PlanUnit_get_awardunit_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_planunit = planunit_shop(sport_str)
    sport_planunit.set_awardunit(awardunit_shop(biker_str))

    # WHEN
    biker_awardunit = sport_planunit.get_awardunit(biker_str)

    # THEN
    assert biker_awardunit
    assert biker_awardunit.awardee_title == biker_str


def test_PlanUnit_set_awardheirs_fund_give_fund_take_SetsAttr_WithValues():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_str = "bikers2"
    biker_awardheir = awardheir_shop(biker_str, biker_give_force, biker_take_force)
    swim_str = "swimmers"
    swim_group_title = swim_str
    swim_give_force = 29
    swim_take_force = 32
    swim_awardheir = awardheir_shop(swim_group_title, swim_give_force, swim_take_force)
    x_awardheirs = {
        swim_awardheir.awardee_title: swim_awardheir,
        biker_awardheir.awardee_title: biker_awardheir,
    }
    sport_str = "sport"
    sport_plan = planunit_shop(sport_str, awardheirs=x_awardheirs)
    assert sport_plan.fund_iota == 1
    assert len(sport_plan.awardheirs) == 2
    swim_awardheir = sport_plan.awardheirs.get(swim_str)
    assert not swim_awardheir.fund_give
    assert not swim_awardheir.fund_take
    biker_awardheir = sport_plan.awardheirs.get(biker_str)
    assert not biker_awardheir.fund_give
    assert not biker_awardheir.fund_take

    # WHEN
    sport_plan.fund_onset = 91
    sport_plan.fund_cease = 820
    sport_plan.set_awardheirs_fund_give_fund_take()

    # THEN
    print(f"{len(sport_plan.awardheirs)=}")
    swim_awardheir = sport_plan.awardheirs.get(swim_str)
    assert swim_awardheir.fund_give == 516
    assert swim_awardheir.fund_take == 496
    biker_awardheir = sport_plan.awardheirs.get(biker_str)
    assert biker_awardheir.fund_give == 213
    assert biker_awardheir.fund_take == 233


def test_PlanUnit_awardheir_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    biker_awardheir = awardheir_shop(biker_str)
    sport_str = "sport"
    sport_planunit = planunit_shop(sport_str)
    assert not sport_planunit.awardheir_exists()

    # WHEN
    sport_planunit.awardheirs[biker_str] = biker_awardheir

    # THEN
    assert sport_planunit.awardheir_exists()


def test_PlanUnit_set_awardheirs_fund_give_fund_take_ReturnsObj_NoValues():
    # ESTABLISH /WHEN
    sport_str = "sport"
    sport_plan = planunit_shop(sport_str)

    # WHEN / THEN
    # does not crash with empty set
    sport_plan.set_awardheirs_fund_give_fund_take()


def test_PlanUnit_set_reasonheirsAcceptsNewValues():
    # ESTABLISH
    ball_str = "ball"
    ball_rope = create_rope(ball_str)
    run_str = "run"
    run_rope = create_rope(ball_rope, run_str)
    ball_plan = planunit_shop(ball_str)
    run_case = caseunit_shop(reason_state=run_rope, reason_lower=0, reason_upper=7)
    run_cases = {run_case.reason_state: run_case}
    reasonheir = reasonheir_shop(run_rope, cases=run_cases)
    reasonheirs = {reasonheir.reason_context: reasonheir}
    assert ball_plan.reasonheirs == {}

    # WHEN
    ball_plan.set_reasonheirs(reasonheirs=reasonheirs, belief_plan_dict={})

    # THEN
    assert ball_plan.reasonheirs == reasonheirs
    assert id(ball_plan.reasonheirs) != id(reasonheirs)


def test_PlanUnit_set_reasonheirsRefusesNewValues():
    # ESTABLISH
    ball_str = "ball"
    ball_rope = create_rope(ball_str)
    run_str = "run"
    run_rope = create_rope(ball_rope, run_str)
    run_case = caseunit_shop(reason_state=run_rope, reason_lower=0, reason_upper=7)
    run_cases = {run_case.reason_state: run_case}
    run_reasonunit = reasonunit_shop(reason_context=run_rope, cases=run_cases)
    run_reasonunits = {run_reasonunit.reason_context: run_reasonunit}
    ball_plan = planunit_shop(ball_str, reasonunits=run_reasonunits)
    assert ball_plan.reasonunits != {}

    # WHEN
    ball_plan.set_reasonheirs(reasonheirs={}, belief_plan_dict={})

    # THEN
    reasonheir = reasonheir_shop(run_rope, cases=run_cases)
    reasonheirs = {reasonheir.reason_context: reasonheir}
    assert ball_plan.reasonheirs == reasonheirs


def test_PlanUnit_set_range_factheirs_SetsAttrNoParameters():
    # ESTABLISH
    ball_plan = planunit_shop("ball")
    assert ball_plan.factheirs == {}

    # WHEN
    ball_plan.set_range_factheirs(belief_plan_dict={}, range_inheritors={})

    # THEN
    assert ball_plan.factheirs == {}


def test_PlanUnit_set_range_factheirs_SetsAttrNewFactHeir():
    # ESTABLISH
    wk_str = "wk"
    wk_rope = create_rope(root_label(), wk_str)
    wk_reason_lower = 3
    wk_reason_upper = 7
    wk_addin = 10
    wk_plan = planunit_shop(wk_str, parent_rope=root_label(), addin=wk_addin)
    wk_factheir = factheir_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)
    tue_str = "Tue"
    tue_rope = create_rope(wk_rope, tue_str)
    tue_addin = 100
    tue_plan = planunit_shop(tue_str, parent_rope=wk_rope, addin=tue_addin)
    ball_str = "ball"
    ball_rope = create_rope(root_label(), ball_str)
    ball_plan = planunit_shop(ball_str)
    ball_plan._set_factheir(wk_factheir)
    tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    x_belief_plan_dict = {
        wk_plan.get_plan_rope(): wk_plan,
        tue_plan.get_plan_rope(): tue_plan,
    }
    ball_plan.set_reasonheirs(x_belief_plan_dict, tue_reasonheirs)

    x_range_inheritors = {tue_rope: wk_rope}
    assert len(ball_plan.reasonheirs) == 1
    assert ball_plan.factheirs == {wk_rope: wk_factheir}
    assert ball_plan.factheirs.get(wk_rope)
    assert len(ball_plan.factheirs) == 1
    assert ball_plan.factheirs.get(tue_rope) is None

    # WHEN
    ball_plan.set_range_factheirs(x_belief_plan_dict, x_range_inheritors)

    # THEN
    tue_reason_lower = 113
    tue_reason_upper = 117
    tue_factheir = factheir_shop(tue_rope, tue_rope, tue_reason_lower, tue_reason_upper)
    assert len(ball_plan.factheirs) == 2
    assert ball_plan.factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}


def test_PlanUnit_set_reasonunit_SetsAttr():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_plan.reasonunits.get(dirty_str)

    # WHEN
    clean_plan.set_reasonunit(reasonunit_shop(reason_context=dirty_str))

    # THEN
    assert clean_plan.reasonunits.get(dirty_str)
    x_reasonunit = clean_plan.get_reasonunit(reason_context=dirty_str)
    assert x_reasonunit is not None
    assert x_reasonunit.reason_context == dirty_str


def test_PlanUnit_reasonunit_exists_ReturnsObj():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_plan.reasonunit_exists(dirty_str)

    # WHEN
    clean_plan.set_reasonunit(reasonunit_shop(reason_context=dirty_str))

    # THEN
    assert clean_plan.reasonunit_exists(dirty_str)


def test_PlanUnit_get_reasonunit_ReturnsObj():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    dirty_str = "dirty"
    clean_plan.set_reasonunit(reasonunit_shop(reason_context=dirty_str))

    # WHEN
    x_reasonunit = clean_plan.get_reasonunit(reason_context=dirty_str)

    # THEN
    assert x_reasonunit is not None
    assert x_reasonunit.reason_context == dirty_str


def test_PlanUnit_get_reasonheir_ReturnsObj():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    dirty_str = "dirty"
    x_reasonheir = reasonheir_shop(reason_context=dirty_str)
    x_reasonheirs = {x_reasonheir.reason_context: x_reasonheir}
    clean_plan.set_reasonheirs(reasonheirs=x_reasonheirs, belief_plan_dict={})

    # WHEN
    z_reasonheir = clean_plan.get_reasonheir(reason_context=dirty_str)

    # THEN
    assert z_reasonheir is not None
    assert z_reasonheir.reason_context == dirty_str


def test_PlanUnit_get_reasonheir_ReturnsNone():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    dirty_str = "dirty"
    x_reasonheir = reasonheir_shop(dirty_str)
    x_reasonheirs = {x_reasonheir.reason_context: x_reasonheir}
    clean_plan.set_reasonheirs(reasonheirs=x_reasonheirs, belief_plan_dict={})

    # WHEN
    test6_str = "test6"
    reason_heir_test6 = clean_plan.get_reasonheir(reason_context=test6_str)

    # THEN
    assert reason_heir_test6 is None


def test_PlanUnit_set_active_attrs_SetsNullactive_hxToNonEmpty():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    assert clean_plan.active_hx == {}

    # WHEN
    clean_plan.set_active_attrs(tree_traverse_count=3)
    # THEN
    assert clean_plan.active_hx == {3: True}


def test_PlanUnit_set_active_attrs_IfFullactive_hxResetToTrue():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    clean_plan.active_hx = {0: True, 4: False}
    assert clean_plan.active_hx != {0: True}
    # WHEN
    clean_plan.set_active_attrs(tree_traverse_count=0)
    # THEN
    assert clean_plan.active_hx == {0: True}


def test_PlanUnit_set_factunit_SetsAttr():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_plan.factunits.get(dirty_str)

    # WHEN
    clean_plan.set_factunit(factunit_shop(fact_context=dirty_str))

    # THEN
    assert clean_plan.factunits.get(dirty_str)


def test_PlanUnit_factunit_exists_ReturnsObj():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_plan.factunit_exists(dirty_str)

    # WHEN
    clean_plan.set_factunit(factunit_shop(fact_context=dirty_str))

    # THEN
    assert clean_plan.factunit_exists(dirty_str)


# def test_PlanUnit_set_active_attrs_IfFullactive_hxResetToFalse():
#     # ESTABLISH
# clean_str = "clean"
# clean_plan = planunit_shop(clean_str)
#     clean_plan.set_reason_case(
#         reason_context="testing1,sec",
#         case="testing1,sec,next",
#         reason_lower=None,
#         reason_upper=None,
#         reason_divisor=None,
#     )
#     clean_plan.active_hx = {0: True, 4: False}
#     assert clean_plan.active_hx != {0: False}
#     # WHEN
#     clean_plan.set_active_attrs(tree_traverse_count=0)
#     # THEN
#     assert clean_plan.active_hx == {0: False}


def test_PlanUnit_record_active_hx_Sets_active_hx():
    # ESTABLISH
    clean_str = "clean"
    clean_plan = planunit_shop(clean_str)
    assert clean_plan.active_hx == {}

    # WHEN
    clean_plan.record_active_hx(0, prev_active=None, now_active=True)
    # THEN
    assert clean_plan.active_hx == {0: True}

    # WHEN
    clean_plan.record_active_hx(1, prev_active=True, now_active=True)
    # THEN
    assert clean_plan.active_hx == {0: True}

    # WHEN
    clean_plan.record_active_hx(2, prev_active=True, now_active=False)
    # THEN
    assert clean_plan.active_hx == {0: True, 2: False}

    # WHEN
    clean_plan.record_active_hx(3, prev_active=False, now_active=False)
    # THEN
    assert clean_plan.active_hx == {0: True, 2: False}

    # WHEN
    clean_plan.record_active_hx(4, prev_active=False, now_active=True)
    # THEN
    assert clean_plan.active_hx == {0: True, 2: False, 4: True}

    # WHEN
    clean_plan.record_active_hx(0, prev_active=False, now_active=False)
    # THEN
    assert clean_plan.active_hx == {0: False}


def test_PlanUnit_set_laborunit_empty_if_None():
    # ESTABLISH
    run_str = "run"
    run_plan = planunit_shop(run_str)
    run_plan.laborunit = None
    assert run_plan.laborunit is None

    # WHEN
    run_plan.set_laborunit_empty_if_None()

    # THEN
    assert run_plan.laborunit is not None
    assert run_plan.laborunit == laborunit_shop()


def test_PlanUnit_set_laborheir_SetsAttr():
    # ESTABLISH
    swim_str = "swimmers"
    sport_str = "sports"
    sport_plan = planunit_shop(sport_str)
    sport_plan.laborunit.add_party(party_title=swim_str)
    # assert sport_plan.laborheir is None

    # WHEN
    sport_plan.set_laborheir(parent_laborheir=None, groupunits=None)

    # THEN
    assert sport_plan.laborheir is not None
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=swim_str)
    swim_laborheir = laborheir_shop()
    swim_laborheir.set_partys(
        laborunit=swim_laborunit, parent_laborheir=None, groupunits=None
    )
    assert sport_plan.laborheir == swim_laborheir
