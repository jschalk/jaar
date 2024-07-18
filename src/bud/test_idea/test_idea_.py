from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src.bud.healer import healerhold_shop
from src.bud.lobby import awardlink_shop, awardheir_shop
from src.bud.reason_idea import (
    reasonunit_shop,
    reasonheir_shop,
    factunit_shop,
    premiseunit_shop,
)
from src.bud.reason_doer import doerunit_shop, doerheir_shop
from src.bud.origin import originunit_shop
from src.bud.idea import IdeaUnit, ideaunit_shop, get_obj_from_idea_dict
from pytest import raises as pytest_raises


def test_IdeaUnit_exists():
    x_ideaunit = IdeaUnit()
    assert x_ideaunit
    assert x_ideaunit._kids is None
    assert x_ideaunit._weight is None
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
    assert x_ideaunit.pledge is None
    assert x_ideaunit._problem_bool is None
    assert x_ideaunit._healerhold is None
    # calculated_fields
    assert x_ideaunit._descendant_pledge_count is None
    assert x_ideaunit._is_expanded is None
    assert x_ideaunit._all_char_cred is None
    assert x_ideaunit._all_char_debt is None
    assert x_ideaunit._level is None
    assert x_ideaunit._active_hx is None
    assert x_ideaunit._fund_ratio is None
    assert x_ideaunit._fund_coin is None
    assert x_ideaunit._fund_onset is None
    assert x_ideaunit._fund_cease is None
    assert x_ideaunit._root is None
    assert x_ideaunit._bud_real_id is None
    assert x_ideaunit._healerhold_ratio is None


def test_ideaunit_shop_NoParametersReturnsCorrectObj():
    # ESTABLISH / WHEN
    x_ideaunit = ideaunit_shop()

    # THEN
    assert x_ideaunit
    assert x_ideaunit._kids == {}
    assert x_ideaunit._weight == 1
    assert x_ideaunit._label is None
    assert x_ideaunit._uid is None
    assert x_ideaunit._all_char_cred is None
    assert x_ideaunit._all_char_debt is None
    assert x_ideaunit._begin is None
    assert x_ideaunit._close is None
    assert x_ideaunit._addin is None
    assert x_ideaunit._numor is None
    assert x_ideaunit._denom is None
    assert x_ideaunit._reest is None
    assert x_ideaunit._numeric_road is None
    assert x_ideaunit._range_source_road is None
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
    assert x_ideaunit._level is None
    assert x_ideaunit._active_hx == {}
    assert x_ideaunit._fund_ratio is None
    assert x_ideaunit._fund_coin is None
    assert x_ideaunit._fund_onset is None
    assert x_ideaunit._fund_cease is None
    assert x_ideaunit._reasonunits == {}
    assert x_ideaunit._reasonheirs == {}
    assert x_ideaunit._doerunit == doerunit_shop()
    assert x_ideaunit._doerheir is None
    assert x_ideaunit._originunit == originunit_shop()
    assert x_ideaunit._road_delimiter == default_road_delimiter_if_none()
    assert x_ideaunit._root is False
    assert x_ideaunit._bud_real_id == root_label()
    assert x_ideaunit._healerhold_ratio == 0


def test_ideaunit_shop_Allows_weightToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_ideaunit = ideaunit_shop("run", _weight=zero_int)
    # THEN
    assert x_ideaunit._weight == zero_int


def test_ideaunit_shop_Allows_doesNotAllow_weightToBeNegative():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_ideaunit = ideaunit_shop("run", _weight=negative_int)
    # THEN
    zero_int = 0
    assert x_ideaunit._weight == zero_int


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


def test_IdeaUnit_set_parent_road_ReturnsCorrectObj():
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


