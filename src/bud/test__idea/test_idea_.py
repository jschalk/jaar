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


def test_IdeaUnit_Exists():
    x_ideaunit = IdeaUnit()
    assert x_ideaunit
    assert x_ideaunit._kids is None
    assert x_ideaunit._mass is None
    assert x_ideaunit._label is None
    assert x_ideaunit._uid is None
    assert x_ideaunit._reasonunits is None
    assert x_ideaunit._reasonheirs is None  # calculated field
    assert x_ideaunit._doerunit is None
    assert x_ideaunit._doerheir is None  # calculated field
    assert x_ideaunit._factunits is None
    assert x_ideaunit._factheirs is None  # calculated field
    assert x_ideaunit._awardlinks is None
    assert x_ideaunit._awardlines is None  # calculated field'
    assert x_ideaunit._awardheirs is None  # calculated field'
    assert x_ideaunit._originunit is None
    assert x_ideaunit._road_delimiter is None
    assert x_ideaunit._begin is None
    assert x_ideaunit._close is None
    assert x_ideaunit._addin is None
    assert x_ideaunit._numor is None
    assert x_ideaunit._denom is None
    assert x_ideaunit._reest is None
    assert x_ideaunit._numeric_road is None
    assert x_ideaunit._range_source_road is None
    assert x_ideaunit._range_pushs is None
    assert x_ideaunit.pledge is None
    assert x_ideaunit._problem_bool is None
    assert x_ideaunit._healerhold is None
    # calculated_fields
    assert x_ideaunit._debut is None
    assert x_ideaunit._arret is None
    assert x_ideaunit._descendant_pledge_count is None
    assert x_ideaunit._is_expanded is None
    assert x_ideaunit._all_acct_cred is None
    assert x_ideaunit._all_acct_debt is None
    assert x_ideaunit._level is None
    assert x_ideaunit._active_hx is None
    assert x_ideaunit._fund_ratio is None
    assert x_ideaunit._fund_coin is None
    assert x_ideaunit._fund_onset is None
    assert x_ideaunit._fund_cease is None
    assert x_ideaunit._root is None
    assert x_ideaunit._bud_real_id is None
    assert x_ideaunit._healerhold_ratio is None


def test_ideaunit_shop_WithNoParametersReturnsObj():
    # ESTABLISH / WHEN
    x_ideaunit = ideaunit_shop()

    # THEN
    assert x_ideaunit
    assert x_ideaunit._kids == {}
    assert x_ideaunit._mass == 1
    assert x_ideaunit._label is None
    assert x_ideaunit._bud_real_id == root_label()
    assert x_ideaunit._uid is None
    assert x_ideaunit._begin is None
    assert x_ideaunit._close is None
    assert x_ideaunit._addin is None
    assert x_ideaunit._numor is None
    assert x_ideaunit._denom is None
    assert x_ideaunit._reest is None
    assert x_ideaunit._numeric_road is None
    assert x_ideaunit._range_source_road is None
    assert x_ideaunit._range_pushs == set()
    assert x_ideaunit.pledge is False
    assert x_ideaunit._problem_bool is False
    assert x_ideaunit._descendant_pledge_count is None
    assert x_ideaunit._awardlines == {}
    assert x_ideaunit._awardlinks == {}
    assert x_ideaunit._awardheirs == {}
    assert x_ideaunit._is_expanded == True
    assert x_ideaunit._factheirs == {}
    assert x_ideaunit._factunits == {}
    assert x_ideaunit._healerhold == healerhold_shop()
    assert x_ideaunit._debut is None
    assert x_ideaunit._arret is None
    assert x_ideaunit._level is None
    assert x_ideaunit._active_hx == {}
    assert x_ideaunit._fund_ratio is None
    assert x_ideaunit._fund_coin == default_fund_coin_if_none()
    assert x_ideaunit._fund_onset is None
    assert x_ideaunit._fund_cease is None
    assert x_ideaunit._reasonunits == {}
    assert x_ideaunit._reasonheirs == {}
    assert x_ideaunit._doerunit == doerunit_shop()
    assert x_ideaunit._doerheir is None
    assert x_ideaunit._originunit == originunit_shop()
    assert x_ideaunit._road_delimiter == default_road_delimiter_if_none()
    assert x_ideaunit._root is False
    assert x_ideaunit._all_acct_cred is None
    assert x_ideaunit._all_acct_debt is None
    assert x_ideaunit._healerhold_ratio == 0


