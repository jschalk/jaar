from src._road.road import get_default_real_id_roadnode as root_label, create_road
from src.bud.group import awardheir_shop, awardlink_shop
from src.bud.reason_idea import (
    reasonunit_shop,
    reasonheir_shop,
    premiseunit_shop,
    factheir_shop,
    factunit_shop,
)
from src.bud.reason_team import teamunit_shop, teamheir_shop
from src.bud.idea import ideaunit_shop


def test_IdeaUnit_clear_all_acct_cred_debt_ClearsCorrectly():
    # ESTABLISH
    ball_text = "ball"
    ball_idea = ideaunit_shop(ball_text, _all_acct_cred=55, _all_acct_debt=33)
    assert ball_idea._all_acct_cred == 55
    assert ball_idea._all_acct_debt == 33

    # WHEN
    ball_idea.clear_all_acct_cred_debt()

    # THEN
    assert ball_idea._all_acct_cred is None
    assert ball_idea._all_acct_debt is None


def test_IdeaUnit_get_fund_share_ReturnsObj():
    # ESTABLISH
    texas_text = "texas"
    texas_idea = ideaunit_shop(texas_text, root_label())

    # WHEN / THEN
    assert texas_idea.get_fund_share() == 0

    # WHEN / THEN
    texas_idea._fund_onset = 3
    texas_idea._fund_cease = 14
    assert texas_idea.get_fund_share() == 11


def test_IdeaUnit_set_awardlink_SetsAttr():
    # ESTABLISH
    biker_text = "bikers2"
    sport_text = "sport"
    sport_ideaunit = ideaunit_shop(sport_text)
    assert not sport_ideaunit.awardlinks.get(biker_text)

    # WHEN
    sport_ideaunit.set_awardlink(awardlink_shop(biker_text))

    # THEN
    assert sport_ideaunit.awardlinks.get(biker_text)


def test_IdeaUnit_awardlink_exists_ReturnsObj():
    # ESTABLISH
    biker_text = "bikers2"
    sport_text = "sport"
    sport_ideaunit = ideaunit_shop(sport_text)
    assert not sport_ideaunit.awardlink_exists(biker_text)

    # WHEN
    sport_ideaunit.set_awardlink(awardlink_shop(biker_text))

    # THEN
    assert sport_ideaunit.awardlink_exists(biker_text)


def test_IdeaUnit_get_awardlink_ReturnsObj():
    # ESTABLISH
    biker_text = "bikers2"
    sport_text = "sport"
    sport_ideaunit = ideaunit_shop(sport_text)
    sport_ideaunit.set_awardlink(awardlink_shop(biker_text))

    # WHEN
    biker_awardlink = sport_ideaunit.get_awardlink(biker_text)

    # THEN
    assert biker_awardlink
    assert biker_awardlink.group_id == biker_text


def test_IdeaUnit_set_awardheirs_fund_give_fund_take_SetsAttrCorrectly_WithValues():
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_text = "bikers2"
    biker_awardheir = awardheir_shop(biker_text, biker_give_force, biker_take_force)
    swim_text = "swimmers"
    swim_group_id = swim_text
    swim_give_force = 29
    swim_take_force = 32
    swim_awardheir = awardheir_shop(swim_group_id, swim_give_force, swim_take_force)
    x_awardheirs = {
        swim_awardheir.group_id: swim_awardheir,
        biker_awardheir.group_id: biker_awardheir,
    }
    sport_text = "sport"
    sport_idea = ideaunit_shop(sport_text, _awardheirs=x_awardheirs)
    assert sport_idea._fund_coin == 1
    assert len(sport_idea._awardheirs) == 2
    swim_awardheir = sport_idea._awardheirs.get(swim_text)
    assert not swim_awardheir._fund_give
    assert not swim_awardheir._fund_take
    biker_awardheir = sport_idea._awardheirs.get(biker_text)
    assert not biker_awardheir._fund_give
    assert not biker_awardheir._fund_take

    # WHEN
    sport_idea._fund_onset = 91
    sport_idea._fund_cease = 820
    sport_idea.set_awardheirs_fund_give_fund_take()

    # THEN
    print(f"{len(sport_idea._awardheirs)=}")
    swim_awardheir = sport_idea._awardheirs.get(swim_text)
    assert swim_awardheir._fund_give == 516
    assert swim_awardheir._fund_take == 496
    biker_awardheir = sport_idea._awardheirs.get(biker_text)
    assert biker_awardheir._fund_give == 213
    assert biker_awardheir._fund_take == 233


