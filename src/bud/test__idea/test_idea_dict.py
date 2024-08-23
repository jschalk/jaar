from src._road.road import get_default_real_id_roadnode as root_label, create_road
from src.bud.healer import healerhold_shop
from src.bud.group import awardlink_shop
from src.bud.reason_idea import (
    reasonunit_shop,
    reasonheir_shop,
    factunit_shop,
    premiseunit_shop,
)
from src.bud.reason_doer import doerunit_shop
from src.bud.origin import originunit_shop
from src.bud.idea import ideaunit_shop, get_obj_from_idea_dict


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
    healerhold_dict = {"healerhold_group_ids": [sue_text, zia_text]}
    ideaunit_dict = {healerhold_key: healerhold_dict}

    # THEN
    static_healerhold = healerhold_shop()
    static_healerhold.set_group_id(x_group_id=sue_text)
    static_healerhold.set_group_id(x_group_id=zia_text)
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
    biker_group_id = "bikers"
    biker_give_force = 3.0
    biker_take_force = 7.0
    biker_awardlink = awardlink_shop(biker_group_id, biker_give_force, biker_take_force)
    flyer_group_id = "flyers"
    flyer_give_force = 6.0
    flyer_take_force = 9.0
    flyer_awardlink = awardlink_shop(
        group_id=flyer_group_id,
        give_force=flyer_give_force,
        take_force=flyer_take_force,
    )
    biker_and_flyer_awardlinks = {
        biker_awardlink.group_id: biker_awardlink,
        flyer_awardlink.group_id: flyer_awardlink,
    }
    biker_get_dict = {
        "group_id": biker_awardlink.group_id,
        "give_force": biker_awardlink.give_force,
        "take_force": biker_awardlink.take_force,
    }
    flyer_get_dict = {
        "group_id": flyer_awardlink.group_id,
        "give_force": flyer_awardlink.give_force,
        "take_force": flyer_awardlink.take_force,
    }
    x1_awardlinks = {biker_group_id: biker_get_dict, flyer_group_id: flyer_get_dict}
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
        _mass=30,
        _label=casa_text,
        _level=1,
        _reasonunits=x1_reasonunits,
        _reasonheirs=x1_reasonheirs,
        _doerunit=sue_doerunit,
        _healerhold=yao_healerhold,
        _active=True,
        pledge=True,
        _problem_bool=x_problem_bool,
    )
    factunit_x = factunit_shop(base=week_road, pick=week_road, open=5, nigh=59)
    casa_idea.set_factunit(factunit=factunit_x)
    casa_idea._originunit.set_originhold(acct_id="Ray", importance=None)
    casa_idea._originunit.set_originhold(acct_id="Lei", importance=4)
    x_begin = 11
    x_close = 12
    x_addin = 13
    x_denom = 14
    x_numor = 15
    x_morph = 16
    x_gogo_want = 81
    x_stop_want = 87
    casa_idea._begin = x_begin
    casa_idea._close = x_close
    casa_idea._addin = x_addin
    casa_idea._denom = x_denom
    casa_idea._numor = x_numor
    casa_idea._morph = x_morph
    casa_idea._gogo_want = x_gogo_want
    casa_idea._stop_want = x_stop_want
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
    assert casa_dict["_mass"] == casa_idea._mass
    assert casa_dict["_label"] == casa_idea._label
    assert casa_dict["_uid"] == casa_idea._uid
    assert casa_dict["_begin"] == casa_idea._begin
    assert casa_dict["_close"] == casa_idea._close
    assert casa_dict["_numor"] == casa_idea._numor
    assert casa_dict["_denom"] == casa_idea._denom
    assert casa_dict["_morph"] == casa_idea._morph
    assert casa_dict["_gogo_want"] == casa_idea._gogo_want
    assert casa_dict["_stop_want"] == casa_idea._stop_want
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
    assert casa_dict == {"_mass": 1}


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
    x_doerunit.set_grouphold(group_id=yao_text)

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