def test_ideaunit_shop_Allows_massToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_ideaunit = ideaunit_shop("run", _mass=zero_int)
    # THEN
    assert x_ideaunit._mass == zero_int


def test_ideaunit_shop_Allows_doesNotAllow_massToBeNegative():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_ideaunit = ideaunit_shop("run", _mass=negative_int)
    # THEN
    zero_int = 0
    assert x_ideaunit._mass == zero_int


def test_ideaunit_shop_NonNoneParametersReturnsCorrectObj():
    # ESTABLISH
    x_healerhold = healerhold_shop({"Sue", "Yao"})
    x_problem_bool = True
    x_fund_coin = 88

    # WHEN
    x_ideaunit = ideaunit_shop(
        _healerhold=x_healerhold, _problem_bool=x_problem_bool, _fund_coin=x_fund_coin
    )

    # THEN
    assert x_ideaunit._healerhold == x_healerhold
    assert x_ideaunit._problem_bool == x_problem_bool
    assert x_ideaunit._fund_coin == x_fund_coin


def test_ideaunit_shop_ReturnsObjWith_awardlinks():
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_awardlink = awardlink_shop("bikers2", biker_give_force, biker_take_force)
    swim_group_id = "swimmers"
    swim_give_force = 29
    swim_take_force = 32
    swim_awardlink = awardlink_shop(swim_group_id, swim_give_force, swim_take_force)
    x_awardlinks = {
        swim_awardlink.group_id: swim_awardlink,
        biker_awardlink.group_id: biker_awardlink,
    }

    # WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text, _awardlinks=x_awardlinks)

    # THEN
    assert sport_idea._awardlinks == x_awardlinks


def test_IdeaUnit_get_obj_key_ReturnsCorrectObj():
    # ESTABLISH
    round_text = "round_things"
    round_road = create_road(root_label(), round_text)
    ball_text = "ball"

    # WHEN
    ball_idea = ideaunit_shop(_label=ball_text, _parent_road=round_road)

    # THEN
    assert ball_idea.get_obj_key() == ball_text


def test_IdeaUnit_get_road_ReturnsCorrectObj():
    # ESTABLISH
    round_text = "round_things"
    slash_text = "/"
    round_road = create_road(root_label(), round_text, delimiter=slash_text)
    ball_text = "ball"

    # WHEN
    ball_idea = ideaunit_shop(
        ball_text, _parent_road=round_road, _road_delimiter=slash_text
    )

    # THEN
    ball_road = create_road(round_road, ball_text, delimiter=slash_text)
    assert ball_idea.get_road() == ball_road


def test_IdeaUnit_set_parent_road_SetsAttr():
    # ESTABLISH
    round_text = "round_things"
    slash_text = "/"
    round_road = create_road(root_label(), round_text, delimiter=slash_text)
    ball_text = "ball"
    ball_idea = ideaunit_shop(
        ball_text, _parent_road=round_road, _road_delimiter=slash_text
    )
    assert ball_idea._parent_road == round_road

    # WHEN
    sports_road = create_road(root_label(), "sports", delimiter=slash_text)
    ball_idea.set_parent_road(parent_road=sports_road)

    # THEN
    assert ball_idea._parent_road == sports_road


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
    sport_idea = ideaunit_shop(_label=sport_text)

    # WHEN / THEN
    # does not crash with empty set
    sport_idea.set_awardheirs_fund_give_fund_take()