def test_IdeaUnit_awardlinks_exist():
    # ESTABLISH
    biker_give_weight = 12
    biker_take_weight = 15
    biker_awardlink = awardlink_shop(
        lobby_id="bikers2",
        give_weight=biker_give_weight,
        take_weight=biker_take_weight,
    )

    swimmer_lobby_id = "swimmers"
    swimmer_give_weight = 29
    swimmer_take_weight = 32
    swimmer_awardlink = awardlink_shop(
        lobby_id=swimmer_lobby_id,
        give_weight=swimmer_give_weight,
        take_weight=swimmer_take_weight,
    )

    x_lobbyships = {
        swimmer_awardlink.lobby_id: swimmer_awardlink,
        biker_awardlink.lobby_id: biker_awardlink,
    }

    # WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text, _awardlinks=x_lobbyships)

    # THEN
    assert sport_idea._awardlinks == x_lobbyships


def test_IdeaUnit_get_inherited_awardheirs_weight_sum_SetsAttrCorrectly_WithValues():
    # ESTABLISH
    biker_give_weight = 12
    biker_take_weight = 15
    biker_text = "bikers2"
    biker_awardlink = awardheir_shop(
        lobby_id=biker_text,
        give_weight=biker_give_weight,
        take_weight=biker_take_weight,
    )

    swimmer_text = "swimmers"
    swimmer_lobby_id = swimmer_text
    swimmer_give_weight = 29
    swimmer_take_weight = 32
    swimmer_awardlink = awardheir_shop(
        lobby_id=swimmer_lobby_id,
        give_weight=swimmer_give_weight,
        take_weight=swimmer_take_weight,
    )

    x_lobbyships = {
        swimmer_awardlink.lobby_id: swimmer_awardlink,
        biker_awardlink.lobby_id: biker_awardlink,
    }

    # WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text, _awardheirs=x_lobbyships)

    # THEN
    assert sport_idea.get_awardheirs_give_weight_sum() is not None
    assert sport_idea.get_awardheirs_give_weight_sum() == 41
    assert sport_idea.get_awardheirs_take_weight_sum() is not None
    assert sport_idea.get_awardheirs_take_weight_sum() == 47

    assert len(sport_idea._awardheirs) == 2

    swimmer_awardheir = sport_idea._awardheirs.get(swimmer_text)
    assert swimmer_awardheir._fund_give is None
    assert swimmer_awardheir._fund_take is None
    biker_awardheir = sport_idea._awardheirs.get(biker_text)
    assert biker_awardheir._fund_give is None
    assert biker_awardheir._fund_take is None

    # WHEN
    sport_idea._fund_ratio = 0.25
    sport_idea.set_awardheirs_fund_give_fund_take()

    # THEN
    print(f"{len(sport_idea._awardheirs)=}")
    swimmer_awardheir = sport_idea._awardheirs.get(swimmer_text)
    assert swimmer_awardheir._fund_give is not None
    assert swimmer_awardheir._fund_take is not None
    biker_awardheir = sport_idea._awardheirs.get(biker_text)
    assert biker_awardheir._fund_give is not None
    assert biker_awardheir._fund_take is not None


def test_IdeaUnit_get_awardlinks_weight_sum_ReturnsCorrectObj_NoValues():
    # ESTABLISH /WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text)
    assert sport_idea.get_awardheirs_give_weight_sum() is not None
    assert sport_idea.get_awardheirs_take_weight_sum() is not None

    # WHEN / THEN
    # does not crash with empty set
    sport_idea.set_awardheirs_fund_give_fund_take()


def test_IdeaUnit_set_reasonheirsCorrectlySourcesFromOutside():
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


def test_IdeaUnit_set_reasonheirsCorrectlySourcesFromSelf():
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


def test_IdeaUnit_clear_all_char_cred_debt_ClearsCorrectly():
    # ESTABLISH
    ball_text = "ball"
    ball_idea = ideaunit_shop(_label=ball_text, _all_char_cred=55, _all_char_debt=33)
    assert ball_idea._all_char_cred == 55
    assert ball_idea._all_char_debt == 33

    # WHEN
    ball_idea.clear_all_char_cred_debt()

    # THEN
    assert ball_idea._all_char_cred is None
    assert ball_idea._all_char_debt is None


