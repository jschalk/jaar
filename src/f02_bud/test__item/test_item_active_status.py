from src.f01_road.road import get_default_deal_id_ideaunit as root_label, create_road
from src.f02_bud.group import awardheir_shop, awardlink_shop
from src.f02_bud.reason_item import (
    reasonunit_shop,
    reasonheir_shop,
    premiseunit_shop,
    factheir_shop,
    factunit_shop,
)
from src.f02_bud.reason_team import teamunit_shop, teamheir_shop
from src.f02_bud.item import itemunit_shop


def test_ItemUnit_clear_all_acct_cred_debt_ClearsCorrectly():
    # ESTABLISH
    ball_str = "ball"
    ball_item = itemunit_shop(ball_str, _all_acct_cred=55, _all_acct_debt=33)
    assert ball_item._all_acct_cred == 55
    assert ball_item._all_acct_debt == 33

    # WHEN
    ball_item.clear_all_acct_cred_debt()

    # THEN
    assert ball_item._all_acct_cred is None
    assert ball_item._all_acct_debt is None


def test_ItemUnit_get_fund_share_ReturnsObj():
    # ESTABLISH
    texas_str = "texas"
    texas_item = itemunit_shop(texas_str, root_label())

    # WHEN / THEN
    assert texas_item.get_fund_share() == 0

    # WHEN / THEN
    texas_item._fund_onset = 3
    texas_item._fund_cease = 14
    assert texas_item.get_fund_share() == 11


def test_ItemUnit_set_awardlink_SetsAttr():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_itemunit = itemunit_shop(sport_str)
    assert not sport_itemunit.awardlinks.get(biker_str)

    # WHEN
    sport_itemunit.set_awardlink(awardlink_shop(biker_str))

    # THEN
    assert sport_itemunit.awardlinks.get(biker_str)


def test_ItemUnit_awardlink_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_itemunit = itemunit_shop(sport_str)
    assert not sport_itemunit.awardlink_exists(biker_str)

    # WHEN
    sport_itemunit.set_awardlink(awardlink_shop(biker_str))

    # THEN
    assert sport_itemunit.awardlink_exists(biker_str)


def test_ItemUnit_get_awardlink_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_itemunit = itemunit_shop(sport_str)
    sport_itemunit.set_awardlink(awardlink_shop(biker_str))

    # WHEN
    biker_awardlink = sport_itemunit.get_awardlink(biker_str)

    # THEN
    assert biker_awardlink
    assert biker_awardlink.awardee_id == biker_str


def test_ItemUnit_set_awardheirs_fund_give_fund_take_SetsAttrCorrectly_WithValues():
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
        swim_awardheir.awardee_id: swim_awardheir,
        biker_awardheir.awardee_id: biker_awardheir,
    }
    sport_str = "sport"
    sport_item = itemunit_shop(sport_str, _awardheirs=x_awardheirs)
    assert sport_item._fund_coin == 1
    assert len(sport_item._awardheirs) == 2
    swim_awardheir = sport_item._awardheirs.get(swim_str)
    assert not swim_awardheir._fund_give
    assert not swim_awardheir._fund_take
    biker_awardheir = sport_item._awardheirs.get(biker_str)
    assert not biker_awardheir._fund_give
    assert not biker_awardheir._fund_take

    # WHEN
    sport_item._fund_onset = 91
    sport_item._fund_cease = 820
    sport_item.set_awardheirs_fund_give_fund_take()

    # THEN
    print(f"{len(sport_item._awardheirs)=}")
    swim_awardheir = sport_item._awardheirs.get(swim_str)
    assert swim_awardheir._fund_give == 516
    assert swim_awardheir._fund_take == 496
    biker_awardheir = sport_item._awardheirs.get(biker_str)
    assert biker_awardheir._fund_give == 213
    assert biker_awardheir._fund_take == 233


def test_ItemUnit_awardheir_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    biker_awardheir = awardheir_shop(biker_str)
    sport_str = "sport"
    sport_itemunit = itemunit_shop(sport_str)
    assert not sport_itemunit.awardheir_exists()

    # WHEN
    sport_itemunit._awardheirs[biker_str] = biker_awardheir

    # THEN
    assert sport_itemunit.awardheir_exists()


def test_ItemUnit_set_awardheirs_fund_give_fund_take_ReturnsCorrectObj_NoValues():
    # ESTABLISH /WHEN
    sport_str = "sport"
    sport_item = itemunit_shop(sport_str)

    # WHEN / THEN
    # does not crash with empty set
    sport_item.set_awardheirs_fund_give_fund_take()