def test_IdeaUnit_set_reasonheirs_CorrectlyAcceptsChanges():
    # ESTABLISH
    ball_text = "ball"
    ball_road = create_road(ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    ball_idea = ideaunit_shop(_label=ball_text)
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
    ball_idea = ideaunit_shop(_label=ball_text, _reasonunits=run_reasonunits)
    assert ball_idea._reasonunits != {}

    # WHEN
    ball_idea.set_reasonheirs(reasonheirs=None, bud_idea_dict={})

    # THEN
    reasonheir = reasonheir_shop(run_road, premises=run_premises)
    reasonheirs = {reasonheir.base: reasonheir}
    assert ball_idea._reasonheirs == reasonheirs


def test_IdeaUnit_clear_descendant_pledge_count_ClearsCorrectly():
    # ESTABLISH
    ball_text = "ball"
    ball_idea = ideaunit_shop(_label=ball_text, _descendant_pledge_count=55)
    assert ball_idea._descendant_pledge_count == 55

    # WHEN
    ball_idea.clear_descendant_pledge_count()

    # THEN
    assert ball_idea._descendant_pledge_count is None


def test_IdeaUnit_add_to_descendant_pledge_count_CorrectlyAdds():
    # ESTABLISH
    ball_text = "ball"
    ball_idea = ideaunit_shop(_label=ball_text, _descendant_pledge_count=55)
    ball_idea.clear_descendant_pledge_count()
    assert ball_idea._descendant_pledge_count is None

    # WHEN
    ball_idea.add_to_descendant_pledge_count(44)

    # THEN
    assert ball_idea._descendant_pledge_count == 44

    # WHEN
    ball_idea.add_to_descendant_pledge_count(33)

    # THEN
    assert ball_idea._descendant_pledge_count == 77


def test_IdeaUnit_clear_all_acct_cred_debt_ClearsCorrectly():
    # ESTABLISH
    ball_text = "ball"
    ball_idea = ideaunit_shop(_label=ball_text, _all_acct_cred=55, _all_acct_debt=33)
    assert ball_idea._all_acct_cred == 55
    assert ball_idea._all_acct_debt == 33

    # WHEN
    ball_idea.clear_all_acct_cred_debt()

    # THEN
    assert ball_idea._all_acct_cred is None
    assert ball_idea._all_acct_debt is None


def test_IdeaUnit_get_reasonunit_ReturnsCorrectObj():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
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
    clean_idea = ideaunit_shop(_label=clean_text)
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
    clean_idea = ideaunit_shop(_label=clean_text)
    dirty_text = "dirty"
    reason_heir_x = reasonheir_shop(dirty_text)
    reason_heirs_x = {reason_heir_x.base: reason_heir_x}
    clean_idea.set_reasonheirs(reasonheirs=reason_heirs_x, bud_idea_dict={})

    # WHEN
    test6_text = "test6"
    reason_heir_test6 = clean_idea.get_reasonheir(base=test6_text)

    # THEN
    assert reason_heir_test6 is None


def test_IdeaUnit_set_active_SetsNullactive_hxToNonEmpty():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    assert clean_idea._active_hx == {}

    # WHEN
    clean_idea.set_active(tree_traverse_count=3)
    # THEN
    assert clean_idea._active_hx == {3: True}


def test_IdeaUnit_set_active_IfFullactive_hxResetToTrue():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    clean_idea._active_hx = {0: True, 4: False}
    assert clean_idea._active_hx != {0: True}
    # WHEN
    clean_idea.set_active(tree_traverse_count=0)
    # THEN
    assert clean_idea._active_hx == {0: True}


# def test_IdeaUnit_set_active_IfFullactive_hxResetToFalse():
#     # ESTABLISH
# clean_text = "clean"
# clean_idea = ideaunit_shop(_label=clean_text)
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
#     clean_idea.set_active(tree_traverse_count=0)
#     # THEN
#     assert clean_idea._active_hx == {0: False}


def test_IdeaUnit_record_active_hx_CorrectlyRecordsHistorry():
    # ESTABLISH
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    assert clean_idea._active_hx == {}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=0,
        prev_active=None,
        now_active=True,
    )
    # THEN
    assert clean_idea._active_hx == {0: True}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=1,
        prev_active=True,
        now_active=True,
    )
    # THEN
    assert clean_idea._active_hx == {0: True}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=2,
        prev_active=True,
        now_active=False,
    )
    # THEN
    assert clean_idea._active_hx == {0: True, 2: False}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=3,
        prev_active=False,
        now_active=False,
    )
    # THEN
    assert clean_idea._active_hx == {0: True, 2: False}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=4,
        prev_active=False,
        now_active=True,
    )
    # THEN
    assert clean_idea._active_hx == {0: True, 2: False, 4: True}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=0,
        prev_active=False,
        now_active=False,
    )
    # THEN
    assert clean_idea._active_hx == {0: False}


def test_IdeaUnit_set_doerunit_empty_if_none():
    # ESTABLISH
    run_text = "run"
    run_idea = ideaunit_shop(_label=run_text)
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
    sport_idea = ideaunit_shop(_label=sport_text)
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