def test_get_kids_in_range_GetsCorrectIdeas():
    # ESTABLISH
    mon366_text = "366months"
    mon366_idea = ideaunit_shop(_label=mon366_text, _begin=0, _close=366)
    jan_text = "Jan"
    feb29_text = "Feb29"
    mar_text = "Mar"
    mon366_idea.add_kid(idea_kid=ideaunit_shop(_label=jan_text, _begin=0, _close=31))
    mon366_idea.add_kid(idea_kid=ideaunit_shop(_label=feb29_text, _begin=31, _close=60))
    mon366_idea.add_kid(idea_kid=ideaunit_shop(_label=mar_text, _begin=31, _close=91))

    # WHEN / THEN
    assert len(mon366_idea.get_kids_in_range(begin=100, close=120)) == 0
    assert len(mon366_idea.get_kids_in_range(begin=0, close=31)) == 1
    assert len(mon366_idea.get_kids_in_range(begin=5, close=5)) == 1
    assert len(mon366_idea.get_kids_in_range(begin=0, close=61)) == 3
    assert mon366_idea.get_kids_in_range(begin=31, close=31)[0]._label == feb29_text


def test_get_obj_from_idea_dict_ReturnsCorrectObj():
    # ESTABLISH
    field_text = "_is_expanded"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_text: True}, field_text)
    assert get_obj_from_idea_dict({}, field_text)
    assert get_obj_from_idea_dict({field_text: False}, field_text) is False

    # ESTABLISH
    field_text = "pledge"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_text: True}, field_text)
    assert get_obj_from_idea_dict({}, field_text) is False
    assert get_obj_from_idea_dict({field_text: False}, field_text) is False

    # ESTABLISH
    field_text = "_problem_bool"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_text: True}, field_text)
    assert get_obj_from_idea_dict({}, field_text) is False
    assert get_obj_from_idea_dict({field_text: False}, field_text) is False

    # ESTABLISH
    field_text = "_kids"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_text: {}}, field_text) == {}
    assert get_obj_from_idea_dict({}, field_text) == {}


def test_get_obj_from_idea_dict_ReturnsCorrect_HealerHold():
    # ESTABLISH
    # WHEN / THEN
    healerhold_key = "_healerhold"
    assert get_obj_from_idea_dict({}, healerhold_key) == healerhold_shop()

    # WHEN
    sue_text = "Sue"
    zia_text = "Zia"
    healerhold_dict = {"healerhold_lobby_ids": [sue_text, zia_text]}
    ideaunit_dict = {healerhold_key: healerhold_dict}

    # THEN
    static_healerhold = healerhold_shop()
    static_healerhold.set_lobby_id(x_lobby_id=sue_text)
    static_healerhold.set_lobby_id(x_lobby_id=zia_text)
    assert get_obj_from_idea_dict(ideaunit_dict, healerhold_key) is not None
    assert get_obj_from_idea_dict(ideaunit_dict, healerhold_key) == static_healerhold


