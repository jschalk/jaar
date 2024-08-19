from src._road.finance import default_fund_coin_if_none
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src.bud.healer import healerhold_shop
from src.bud.group import awardlink_shop, awardheir_shop
from src.bud.reason_idea import reasonunit_shop, reasonheir_shop, premiseunit_shop
from src.bud.reason_doer import doerunit_shop, doerheir_shop
from src.bud.origin import originunit_shop
from src.bud.idea import IdeaUnit, ideaunit_shop


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
    ball_idea = ideaunit_shop(ball_text, _reasonunits=run_reasonunits)
    assert ball_idea._reasonunits != {}

    # WHEN
    ball_idea.set_reasonheirs(reasonheirs={}, bud_idea_dict={})

    # THEN
    reasonheir = reasonheir_shop(run_road, premises=run_premises)
    reasonheirs = {reasonheir.base: reasonheir}
    assert ball_idea._reasonheirs == reasonheirs


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


def test_IdeaUnit_set_doerunit_empty_if_none():
    # ESTABLISH
    run_text = "run"
    run_idea = ideaunit_shop(run_text)
    run_idea._doerunit = None
    assert run_idea._doerunit is None

    # WHEN
    run_idea.set_doerunit_empty_if_none()

    # THEN
    assert run_idea._doerunit is not None
    assert run_idea._doerunit == doerunit_shop()


def test_IdeaUnit_set_doerheir_CorrectlySetsAttr():
    # ESTABLISH
    swim_text = "swimmers"
    sport_text = "sports"
    sport_idea = ideaunit_shop(sport_text)
    sport_idea._doerunit.set_grouphold(group_id=swim_text)
    # assert sport_idea._doerheir is None

    # WHEN
    sport_idea.set_doerheir(parent_doerheir=None, bud_groupboxs=None)

    # THEN
    assert sport_idea._doerheir is not None
    swim_doerunit = doerunit_shop()
    swim_doerunit.set_grouphold(group_id=swim_text)
    swim_doerheir = doerheir_shop()
    swim_doerheir.set_groupholds(
        doerunit=swim_doerunit, parent_doerheir=None, bud_groupboxs=None
    )
    assert sport_idea._doerheir == swim_doerheir