def test_IdeaUnit_get_fund_share_ReturnsObj():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    # WHEN / THEN
    assert nation_idea.get_fund_share() == 0

    # WHEN / THEN
    nation_idea._fund_onset = 3
    nation_idea._fund_cease = 14
    assert nation_idea.get_fund_share() == 11


def test_IdeaUnit_is_arithmetic_ReturnsObj():
    # ESTABLISH
    swim_text = "swim"
    swim_idea = ideaunit_shop(swim_text)
    assert not swim_idea.is_arithmetic()
    # WHEN
    swim_idea._begin = 9
    # THEN
    assert not swim_idea.is_arithmetic()
    # WHEN
    swim_idea._close = 10
    # THEN
    assert swim_idea.is_arithmetic()
    # WHEN
    swim_idea._begin = None
    # THEN
    assert not swim_idea.is_arithmetic()


def test_IdeaUnit_set_range_push_SetsAttr():
    # ESTABLISH
    time_text = "time"
    time_idea = ideaunit_shop(time_text)
    week_text = "week"
    week_road = create_road(time_idea._bud_real_id, week_text)
    assert time_idea._range_pushs == set()

    # WHEN
    time_idea.set_range_push(week_road)

    # THEN
    assert time_idea._range_pushs == {week_road}

    # WHEN
    day_text = "day"
    day_road = create_road(time_idea._bud_real_id, day_text)
    time_idea.set_range_push(day_road)

    # THEN
    assert time_idea._range_pushs == {week_road, day_road}


def test_IdeaUnit_range_push_exists_ReturnsObj():
    # ESTABLISH
    time_text = "time"
    time_idea = ideaunit_shop(time_text)
    week_text = "week"
    week_road = create_road(time_idea._bud_real_id, week_text)
    day_text = "day"
    day_road = create_road(time_idea._bud_real_id, day_text)
    assert not time_idea.range_push_exists(week_road)
    assert not time_idea.range_push_exists(day_road)

    # WHEN
    time_idea.set_range_push(week_road)

    # THEN
    assert time_idea.range_push_exists(week_road)
    assert not time_idea.range_push_exists(day_road)

    # WHEN
    time_idea.set_range_push(day_road)

    # THEN
    assert time_idea.range_push_exists(week_road)
    assert time_idea.range_push_exists(day_road)


def test_IdeaUnit_del_range_push_SetsAttr():
    # ESTABLISH
    time_text = "time"
    time_idea = ideaunit_shop(time_text)
    week_text = "week"
    week_road = create_road(time_idea._bud_real_id, week_text)
    day_text = "day"
    day_road = create_road(time_idea._bud_real_id, day_text)
    time_idea.set_range_push(week_road)
    time_idea.set_range_push(day_road)
    assert time_idea.range_push_exists(week_road)
    assert time_idea.range_push_exists(day_road)

    # WHEN
    time_idea.del_range_push(week_road)

    # THEN
    assert not time_idea.range_push_exists(week_road)
    assert time_idea.range_push_exists(day_road)


def test_IdeaUnit_clear_debut_arret_SetsAttr():
    # ESTABLISH
    time_text = "time"
    time_idea = ideaunit_shop(time_text)
    time_idea._debut = 3
    time_idea._arret = 4
    assert time_idea._debut
    assert time_idea._arret

    # WHEN
    time_idea.clear_debut_arret()

    # THEN
    assert not time_idea._debut
    assert not time_idea._arret


def test_IdeaUnit_transform_debut_arret_SetsAttr_denom():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom)
    init_debut = 21
    init_arret = 42
    time_idea._debut = init_debut
    time_idea._arret = init_arret
    time_idea._denom = time_denom
    assert time_idea._debut
    assert time_idea._arret

    # WHEN
    time_idea._transform_debut_arret()

    # THEN
    assert time_idea._debut == init_debut / time_denom
    assert time_idea._arret == init_arret / time_denom
    assert time_idea._debut == 3
    assert time_idea._arret == 6


def test_IdeaUnit_transform_debut_arret_SetsAttr_reest():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _reest=True)
    init_debut = 21
    init_arret = 45
    time_idea._debut = init_debut
    time_idea._arret = init_arret
    time_idea._denom = time_denom
    assert time_idea._debut
    assert time_idea._arret

    # WHEN
    time_idea._transform_debut_arret()

    # THEN
    assert time_idea._debut == 0
    assert time_idea._arret == (init_arret - init_debut) % time_denom
    assert time_idea._debut == 0
    assert time_idea._arret == 3