def test_IdeaUnit_get_dict_ReturnsCorrectCompleteDict():
    # ESTABLISH
    week_text = "weekdays"
    week_road = create_road(root_label(), week_text)
    wed_text = "Wednesday"
    wed_road = create_road(week_road, wed_text)
    states_text = "nation-state"
    states_road = create_road(root_label(), states_text)
    usa_text = "USA"
    usa_road = create_road(states_road, usa_text)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = True
    usa_premise = premiseunit_shop(need=usa_road)
    usa_premise._status = False

    x1_reasonunits = {
        week_road: reasonunit_shop(
            base=week_road, premises={wed_premise.need: wed_premise}
        ),
        states_road: reasonunit_shop(
            base=states_road, premises={usa_premise.need: usa_premise}
        ),
    }
    x1_reasonheirs = {
        week_road: reasonheir_shop(
            base=week_road, premises={wed_premise.need: wed_premise}, _status=True
        ),
        states_road: reasonheir_shop(
            base=states_road, premises={usa_premise.need: usa_premise}, _status=False
        ),
    }
    biker_lobby_id = "bikers"
    biker_give_weight = 3.0
    biker_take_weight = 7.0
    biker_awardlink = awardlink_shop(
        biker_lobby_id, biker_give_weight, biker_take_weight
    )
    flyer_lobby_id = "flyers"
    flyer_give_weight = 6.0
    flyer_take_weight = 9.0
    flyer_awardlink = awardlink_shop(
        lobby_id=flyer_lobby_id,
        give_weight=flyer_give_weight,
        take_weight=flyer_take_weight,
    )
    biker_and_flyer_awardlinks = {
        biker_awardlink.lobby_id: biker_awardlink,
        flyer_awardlink.lobby_id: flyer_awardlink,
    }
    biker_get_dict = {
        "lobby_id": biker_awardlink.lobby_id,
        "give_weight": biker_awardlink.give_weight,
        "take_weight": biker_awardlink.take_weight,
    }
    flyer_get_dict = {
        "lobby_id": flyer_awardlink.lobby_id,
        "give_weight": flyer_awardlink.give_weight,
        "take_weight": flyer_awardlink.take_weight,
    }
    x1_awardlinks = {biker_lobby_id: biker_get_dict, flyer_lobby_id: flyer_get_dict}
    sue_text = "Sue"
    yao_text = "Yao"
    sue_doerunit = doerunit_shop({sue_text: -1, yao_text: -1})
    yao_healerhold = healerhold_shop({yao_text})
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
    x_problem_bool = True
    casa_idea = ideaunit_shop(
        _parent_road=casa_road,
        _kids=None,
        _awardlinks=biker_and_flyer_awardlinks,
        _weight=30,
        _label=casa_text,
        _level=1,
        _reasonunits=x1_reasonunits,
        _reasonheirs=x1_reasonheirs,
        _doerunit=sue_doerunit,
        _healerhold=yao_healerhold,
        _active=True,
        _range_source_road="test123",
        pledge=True,
        _problem_bool=x_problem_bool,
    )
    factunit_x = factunit_shop(base=week_road, pick=week_road, open=5, nigh=59)
    casa_idea.set_factunit(factunit=factunit_x)
    casa_idea._originunit.set_originhold(char_id="Ray", weight=None)
    casa_idea._originunit.set_originhold(char_id="Lei", weight=4)
    x_begin = 11
    x_close = 12
    x_addin = 13
    x_denom = 14
    x_numor = 15
    x_reest = 16
    casa_idea._begin = x_begin
    casa_idea._close = x_close
    casa_idea._addin = x_addin
    casa_idea._denom = x_denom
    casa_idea._numor = x_numor
    casa_idea._reest = x_reest
    casa_idea._uid = 17
    casa_idea.add_kid(ideaunit_shop("paper"))

    # WHEN
    casa_dict = casa_idea.get_dict()

    # THEN
    assert casa_dict is not None
    assert len(casa_dict["_kids"]) == 1
    assert casa_dict["_kids"] == casa_idea.get_kids_dict()
    assert casa_dict["_reasonunits"] == casa_idea.get_reasonunits_dict()
    assert casa_dict["_awardlinks"] == casa_idea.get_awardlinks_dict()
    assert casa_dict["_awardlinks"] == x1_awardlinks
    assert casa_dict["_doerunit"] == sue_doerunit.get_dict()
    assert casa_dict["_healerhold"] == yao_healerhold.get_dict()
    assert casa_dict["_originunit"] == casa_idea.get_originunit_dict()
    assert casa_dict["_weight"] == casa_idea._weight
    assert casa_dict["_label"] == casa_idea._label
    assert casa_dict["_uid"] == casa_idea._uid
    assert casa_dict["_begin"] == casa_idea._begin
    assert casa_dict["_close"] == casa_idea._close
    assert casa_dict["_numor"] == casa_idea._numor
    assert casa_dict["_denom"] == casa_idea._denom
    assert casa_dict["_reest"] == casa_idea._reest
    assert casa_dict["_range_source_road"] == casa_idea._range_source_road
    assert casa_dict["pledge"] == casa_idea.pledge
    assert casa_dict["_problem_bool"] == casa_idea._problem_bool
    assert casa_dict["_problem_bool"] == x_problem_bool
    assert casa_idea._is_expanded
    assert casa_dict.get("_is_expanded") is None
    assert len(casa_dict["_factunits"]) == len(casa_idea.get_factunits_dict())