def test_IdeaUnit_awardheir_exists_ReturnsObj():
    # ESTABLISH
    biker_text = "bikers2"
    biker_awardheir = awardheir_shop(biker_text)
    sport_text = "sport"
    sport_ideaunit = ideaunit_shop(sport_text)
    assert not sport_ideaunit.awardheir_exists()

    # WHEN
    sport_ideaunit._awardheirs[biker_text] = biker_awardheir

    # THEN
    assert sport_ideaunit.awardheir_exists()


def test_IdeaUnit_set_awardheirs_fund_give_fund_take_ReturnsCorrectObj_NoValues():
    # ESTABLISH /WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(sport_text)

    # WHEN / THEN
    # does not crash with empty set
    sport_idea.set_awardheirs_fund_give_fund_take()


def test_IdeaUnit_set_reasonheirs_CorrectlyAcceptsChanges():
    # ESTABLISH
    ball_text = "ball"
    ball_road = create_road(ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    ball_idea = ideaunit_shop(ball_text)
    run_premise = premiseunit_shop(need=run_road, open=0, nigh=7)
    run_premises = {run_premise.need: run_premise}
    reasonheir = reasonheir_shop(run_road, premises=run_premises)
    reasonheirs = {reasonheir.base: reasonheir}
    assert ball_idea._reasonheirs == {}

    # WHEN
    ball_idea.set_reasonheirs(reasonheirs=reasonheirs, bud_idea_dict={})

    # THEN
    assert ball_idea._reasonheirs == reasonheirs
    assert id(ball_idea._reasonheirs) != id(reasonheirs)


def test_IdeaUnit_set_reasonheirs_CorrectlyRefusesChanges():
    # ESTABLISH
    ball_text = "ball"
    ball_road = create_road(ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    run_premise = premiseunit_shop(need=run_road, open=0, nigh=7)
    run_premises = {run_premise.need: run_premise}
    run_reasonunit = reasonunit_shop(base=run_road, premises=run_premises)
    run_reasonunits = {run_reasonunit.base: run_reasonunit}
    ball_idea = ideaunit_shop(ball_text, reasonunits=run_reasonunits)
    assert ball_idea.reasonunits != {}

    # WHEN
    ball_idea.set_reasonheirs(reasonheirs={}, bud_idea_dict={})

    # THEN
    reasonheir = reasonheir_shop(run_road, premises=run_premises)
    reasonheirs = {reasonheir.base: reasonheir}
    assert ball_idea._reasonheirs == reasonheirs


def test_IdeaUnit_set_range_factheirs_SetsAttrNoParameters():
    # ESTABLISH
    ball_idea = ideaunit_shop("ball")
    assert ball_idea._factheirs == {}

    # WHEN
    ball_idea.set_range_factheirs(bud_idea_dict={}, range_inheritors={})

    # THEN
    assert ball_idea._factheirs == {}


def test_IdeaUnit_set_range_factheirs_SetsAttrNewFactHeir():
    # ESTABLISH
    week_text = "week"
    week_road = create_road(root_label(), week_text)
    week_open = 3
    week_nigh = 7
    week_addin = 10
    week_idea = ideaunit_shop(week_text, _parent_road=root_label(), addin=week_addin)
    week_factheir = factheir_shop(week_road, week_road, week_open, week_nigh)
    tue_text = "Tue"
    tue_road = create_road(week_road, tue_text)
    tue_addin = 100
    tue_idea = ideaunit_shop(tue_text, _parent_road=week_road, addin=tue_addin)
    ball_text = "ball"
    ball_road = create_road(root_label(), ball_text)
    ball_idea = ideaunit_shop(ball_text)
    ball_idea._set_factheir(week_factheir)
    tue_reasonheirs = {tue_road: reasonheir_shop(tue_road, None, False)}
    x_bud_idea_dict = {week_idea.get_road(): week_idea, tue_idea.get_road(): tue_idea}
    ball_idea.set_reasonheirs(x_bud_idea_dict, tue_reasonheirs)

    x_range_inheritors = {tue_road: week_road}
    assert len(ball_idea._reasonheirs) == 1
    assert ball_idea._factheirs == {week_road: week_factheir}
    assert ball_idea._factheirs.get(week_road)
    assert len(ball_idea._factheirs) == 1
    assert ball_idea._factheirs.get(tue_road) is None

    # WHEN
    ball_idea.set_range_factheirs(x_bud_idea_dict, x_range_inheritors)

    # THEN
    tue_open = 113
    tue_nigh = 117
    tue_factheir = factheir_shop(tue_road, tue_road, tue_open, tue_nigh)
    assert len(ball_idea._factheirs) == 2
    assert ball_idea._factheirs == {tue_road: tue_factheir, week_road: week_factheir}


def test_IdeaUnit_set_reasonunit_SetsAttr():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    dirty_text = "dirty"
    assert not clean_idea.reasonunits.get(dirty_text)

    # WHEN
    clean_idea.set_reasonunit(reasonunit_shop(base=dirty_text))

    # THEN
    assert clean_idea.reasonunits.get(dirty_text)
    x_reasonunit = clean_idea.get_reasonunit(base=dirty_text)
    assert x_reasonunit is not None
    assert x_reasonunit.base == dirty_text


def test_IdeaUnit_reasonunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    dirty_text = "dirty"
    assert not clean_idea.reasonunit_exists(dirty_text)

    # WHEN
    clean_idea.set_reasonunit(reasonunit_shop(base=dirty_text))

    # THEN
    assert clean_idea.reasonunit_exists(dirty_text)


def test_IdeaUnit_get_reasonunit_ReturnsCorrectObj():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    dirty_text = "dirty"
    clean_idea.set_reasonunit(reasonunit_shop(base=dirty_text))

    # WHEN
    x_reasonunit = clean_idea.get_reasonunit(base=dirty_text)

    # THEN
    assert x_reasonunit is not None
    assert x_reasonunit.base == dirty_text


def test_IdeaUnit_get_reasonheir_ReturnsCorrectObj():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    dirty_text = "dirty"
    reason_heir_x = reasonheir_shop(base=dirty_text)
    reason_heirs_x = {reason_heir_x.base: reason_heir_x}
    clean_idea.set_reasonheirs(reasonheirs=reason_heirs_x, bud_idea_dict={})

    # WHEN
    reason_heir_z = clean_idea.get_reasonheir(base=dirty_text)

    # THEN
    assert reason_heir_z is not None
    assert reason_heir_z.base == dirty_text


def test_IdeaUnit_get_reasonheir_ReturnsNone():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    dirty_text = "dirty"
    reason_heir_x = reasonheir_shop(dirty_text)
    reason_heirs_x = {reason_heir_x.base: reason_heir_x}
    clean_idea.set_reasonheirs(reasonheirs=reason_heirs_x, bud_idea_dict={})

    # WHEN
    test6_text = "test6"
    reason_heir_test6 = clean_idea.get_reasonheir(base=test6_text)

    # THEN
    assert reason_heir_test6 is None


def test_IdeaUnit_set_active_attrs_SetsNullactive_hxToNonEmpty():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    assert clean_idea._active_hx == {}

    # WHEN
    clean_idea.set_active_attrs(tree_traverse_count=3)
    # THEN
    assert clean_idea._active_hx == {3: True}


def test_IdeaUnit_set_active_attrs_IfFullactive_hxResetToTrue():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    clean_idea._active_hx = {0: True, 4: False}
    assert clean_idea._active_hx != {0: True}
    # WHEN
    clean_idea.set_active_attrs(tree_traverse_count=0)
    # THEN
    assert clean_idea._active_hx == {0: True}


def test_IdeaUnit_set_factunit_SetsAttr():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    dirty_text = "dirty"
    assert not clean_idea.factunits.get(dirty_text)

    # WHEN
    clean_idea.set_factunit(factunit_shop(base=dirty_text))

    # THEN
    assert clean_idea.factunits.get(dirty_text)


def test_IdeaUnit_factunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    dirty_text = "dirty"
    assert not clean_idea.factunit_exists(dirty_text)

    # WHEN
    clean_idea.set_factunit(factunit_shop(base=dirty_text))

    # THEN
    assert clean_idea.factunit_exists(dirty_text)


# def test_IdeaUnit_set_active_attrs_IfFullactive_hxResetToFalse():
#     # ESTABLISH
# clean_text = "clean"
# clean_idea = ideaunit_shop(clean_text)
#     clean_idea.set_reason_premise(
#         base="testing1,sec",
#         premise="testing1,sec,next",
#         open=None,
#         nigh=None,
#         divisor=None,
#     )
#     clean_idea._active_hx = {0: True, 4: False}
#     assert clean_idea._active_hx != {0: False}
#     # WHEN
#     clean_idea.set_active_attrs(tree_traverse_count=0)
#     # THEN
#     assert clean_idea._active_hx == {0: False}


def test_IdeaUnit_record_active_hx_CorrectlyRecordsHistorry():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    assert clean_idea._active_hx == {}

    # WHEN
    clean_idea.record_active_hx(0, prev_active=None, now_active=True)
    # THEN
    assert clean_idea._active_hx == {0: True}

    # WHEN
    clean_idea.record_active_hx(1, prev_active=True, now_active=True)
    # THEN
    assert clean_idea._active_hx == {0: True}

    # WHEN
    clean_idea.record_active_hx(2, prev_active=True, now_active=False)
    # THEN
    assert clean_idea._active_hx == {0: True, 2: False}

    # WHEN
    clean_idea.record_active_hx(3, prev_active=False, now_active=False)
    # THEN
    assert clean_idea._active_hx == {0: True, 2: False}

    # WHEN
    clean_idea.record_active_hx(4, prev_active=False, now_active=True)
    # THEN
    assert clean_idea._active_hx == {0: True, 2: False, 4: True}

    # WHEN
    clean_idea.record_active_hx(0, prev_active=False, now_active=False)
    # THEN
    assert clean_idea._active_hx == {0: False}


def test_IdeaUnit_set_teamunit_empty_if_none():
    # ESTABLISH
    run_text = "run"
    run_idea = ideaunit_shop(run_text)
    run_idea.teamunit = None
    assert run_idea.teamunit is None

    # WHEN
    run_idea.set_teamunit_empty_if_none()

    # THEN
    assert run_idea.teamunit is not None
    assert run_idea.teamunit == teamunit_shop()


def test_IdeaUnit_set_teamheir_CorrectlySetsAttr():
    # ESTABLISH
    swim_text = "swimmers"
    sport_text = "sports"
    sport_idea = ideaunit_shop(sport_text)
    sport_idea.teamunit.set_teamlink(group_id=swim_text)
    # assert sport_idea._teamheir is None

    # WHEN
    sport_idea.set_teamheir(parent_teamheir=None, bud_groupboxs=None)

    # THEN
    assert sport_idea._teamheir is not None
    swim_teamunit = teamunit_shop()
    swim_teamunit.set_teamlink(group_id=swim_text)
    swim_teamheir = teamheir_shop()
    swim_teamheir.set_teamlinks(
        teamunit=swim_teamunit, parent_teamheir=None, bud_groupboxs=None
    )
    assert sport_idea._teamheir == swim_teamheir