def test_ItemUnit_set_reasonheirs_CorrectlyAcceptsNewValues():
    # ESTABLISH
    ball_str = "ball"
    ball_road = create_road(ball_str)
    run_str = "run"
    run_road = create_road(ball_road, run_str)
    ball_item = itemunit_shop(ball_str)
    run_premise = premiseunit_shop(need=run_road, open=0, nigh=7)
    run_premises = {run_premise.need: run_premise}
    reasonheir = reasonheir_shop(run_road, premises=run_premises)
    reasonheirs = {reasonheir.base: reasonheir}
    assert ball_item._reasonheirs == {}

    # WHEN
    ball_item.set_reasonheirs(reasonheirs=reasonheirs, bud_item_dict={})

    # THEN
    assert ball_item._reasonheirs == reasonheirs
    assert id(ball_item._reasonheirs) != id(reasonheirs)


def test_ItemUnit_set_reasonheirs_CorrectlyRefusesNewValues():
    # ESTABLISH
    ball_str = "ball"
    ball_road = create_road(ball_str)
    run_str = "run"
    run_road = create_road(ball_road, run_str)
    run_premise = premiseunit_shop(need=run_road, open=0, nigh=7)
    run_premises = {run_premise.need: run_premise}
    run_reasonunit = reasonunit_shop(base=run_road, premises=run_premises)
    run_reasonunits = {run_reasonunit.base: run_reasonunit}
    ball_item = itemunit_shop(ball_str, reasonunits=run_reasonunits)
    assert ball_item.reasonunits != {}

    # WHEN
    ball_item.set_reasonheirs(reasonheirs={}, bud_item_dict={})

    # THEN
    reasonheir = reasonheir_shop(run_road, premises=run_premises)
    reasonheirs = {reasonheir.base: reasonheir}
    assert ball_item._reasonheirs == reasonheirs


def test_ItemUnit_set_range_factheirs_SetsAttrNoParameters():
    # ESTABLISH
    ball_item = itemunit_shop("ball")
    assert ball_item._factheirs == {}

    # WHEN
    ball_item.set_range_factheirs(bud_item_dict={}, range_inheritors={})

    # THEN
    assert ball_item._factheirs == {}


def test_ItemUnit_set_range_factheirs_SetsAttrNewFactHeir():
    # ESTABLISH
    week_str = "week"
    week_road = create_road(root_label(), week_str)
    week_open = 3
    week_nigh = 7
    week_addin = 10
    week_item = itemunit_shop(week_str, _parent_road=root_label(), addin=week_addin)
    week_factheir = factheir_shop(week_road, week_road, week_open, week_nigh)
    tue_str = "Tue"
    tue_road = create_road(week_road, tue_str)
    tue_addin = 100
    tue_item = itemunit_shop(tue_str, _parent_road=week_road, addin=tue_addin)
    ball_str = "ball"
    ball_road = create_road(root_label(), ball_str)
    ball_item = itemunit_shop(ball_str)
    ball_item._set_factheir(week_factheir)
    tue_reasonheirs = {tue_road: reasonheir_shop(tue_road, None, False)}
    x_bud_item_dict = {week_item.get_road(): week_item, tue_item.get_road(): tue_item}
    ball_item.set_reasonheirs(x_bud_item_dict, tue_reasonheirs)

    x_range_inheritors = {tue_road: week_road}
    assert len(ball_item._reasonheirs) == 1
    assert ball_item._factheirs == {week_road: week_factheir}
    assert ball_item._factheirs.get(week_road)
    assert len(ball_item._factheirs) == 1
    assert ball_item._factheirs.get(tue_road) is None

    # WHEN
    ball_item.set_range_factheirs(x_bud_item_dict, x_range_inheritors)

    # THEN
    tue_open = 113
    tue_nigh = 117
    tue_factheir = factheir_shop(tue_road, tue_road, tue_open, tue_nigh)
    assert len(ball_item._factheirs) == 2
    assert ball_item._factheirs == {tue_road: tue_factheir, week_road: week_factheir}


def test_ItemUnit_set_reasonunit_SetsAttr():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_item.reasonunits.get(dirty_str)

    # WHEN
    clean_item.set_reasonunit(reasonunit_shop(base=dirty_str))

    # THEN
    assert clean_item.reasonunits.get(dirty_str)
    x_reasonunit = clean_item.get_reasonunit(base=dirty_str)
    assert x_reasonunit is not None
    assert x_reasonunit.base == dirty_str


def test_ItemUnit_reasonunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_item.reasonunit_exists(dirty_str)

    # WHEN
    clean_item.set_reasonunit(reasonunit_shop(base=dirty_str))

    # THEN
    assert clean_item.reasonunit_exists(dirty_str)


def test_ItemUnit_get_reasonunit_ReturnsCorrectObj():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    dirty_str = "dirty"
    clean_item.set_reasonunit(reasonunit_shop(base=dirty_str))

    # WHEN
    x_reasonunit = clean_item.get_reasonunit(base=dirty_str)

    # THEN
    assert x_reasonunit is not None
    assert x_reasonunit.base == dirty_str


