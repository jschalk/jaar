from src._road.road import get_default_pecun_id_roadnode as root_label, create_road
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
    ball_str = "ball"
    ball_idea = ideaunit_shop(ball_str, _all_acct_cred=55, _all_acct_debt=33)
    assert ball_idea._all_acct_cred == 55
    assert ball_idea._all_acct_debt == 33

    # WHEN
    ball_idea.clear_all_acct_cred_debt()

    # THEN
    assert ball_idea._all_acct_cred is None
    assert ball_idea._all_acct_debt is None


def test_IdeaUnit_get_fund_share_ReturnsObj():
    # ESTABLISH
    texas_str = "texas"
    texas_idea = ideaunit_shop(texas_str, root_label())

    # WHEN / THEN
    assert texas_idea.get_fund_share() == 0

    # WHEN / THEN
    texas_idea._fund_onset = 3
    texas_idea._fund_cease = 14
    assert texas_idea.get_fund_share() == 11


def test_IdeaUnit_set_awardlink_SetsAttr():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_ideaunit = ideaunit_shop(sport_str)
    assert not sport_ideaunit.awardlinks.get(biker_str)

    # WHEN
    sport_ideaunit.set_awardlink(awardlink_shop(biker_str))

    # THEN
    assert sport_ideaunit.awardlinks.get(biker_str)


def test_IdeaUnit_awardlink_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_ideaunit = ideaunit_shop(sport_str)
    assert not sport_ideaunit.awardlink_exists(biker_str)

    # WHEN
    sport_ideaunit.set_awardlink(awardlink_shop(biker_str))

    # THEN
    assert sport_ideaunit.awardlink_exists(biker_str)


def test_IdeaUnit_get_awardlink_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_ideaunit = ideaunit_shop(sport_str)
    sport_ideaunit.set_awardlink(awardlink_shop(biker_str))

    # WHEN
    biker_awardlink = sport_ideaunit.get_awardlink(biker_str)

    # THEN
    assert biker_awardlink
    assert biker_awardlink.group_id == biker_str


def test_IdeaUnit_set_awardheirs_fund_give_fund_take_SetsAttrCorrectly_WithValues():
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_str = "bikers2"
    biker_awardheir = awardheir_shop(biker_str, biker_give_force, biker_take_force)
    swim_str = "swimmers"
    swim_group_id = swim_str
    swim_give_force = 29
    swim_take_force = 32
    swim_awardheir = awardheir_shop(swim_group_id, swim_give_force, swim_take_force)
    x_awardheirs = {
        swim_awardheir.group_id: swim_awardheir,
        biker_awardheir.group_id: biker_awardheir,
    }
    sport_str = "sport"
    sport_idea = ideaunit_shop(sport_str, _awardheirs=x_awardheirs)
    assert sport_idea._fund_coin == 1
    assert len(sport_idea._awardheirs) == 2
    swim_awardheir = sport_idea._awardheirs.get(swim_str)
    assert not swim_awardheir._fund_give
    assert not swim_awardheir._fund_take
    biker_awardheir = sport_idea._awardheirs.get(biker_str)
    assert not biker_awardheir._fund_give
    assert not biker_awardheir._fund_take

    # WHEN
    sport_idea._fund_onset = 91
    sport_idea._fund_cease = 820
    sport_idea.set_awardheirs_fund_give_fund_take()

    # THEN
    print(f"{len(sport_idea._awardheirs)=}")
    swim_awardheir = sport_idea._awardheirs.get(swim_str)
    assert swim_awardheir._fund_give == 516
    assert swim_awardheir._fund_take == 496
    biker_awardheir = sport_idea._awardheirs.get(biker_str)
    assert biker_awardheir._fund_give == 213
    assert biker_awardheir._fund_take == 233


def test_IdeaUnit_awardheir_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    biker_awardheir = awardheir_shop(biker_str)
    sport_str = "sport"
    sport_ideaunit = ideaunit_shop(sport_str)
    assert not sport_ideaunit.awardheir_exists()

    # WHEN
    sport_ideaunit._awardheirs[biker_str] = biker_awardheir

    # THEN
    assert sport_ideaunit.awardheir_exists()


def test_IdeaUnit_set_awardheirs_fund_give_fund_take_ReturnsCorrectObj_NoValues():
    # ESTABLISH /WHEN
    sport_str = "sport"
    sport_idea = ideaunit_shop(sport_str)

    # WHEN / THEN
    # does not crash with empty set
    sport_idea.set_awardheirs_fund_give_fund_take()


