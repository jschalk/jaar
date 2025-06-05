from src.a01_term_logic.way import create_way
from src.a03_group_logic.group import awardheir_shop, awardlink_shop
from src.a04_reason_logic.reason_concept import (
    factheir_shop,
    factunit_shop,
    premiseunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.a04_reason_logic.reason_labor import laborheir_shop, laborunit_shop
from src.a05_concept_logic.concept import (
    conceptunit_shop,
    get_default_vow_label as root_label,
)


def test_ConceptUnit_clear_all_acct_cred_debt_ClearsCorrectly():
    # ESTABLISH
    ball_str = "ball"
    ball_concept = conceptunit_shop(ball_str, _all_acct_cred=55, _all_acct_debt=33)
    assert ball_concept._all_acct_cred == 55
    assert ball_concept._all_acct_debt == 33

    # WHEN
    ball_concept.clear_all_acct_cred_debt()

    # THEN
    assert ball_concept._all_acct_cred is None
    assert ball_concept._all_acct_debt is None


def test_ConceptUnit_get_fund_share_ReturnsObj():
    # ESTABLISH
    texas_str = "texas"
    texas_concept = conceptunit_shop(texas_str, root_label())

    # WHEN / THEN
    assert texas_concept.get_fund_share() == 0

    # WHEN / THEN
    texas_concept._fund_onset = 3
    texas_concept._fund_cease = 14
    assert texas_concept.get_fund_share() == 11


def test_ConceptUnit_set_awardlink_SetsAttr():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_conceptunit = conceptunit_shop(sport_str)
    assert not sport_conceptunit.awardlinks.get(biker_str)

    # WHEN
    sport_conceptunit.set_awardlink(awardlink_shop(biker_str))

    # THEN
    assert sport_conceptunit.awardlinks.get(biker_str)


def test_ConceptUnit_awardlink_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_conceptunit = conceptunit_shop(sport_str)
    assert not sport_conceptunit.awardlink_exists(biker_str)

    # WHEN
    sport_conceptunit.set_awardlink(awardlink_shop(biker_str))

    # THEN
    assert sport_conceptunit.awardlink_exists(biker_str)


def test_ConceptUnit_get_awardlink_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_conceptunit = conceptunit_shop(sport_str)
    sport_conceptunit.set_awardlink(awardlink_shop(biker_str))

    # WHEN
    biker_awardlink = sport_conceptunit.get_awardlink(biker_str)

    # THEN
    assert biker_awardlink
    assert biker_awardlink.awardee_title == biker_str


def test_ConceptUnit_set_awardheirs_fund_give_fund_take_SetsAttrCorrectly_WithValues():
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
    sport_concept = conceptunit_shop(sport_str, _awardheirs=x_awardheirs)
    assert sport_concept.fund_iota == 1
    assert len(sport_concept._awardheirs) == 2
    swim_awardheir = sport_concept._awardheirs.get(swim_str)
    assert not swim_awardheir._fund_give
    assert not swim_awardheir._fund_take
    biker_awardheir = sport_concept._awardheirs.get(biker_str)
    assert not biker_awardheir._fund_give
    assert not biker_awardheir._fund_take

    # WHEN
    sport_concept._fund_onset = 91
    sport_concept._fund_cease = 820
    sport_concept.set_awardheirs_fund_give_fund_take()

    # THEN
    print(f"{len(sport_concept._awardheirs)=}")
    swim_awardheir = sport_concept._awardheirs.get(swim_str)
    assert swim_awardheir._fund_give == 516
    assert swim_awardheir._fund_take == 496
    biker_awardheir = sport_concept._awardheirs.get(biker_str)
    assert biker_awardheir._fund_give == 213
    assert biker_awardheir._fund_take == 233


def test_ConceptUnit_awardheir_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    biker_awardheir = awardheir_shop(biker_str)
    sport_str = "sport"
    sport_conceptunit = conceptunit_shop(sport_str)
    assert not sport_conceptunit.awardheir_exists()

    # WHEN
    sport_conceptunit._awardheirs[biker_str] = biker_awardheir

    # THEN
    assert sport_conceptunit.awardheir_exists()


def test_ConceptUnit_set_awardheirs_fund_give_fund_take_ReturnsObj_NoValues():
    # ESTABLISH /WHEN
    sport_str = "sport"
    sport_concept = conceptunit_shop(sport_str)

    # WHEN / THEN
    # does not crash with empty set
    sport_concept.set_awardheirs_fund_give_fund_take()


def test_ConceptUnit_set_reasonheirs_CorrectlyAcceptsNewValues():
    # ESTABLISH
    ball_str = "ball"
    ball_way = create_way(ball_str)
    run_str = "run"
    run_way = create_way(ball_way, run_str)
    ball_concept = conceptunit_shop(ball_str)
    run_premise = premiseunit_shop(pstate=run_way, popen=0, pnigh=7)
    run_premises = {run_premise.pstate: run_premise}
    reasonheir = reasonheir_shop(run_way, premises=run_premises)
    reasonheirs = {reasonheir.rcontext: reasonheir}
    assert ball_concept._reasonheirs == {}

    # WHEN
    ball_concept.set_reasonheirs(reasonheirs=reasonheirs, bud_concept_dict={})

    # THEN
    assert ball_concept._reasonheirs == reasonheirs
    assert id(ball_concept._reasonheirs) != id(reasonheirs)


def test_ConceptUnit_set_reasonheirs_CorrectlyRefusesNewValues():
    # ESTABLISH
    ball_str = "ball"
    ball_way = create_way(ball_str)
    run_str = "run"
    run_way = create_way(ball_way, run_str)
    run_premise = premiseunit_shop(pstate=run_way, popen=0, pnigh=7)
    run_premises = {run_premise.pstate: run_premise}
    run_reasonunit = reasonunit_shop(rcontext=run_way, premises=run_premises)
    run_reasonunits = {run_reasonunit.rcontext: run_reasonunit}
    ball_concept = conceptunit_shop(ball_str, reasonunits=run_reasonunits)
    assert ball_concept.reasonunits != {}

    # WHEN
    ball_concept.set_reasonheirs(reasonheirs={}, bud_concept_dict={})

    # THEN
    reasonheir = reasonheir_shop(run_way, premises=run_premises)
    reasonheirs = {reasonheir.rcontext: reasonheir}
    assert ball_concept._reasonheirs == reasonheirs


def test_ConceptUnit_set_range_factheirs_SetsAttrNoParameters():
    # ESTABLISH
    ball_concept = conceptunit_shop("ball")
    assert ball_concept._factheirs == {}

    # WHEN
    ball_concept.set_range_factheirs(bud_concept_dict={}, range_inheritors={})

    # THEN
    assert ball_concept._factheirs == {}


def test_ConceptUnit_set_range_factheirs_SetsAttrNewFactHeir():
    # ESTABLISH
    wk_str = "wk"
    wk_way = create_way(root_label(), wk_str)
    wk_popen = 3
    wk_pnigh = 7
    wk_addin = 10
    wk_concept = conceptunit_shop(wk_str, parent_way=root_label(), addin=wk_addin)
    wk_factheir = factheir_shop(wk_way, wk_way, wk_popen, wk_pnigh)
    tue_str = "Tue"
    tue_way = create_way(wk_way, tue_str)
    tue_addin = 100
    tue_concept = conceptunit_shop(tue_str, parent_way=wk_way, addin=tue_addin)
    ball_str = "ball"
    ball_way = create_way(root_label(), ball_str)
    ball_concept = conceptunit_shop(ball_str)
    ball_concept._set_factheir(wk_factheir)
    tue_reasonheirs = {tue_way: reasonheir_shop(tue_way, None, False)}
    x_bud_concept_dict = {
        wk_concept.get_concept_way(): wk_concept,
        tue_concept.get_concept_way(): tue_concept,
    }
    ball_concept.set_reasonheirs(x_bud_concept_dict, tue_reasonheirs)

    x_range_inheritors = {tue_way: wk_way}
    assert len(ball_concept._reasonheirs) == 1
    assert ball_concept._factheirs == {wk_way: wk_factheir}
    assert ball_concept._factheirs.get(wk_way)
    assert len(ball_concept._factheirs) == 1
    assert ball_concept._factheirs.get(tue_way) is None

    # WHEN
    ball_concept.set_range_factheirs(x_bud_concept_dict, x_range_inheritors)

    # THEN
    tue_popen = 113
    tue_pnigh = 117
    tue_factheir = factheir_shop(tue_way, tue_way, tue_popen, tue_pnigh)
    assert len(ball_concept._factheirs) == 2
    assert ball_concept._factheirs == {tue_way: tue_factheir, wk_way: wk_factheir}


def test_ConceptUnit_set_reasonunit_SetsAttr():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_concept.reasonunits.get(dirty_str)

    # WHEN
    clean_concept.set_reasonunit(reasonunit_shop(rcontext=dirty_str))

    # THEN
    assert clean_concept.reasonunits.get(dirty_str)
    x_reasonunit = clean_concept.get_reasonunit(rcontext=dirty_str)
    assert x_reasonunit is not None
    assert x_reasonunit.rcontext == dirty_str


def test_ConceptUnit_reasonunit_exists_ReturnsObj():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_concept.reasonunit_exists(dirty_str)

    # WHEN
    clean_concept.set_reasonunit(reasonunit_shop(rcontext=dirty_str))

    # THEN
    assert clean_concept.reasonunit_exists(dirty_str)


def test_ConceptUnit_get_reasonunit_ReturnsObj():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    dirty_str = "dirty"
    clean_concept.set_reasonunit(reasonunit_shop(rcontext=dirty_str))

    # WHEN
    x_reasonunit = clean_concept.get_reasonunit(rcontext=dirty_str)

    # THEN
    assert x_reasonunit is not None
    assert x_reasonunit.rcontext == dirty_str


def test_ConceptUnit_get_reasonheir_ReturnsObj():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    dirty_str = "dirty"
    x_reasonheir = reasonheir_shop(rcontext=dirty_str)
    x_reasonheirs = {x_reasonheir.rcontext: x_reasonheir}
    clean_concept.set_reasonheirs(reasonheirs=x_reasonheirs, bud_concept_dict={})

    # WHEN
    z_reasonheir = clean_concept.get_reasonheir(rcontext=dirty_str)

    # THEN
    assert z_reasonheir is not None
    assert z_reasonheir.rcontext == dirty_str


def test_ConceptUnit_get_reasonheir_ReturnsNone():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    dirty_str = "dirty"
    x_reasonheir = reasonheir_shop(dirty_str)
    x_reasonheirs = {x_reasonheir.rcontext: x_reasonheir}
    clean_concept.set_reasonheirs(reasonheirs=x_reasonheirs, bud_concept_dict={})

    # WHEN
    test6_str = "test6"
    reason_heir_test6 = clean_concept.get_reasonheir(rcontext=test6_str)

    # THEN
    assert reason_heir_test6 is None


def test_ConceptUnit_set_active_attrs_SetsNullactive_hxToNonEmpty():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    assert clean_concept._active_hx == {}

    # WHEN
    clean_concept.set_active_attrs(tree_traverse_count=3)
    # THEN
    assert clean_concept._active_hx == {3: True}


def test_ConceptUnit_set_active_attrs_IfFullactive_hxResetToTrue():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    clean_concept._active_hx = {0: True, 4: False}
    assert clean_concept._active_hx != {0: True}
    # WHEN
    clean_concept.set_active_attrs(tree_traverse_count=0)
    # THEN
    assert clean_concept._active_hx == {0: True}


def test_ConceptUnit_set_factunit_SetsAttr():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_concept.factunits.get(dirty_str)

    # WHEN
    clean_concept.set_factunit(factunit_shop(fcontext=dirty_str))

    # THEN
    assert clean_concept.factunits.get(dirty_str)


def test_ConceptUnit_factunit_exists_ReturnsObj():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_concept.factunit_exists(dirty_str)

    # WHEN
    clean_concept.set_factunit(factunit_shop(fcontext=dirty_str))

    # THEN
    assert clean_concept.factunit_exists(dirty_str)


# def test_ConceptUnit_set_active_attrs_IfFullactive_hxResetToFalse():
#     # ESTABLISH
# clean_str = "clean"
# clean_concept = conceptunit_shop(clean_str)
#     clean_concept.set_reason_premise(
#         rcontext="testing1,sec",
#         premise="testing1,sec,next",
#         popen=None,
#         pnigh=None,
#         pdivisor=None,
#     )
#     clean_concept._active_hx = {0: True, 4: False}
#     assert clean_concept._active_hx != {0: False}
#     # WHEN
#     clean_concept.set_active_attrs(tree_traverse_count=0)
#     # THEN
#     assert clean_concept._active_hx == {0: False}


def test_ConceptUnit_record_active_hx_CorrectlyRecordsHistorry():
    # ESTABLISH
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    assert clean_concept._active_hx == {}

    # WHEN
    clean_concept.record_active_hx(0, prev_active=None, now_active=True)
    # THEN
    assert clean_concept._active_hx == {0: True}

    # WHEN
    clean_concept.record_active_hx(1, prev_active=True, now_active=True)
    # THEN
    assert clean_concept._active_hx == {0: True}

    # WHEN
    clean_concept.record_active_hx(2, prev_active=True, now_active=False)
    # THEN
    assert clean_concept._active_hx == {0: True, 2: False}

    # WHEN
    clean_concept.record_active_hx(3, prev_active=False, now_active=False)
    # THEN
    assert clean_concept._active_hx == {0: True, 2: False}

    # WHEN
    clean_concept.record_active_hx(4, prev_active=False, now_active=True)
    # THEN
    assert clean_concept._active_hx == {0: True, 2: False, 4: True}

    # WHEN
    clean_concept.record_active_hx(0, prev_active=False, now_active=False)
    # THEN
    assert clean_concept._active_hx == {0: False}


def test_ConceptUnit_set_laborunit_empty_if_None():
    # ESTABLISH
    run_str = "run"
    run_concept = conceptunit_shop(run_str)
    run_concept.laborunit = None
    assert run_concept.laborunit is None

    # WHEN
    run_concept.set_laborunit_empty_if_None()

    # THEN
    assert run_concept.laborunit is not None
    assert run_concept.laborunit == laborunit_shop()


def test_ConceptUnit_set_laborheir_CorrectlySetsAttr():
    # ESTABLISH
    swim_str = "swimmers"
    sport_str = "sports"
    sport_concept = conceptunit_shop(sport_str)
    sport_concept.laborunit.set_laborlink(labor_title=swim_str)
    # assert sport_concept._laborheir is None

    # WHEN
    sport_concept.set_laborheir(parent_laborheir=None, groupunits=None)

    # THEN
    assert sport_concept._laborheir is not None
    swim_laborunit = laborunit_shop()
    swim_laborunit.set_laborlink(labor_title=swim_str)
    swim_laborheir = laborheir_shop()
    swim_laborheir.set_laborlinks(
        laborunit=swim_laborunit, parent_laborheir=None, groupunits=None
    )
    assert sport_concept._laborheir == swim_laborheir