def test_IdeaUnit_get_dict_ReturnsCorrectDictWithoutEmptyAttributes():
    # ESTABLISH
    casa_idea = ideaunit_shop()

    # WHEN
    casa_dict = casa_idea.get_dict()

    # THEN
    assert casa_dict is not None
    assert casa_dict == {"_weight": 1}


def test_IdeaUnit_get_dict_ReturnsDictWith_attrs_CorrectlySetTrue():
    # ESTABLISH
    casa_idea = ideaunit_shop()
    casa_idea._is_expanded = False
    casa_idea.pledge = True
    ignore_text = "ignore"

    a_text = "a"
    a_road = create_road(root_label(), a_text)
    casa_idea.set_factunit(factunit_shop(a_road, a_road))

    yao_text = "Yao"
    casa_idea.set_awardlink(awardlink_shop(yao_text))

    x_doerunit = casa_idea._doerunit
    x_doerunit.set_lobbyhold(lobby_id=yao_text)

    x_originunit = casa_idea._originunit
    x_originunit.set_originhold(yao_text, 1)

    clean_text = "clean"
    casa_idea.add_kid(ideaunit_shop(clean_text))

    assert not casa_idea._is_expanded
    assert casa_idea.pledge
    assert casa_idea._factunits is not None
    assert casa_idea._awardlinks is not None
    assert casa_idea._doerunit is not None
    assert casa_idea._originunit is not None
    assert casa_idea._kids != {}

    # WHEN
    casa_dict = casa_idea.get_dict()

    # THEN
    assert casa_dict.get("_is_expanded") is False
    assert casa_dict.get("pledge")
    assert casa_dict.get("_factunits") is not None
    assert casa_dict.get("_awardlinks") is not None
    assert casa_dict.get("_doerunit") is not None
    assert casa_dict.get("_originunit") is not None
    assert casa_dict.get("_kids") is not None


def test_IdeaUnit_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # ESTABLISH
    casa_idea = ideaunit_shop()
    assert casa_idea._is_expanded
    assert casa_idea.pledge is False
    assert casa_idea._factunits == {}
    assert casa_idea._awardlinks == {}
    assert casa_idea._doerunit == doerunit_shop()
    assert casa_idea._healerhold == healerhold_shop()
    assert casa_idea._originunit == originunit_shop()
    assert casa_idea._kids == {}

    # WHEN
    casa_dict = casa_idea.get_dict()

    # THEN
    assert casa_dict.get("_is_expanded") is None
    assert casa_dict.get("pledge") is None
    assert casa_dict.get("_factunits") is None
    assert casa_dict.get("_awardlinks") is None
    assert casa_dict.get("_doerunit") is None
    assert casa_dict.get("_healerhold") is None
    assert casa_dict.get("_originunit") is None
    assert casa_dict.get("_kids") is None


def test_IdeaUnit_vaild_DenomCorrectInheritsBeginAndClose():
    # ESTABLISH
    casa_text = "casa"
    clean_text = "clean"
    # parent idea
    casa_idea = ideaunit_shop(_label=casa_text, _begin=22.0, _close=66.0)
    # kid idea
    clean_idea = ideaunit_shop(_label=clean_text, _numor=1, _denom=11.0, _reest=False)

    # WHEN
    casa_idea.add_kid(idea_kid=clean_idea)

    # THEN
    assert casa_idea._kids[clean_text]._begin == 2
    assert casa_idea._kids[clean_text]._close == 6
    kid_idea_expected = ideaunit_shop(
        clean_text, _numor=1, _denom=11.0, _reest=False, _begin=2, _close=6
    )
    assert casa_idea._kids[clean_text] == kid_idea_expected