def test_IdeaUnit_set_reasonheirs_CorrectlyAcceptsChanges():
    # ESTABLISH
    ball_str = "ball"
    ball_road = create_road(ball_str)
    run_str = "run"
    run_road = create_road(ball_road, run_str)
    ball_idea = ideaunit_shop(ball_str)
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
    ball_str = "ball"
    ball_road = create_road(ball_str)
    run_str = "run"
    run_road = create_road(ball_road, run_str)
    run_premise = premiseunit_shop(need=run_road, open=0, nigh=7)
    run_premises = {run_premise.need: run_premise}
    run_reasonunit = reasonunit_shop(base=run_road, premises=run_premises)
    run_reasonunits = {run_reasonunit.base: run_reasonunit}
    ball_idea = ideaunit_shop(ball_str, reasonunits=run_reasonunits)
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
    week_str = "week"
    week_road = create_road(root_label(), week_str)
    week_open = 3
    week_nigh = 7
    week_addin = 10
    week_idea = ideaunit_shop(week_str, _parent_road=root_label(), addin=week_addin)
    week_factheir = factheir_shop(week_road, week_road, week_open, week_nigh)
    tue_str = "Tue"
    tue_road = create_road(week_road, tue_str)
    tue_addin = 100
    tue_idea = ideaunit_shop(tue_str, _parent_road=week_road, addin=tue_addin)
    ball_str = "ball"
    ball_road = create_road(root_label(), ball_str)
    ball_idea = ideaunit_shop(ball_str)
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
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_idea.reasonunits.get(dirty_str)

    # WHEN
    clean_idea.set_reasonunit(reasonunit_shop(base=dirty_str))

    # THEN
    assert clean_idea.reasonunits.get(dirty_str)
    x_reasonunit = clean_idea.get_reasonunit(base=dirty_str)
    assert x_reasonunit is not None
    assert x_reasonunit.base == dirty_str


def test_IdeaUnit_reasonunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_idea.reasonunit_exists(dirty_str)

    # WHEN
    clean_idea.set_reasonunit(reasonunit_shop(base=dirty_str))

    # THEN
    assert clean_idea.reasonunit_exists(dirty_str)


def test_IdeaUnit_get_reasonunit_ReturnsCorrectObj():
    # ESTABLISH
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
    dirty_str = "dirty"
    clean_idea.set_reasonunit(reasonunit_shop(base=dirty_str))

    # WHEN
    x_reasonunit = clean_idea.get_reasonunit(base=dirty_str)

    # THEN
    assert x_reasonunit is not None
    assert x_reasonunit.base == dirty_str


def test_IdeaUnit_get_reasonheir_ReturnsCorrectObj():
    # ESTABLISH
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
    dirty_str = "dirty"
    reason_heir_x = reasonheir_shop(base=dirty_str)
    reason_heirs_x = {reason_heir_x.base: reason_heir_x}
    clean_idea.set_reasonheirs(reasonheirs=reason_heirs_x, bud_idea_dict={})

    # WHEN
    reason_heir_z = clean_idea.get_reasonheir(base=dirty_str)

    # THEN
    assert reason_heir_z is not None
    assert reason_heir_z.base == dirty_str


def test_IdeaUnit_get_reasonheir_ReturnsNone():
    # ESTABLISH
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
    dirty_str = "dirty"
    reason_heir_x = reasonheir_shop(dirty_str)
    reason_heirs_x = {reason_heir_x.base: reason_heir_x}
    clean_idea.set_reasonheirs(reasonheirs=reason_heirs_x, bud_idea_dict={})

    # WHEN
    test6_str = "test6"
    reason_heir_test6 = clean_idea.get_reasonheir(base=test6_str)

    # THEN
    assert reason_heir_test6 is None


def test_IdeaUnit_set_active_attrs_SetsNullactive_hxToNonEmpty():
    # ESTABLISH
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
    assert clean_idea._active_hx == {}

    # WHEN
    clean_idea.set_active_attrs(tree_traverse_count=3)
    # THEN
    assert clean_idea._active_hx == {3: True}


def test_IdeaUnit_set_active_attrs_IfFullactive_hxResetToTrue():
    # ESTABLISH
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
    clean_idea._active_hx = {0: True, 4: False}
    assert clean_idea._active_hx != {0: True}
    # WHEN
    clean_idea.set_active_attrs(tree_traverse_count=0)
    # THEN
    assert clean_idea._active_hx == {0: True}


def test_IdeaUnit_set_factunit_SetsAttr():
    # ESTABLISH
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_idea.factunits.get(dirty_str)

    # WHEN
    clean_idea.set_factunit(factunit_shop(base=dirty_str))

    # THEN
    assert clean_idea.factunits.get(dirty_str)


def test_IdeaUnit_factunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_idea.factunit_exists(dirty_str)

    # WHEN
    clean_idea.set_factunit(factunit_shop(base=dirty_str))

    # THEN
    assert clean_idea.factunit_exists(dirty_str)


# def test_IdeaUnit_set_active_attrs_IfFullactive_hxResetToFalse():
#     # ESTABLISH
# clean_str = "clean"
# clean_idea = ideaunit_shop(clean_str)
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
    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str)
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
    run_str = "run"
    run_idea = ideaunit_shop(run_str)
    run_idea.teamunit = None
    assert run_idea.teamunit is None

    # WHEN
    run_idea.set_teamunit_empty_if_none()

    # THEN
    assert run_idea.teamunit is not None
    assert run_idea.teamunit == teamunit_shop()


def test_IdeaUnit_set_teamheir_CorrectlySetsAttr():
    # ESTABLISH
    swim_str = "swimmers"
    sport_str = "sports"
    sport_idea = ideaunit_shop(sport_str)
    sport_idea.teamunit.set_teamlink(group_id=swim_str)
    # assert sport_idea._teamheir is None

    # WHEN
    sport_idea.set_teamheir(parent_teamheir=None, bud_groupboxs=None)

    # THEN
    assert sport_idea._teamheir is not None
    swim_teamunit = teamunit_shop()
    swim_teamunit.set_teamlink(group_id=swim_str)
    swim_teamheir = teamheir_shop()
    swim_teamheir.set_teamlinks(
        teamunit=swim_teamunit, parent_teamheir=None, bud_groupboxs=None
    )
    assert sport_idea._teamheir == swim_teamheir