def test_ItemUnit_get_reasonheir_ReturnsCorrectObj():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    dirty_str = "dirty"
    reason_heir_x = reasonheir_shop(base=dirty_str)
    reason_heirs_x = {reason_heir_x.base: reason_heir_x}
    clean_item.set_reasonheirs(reasonheirs=reason_heirs_x, bud_item_dict={})

    # WHEN
    reason_heir_z = clean_item.get_reasonheir(base=dirty_str)

    # THEN
    assert reason_heir_z is not None
    assert reason_heir_z.base == dirty_str


def test_ItemUnit_get_reasonheir_ReturnsNone():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    dirty_str = "dirty"
    reason_heir_x = reasonheir_shop(dirty_str)
    reason_heirs_x = {reason_heir_x.base: reason_heir_x}
    clean_item.set_reasonheirs(reasonheirs=reason_heirs_x, bud_item_dict={})

    # WHEN
    test6_str = "test6"
    reason_heir_test6 = clean_item.get_reasonheir(base=test6_str)

    # THEN
    assert reason_heir_test6 is None


def test_ItemUnit_set_active_attrs_SetsNullactive_hxToNonEmpty():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    assert clean_item._active_hx == {}

    # WHEN
    clean_item.set_active_attrs(tree_traverse_count=3)
    # THEN
    assert clean_item._active_hx == {3: True}


def test_ItemUnit_set_active_attrs_IfFullactive_hxResetToTrue():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    clean_item._active_hx = {0: True, 4: False}
    assert clean_item._active_hx != {0: True}
    # WHEN
    clean_item.set_active_attrs(tree_traverse_count=0)
    # THEN
    assert clean_item._active_hx == {0: True}


def test_ItemUnit_set_factunit_SetsAttr():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_item.factunits.get(dirty_str)

    # WHEN
    clean_item.set_factunit(factunit_shop(base=dirty_str))

    # THEN
    assert clean_item.factunits.get(dirty_str)


def test_ItemUnit_factunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    dirty_str = "dirty"
    assert not clean_item.factunit_exists(dirty_str)

    # WHEN
    clean_item.set_factunit(factunit_shop(base=dirty_str))

    # THEN
    assert clean_item.factunit_exists(dirty_str)


# def test_ItemUnit_set_active_attrs_IfFullactive_hxResetToFalse():
#     # ESTABLISH
# clean_str = "clean"
# clean_item = itemunit_shop(clean_str)
#     clean_item.set_reason_premise(
#         base="testing1,sec",
#         premise="testing1,sec,next",
#         open=None,
#         nigh=None,
#         divisor=None,
#     )
#     clean_item._active_hx = {0: True, 4: False}
#     assert clean_item._active_hx != {0: False}
#     # WHEN
#     clean_item.set_active_attrs(tree_traverse_count=0)
#     # THEN
#     assert clean_item._active_hx == {0: False}


def test_ItemUnit_record_active_hx_CorrectlyRecordsHistorry():
    # ESTABLISH
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    assert clean_item._active_hx == {}

    # WHEN
    clean_item.record_active_hx(0, prev_active=None, now_active=True)
    # THEN
    assert clean_item._active_hx == {0: True}

    # WHEN
    clean_item.record_active_hx(1, prev_active=True, now_active=True)
    # THEN
    assert clean_item._active_hx == {0: True}

    # WHEN
    clean_item.record_active_hx(2, prev_active=True, now_active=False)
    # THEN
    assert clean_item._active_hx == {0: True, 2: False}

    # WHEN
    clean_item.record_active_hx(3, prev_active=False, now_active=False)
    # THEN
    assert clean_item._active_hx == {0: True, 2: False}

    # WHEN
    clean_item.record_active_hx(4, prev_active=False, now_active=True)
    # THEN
    assert clean_item._active_hx == {0: True, 2: False, 4: True}

    # WHEN
    clean_item.record_active_hx(0, prev_active=False, now_active=False)
    # THEN
    assert clean_item._active_hx == {0: False}


def test_ItemUnit_set_teamunit_empty_if_None():
    # ESTABLISH
    run_str = "run"
    run_item = itemunit_shop(run_str)
    run_item.teamunit = None
    assert run_item.teamunit is None

    # WHEN
    run_item.set_teamunit_empty_if_None()

    # THEN
    assert run_item.teamunit is not None
    assert run_item.teamunit == teamunit_shop()


def test_ItemUnit_set_teamheir_CorrectlySetsAttr():
    # ESTABLISH
    swim_str = "swimmers"
    sport_str = "sports"
    sport_item = itemunit_shop(sport_str)
    sport_item.teamunit.set_teamlink(team_id=swim_str)
    # assert sport_item._teamheir is None

    # WHEN
    sport_item.set_teamheir(parent_teamheir=None, bud_groupunits=None)

    # THEN
    assert sport_item._teamheir is not None
    swim_teamunit = teamunit_shop()
    swim_teamunit.set_teamlink(team_id=swim_str)
    swim_teamheir = teamheir_shop()
    swim_teamheir.set_teamlinks(
        teamunit=swim_teamunit, parent_teamheir=None, bud_groupunits=None
    )
    assert sport_item._teamheir == swim_teamheir