def test_IdeaUnit_invaild_DenomThrowsError():
    # ESTABLISH
    casa_text = "casa"
    parent_idea = ideaunit_shop(_label=casa_text)
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
    clean_text = "clean"
    clean_road = create_road(casa_road, clean_text)
    print(f"{clean_road=}")
    kid_idea = ideaunit_shop(
        clean_text, _parent_road=casa_road, _numor=1, _denom=11.0, _reest=False
    )
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        parent_idea.add_kid(idea_kid=kid_idea)
    print(f"{str(excinfo.value)=}")
    assert (
        str(excinfo.value)
        == f"Idea {clean_road} cannot have numor,denom,reest if parent does not have begin/close range"
    )


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
    sport_idea._doerunit.set_lobbyhold(lobby_id=swim_text)
    # assert sport_idea._doerheir is None

    # WHEN
    sport_idea.set_doerheir(parent_doerheir=None, bud_lobbyboxs=None)

    # THEN
    assert sport_idea._doerheir is not None
    swim_doerunit = doerunit_shop()
    swim_doerunit.set_lobbyhold(lobby_id=swim_text)
    swim_doerheir = doerheir_shop()
    swim_doerheir.set_lobbyholds(
        doerunit=swim_doerunit, parent_doerheir=None, bud_lobbyboxs=None
    )
    assert sport_idea._doerheir == swim_doerheir


def test_IdeaUnit_get_descendants_ReturnsNoRoadUnits():
    # ESTABLISH
    nation_text = "nation-state"
    nation_idea = ideaunit_shop(_label=nation_text, _parent_road=root_label())

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads_from_kids()

    # THEN
    assert nation_descendants == {}


def test_IdeaUnit_get_descendants_Returns3DescendantsRoadUnits():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    usa_idea = ideaunit_shop(usa_text, _parent_road=nation_road)
    nation_idea.add_kid(idea_kid=usa_idea)

    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    texas_idea = ideaunit_shop(texas_text, _parent_road=usa_road)
    usa_idea.add_kid(idea_kid=texas_idea)

    iowa_text = "Iowa"
    iowa_road = create_road(usa_road, iowa_text)
    iowa_idea = ideaunit_shop(iowa_text, _parent_road=usa_road)
    usa_idea.add_kid(idea_kid=iowa_idea)

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads_from_kids()

    # THEN
    assert len(nation_descendants) == 3
    assert nation_descendants.get(usa_road) is not None
    assert nation_descendants.get(texas_road) is not None
    assert nation_descendants.get(iowa_road) is not None


def test_IdeaUnit_get_descendants_ErrorRaisedIfInfiniteLoop():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())
    nation_idea.add_kid(idea_kid=nation_idea)
    max_count = 1000

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        nation_idea.get_descendant_roads_from_kids()
    assert (
        str(excinfo.value)
        == f"Idea '{nation_idea.get_road()}' either has an infinite loop or more than {max_count} descendants."
    )


def test_IdeaUnit_clear_kids_CorrectlySetsAttr():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())
    nation_idea.add_kid(ideaunit_shop("USA", _parent_road=nation_road))
    nation_idea.add_kid(ideaunit_shop("France", _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    nation_idea.clear_kids()

    # THEN
    assert len(nation_idea._kids) == 0


def test_IdeaUnit_get_kid_ReturnsCorrectObj():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    nation_idea.add_kid(ideaunit_shop(usa_text, _parent_road=nation_road))

    france_text = "France"
    france_road = create_road(nation_road, france_text)
    nation_idea.add_kid(ideaunit_shop(france_text, _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    france_idea = nation_idea.get_kid(france_text)

    # THEN
    assert france_idea._label == france_text


def test_IdeaUnit_del_kid_CorrectModifiesAttr():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    nation_idea.add_kid(ideaunit_shop(usa_text, _parent_road=nation_road))

    france_text = "France"
    france_road = create_road(nation_road, france_text)
    nation_idea.add_kid(ideaunit_shop(france_text, _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    nation_idea.del_kid(france_text)

    # THEN
    assert len(nation_idea._kids) == 1


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
