from src.a01_way_logic.way import get_default_fisc_label as root_label, create_way
from src.a05_idea_logic.healer import healerlink_shop
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_idea import (
    reasonunit_shop,
    reasonheir_shop,
    factunit_shop,
    premiseunit_shop,
)
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_idea_logic.origin import originunit_shop
from src.a05_idea_logic.idea import ideaunit_shop, get_obj_from_idea_dict


def test_get_obj_from_idea_dict_ReturnsObj():
    # ESTABLISH
    field_str = "_is_expanded"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_str: True}, field_str)
    assert get_obj_from_idea_dict({}, field_str)
    assert get_obj_from_idea_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = "pledge"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_str: True}, field_str)
    assert get_obj_from_idea_dict({}, field_str) is False
    assert get_obj_from_idea_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = "problem_bool"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_str: True}, field_str)
    assert get_obj_from_idea_dict({}, field_str) is False
    assert get_obj_from_idea_dict({field_str: False}, field_str) is False

    # ESTABLISH
    field_str = "_kids"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_str: {}}, field_str) == {}
    assert get_obj_from_idea_dict({}, field_str) == {}


def test_get_obj_from_idea_dict_ReturnsCorrect_HealerLink():
    # ESTABLISH
    # WHEN / THEN
    healerlink_key = "healerlink"
    assert get_obj_from_idea_dict({}, healerlink_key) == healerlink_shop()

    # WHEN
    sue_str = "Sue"
    zia_str = "Zia"
    healerlink_dict = {"healerlink_healer_names": [sue_str, zia_str]}
    ideaunit_dict = {healerlink_key: healerlink_dict}

    # THEN
    static_healerlink = healerlink_shop()
    static_healerlink.set_healer_name(x_healer_name=sue_str)
    static_healerlink.set_healer_name(x_healer_name=zia_str)
    assert get_obj_from_idea_dict(ideaunit_dict, healerlink_key) is not None
    assert get_obj_from_idea_dict(ideaunit_dict, healerlink_key) == static_healerlink


def test_IdeaUnit_get_dict_ReturnsCorrectCompleteDict():
    # ESTABLISH
    week_str = "weekdays"
    week_way = create_way(root_label(), week_str)
    wed_str = "Wednesday"
    wed_way = create_way(week_way, wed_str)
    states_str = "nation-state"
    states_way = create_way(root_label(), states_str)
    usa_str = "USA"
    usa_way = create_way(states_way, usa_str)

    wed_premise = premiseunit_shop(pbranch=wed_way)
    wed_premise._status = True
    usa_premise = premiseunit_shop(pbranch=usa_way)
    usa_premise._status = False

    x1_reasonunits = {
        week_way: reasonunit_shop(
            week_way, premises={wed_premise.pbranch: wed_premise}
        ),
        states_way: reasonunit_shop(states_way, {usa_premise.pbranch: usa_premise}),
    }
    wed_premises = {wed_premise.pbranch: wed_premise}
    usa_premises = {usa_premise.pbranch: usa_premise}
    x1_reasonheirs = {
        week_way: reasonheir_shop(week_way, wed_premises, _status=True),
        states_way: reasonheir_shop(states_way, usa_premises, _status=False),
    }
    biker_awardee_title = "bikers"
    biker_give_force = 3.0
    biker_take_force = 7.0
    biker_awardlink = awardlink_shop(
        biker_awardee_title, biker_give_force, biker_take_force
    )
    flyer_awardee_title = "flyers"
    flyer_give_force = 6.0
    flyer_take_force = 9.0
    flyer_awardlink = awardlink_shop(
        awardee_title=flyer_awardee_title,
        give_force=flyer_give_force,
        take_force=flyer_take_force,
    )
    biker_and_flyer_awardlinks = {
        biker_awardlink.awardee_title: biker_awardlink,
        flyer_awardlink.awardee_title: flyer_awardlink,
    }
    biker_get_dict = {
        "awardee_title": biker_awardlink.awardee_title,
        "give_force": biker_awardlink.give_force,
        "take_force": biker_awardlink.take_force,
    }
    flyer_get_dict = {
        "awardee_title": flyer_awardlink.awardee_title,
        "give_force": flyer_awardlink.give_force,
        "take_force": flyer_awardlink.take_force,
    }
    x1_awardlinks = {
        biker_awardee_title: biker_get_dict,
        flyer_awardee_title: flyer_get_dict,
    }
    sue_str = "Sue"
    yao_str = "Yao"
    sue_laborunit = laborunit_shop({sue_str: -1, yao_str: -1})
    yao_healerlink = healerlink_shop({yao_str})
    casa_str = "casa"
    casa_way = create_way(root_label(), casa_str)
    x_problem_bool = True
    casa_idea = ideaunit_shop(
        parent_way=casa_way,
        _kids=None,
        awardlinks=biker_and_flyer_awardlinks,
        mass=30,
        idea_label=casa_str,
        _level=1,
        reasonunits=x1_reasonunits,
        _reasonheirs=x1_reasonheirs,
        laborunit=sue_laborunit,
        healerlink=yao_healerlink,
        _active=True,
        pledge=True,
        problem_bool=x_problem_bool,
    )
    x_factunit = factunit_shop(fcontext=week_way, fbranch=week_way, fopen=5, fnigh=59)
    casa_idea.set_factunit(factunit=x_factunit)
    casa_idea._originunit.set_originhold(acct_name="Ray", importance=None)
    casa_idea._originunit.set_originhold(acct_name="Lei", importance=4)
    x_begin = 11
    x_close = 12
    x_addin = 13
    x_denom = 14
    x_numor = 15
    x_morph = 16
    x_gogo_want = 81
    x_stop_want = 87
    casa_idea.begin = x_begin
    casa_idea.close = x_close
    casa_idea.addin = x_addin
    casa_idea.denom = x_denom
    casa_idea.numor = x_numor
    casa_idea.morph = x_morph
    casa_idea.gogo_want = x_gogo_want
    casa_idea.stop_want = x_stop_want
    casa_idea._uid = 17
    casa_idea.add_kid(ideaunit_shop("paper"))

    # WHEN
    casa_dict = casa_idea.get_dict()

    # THEN
    assert casa_dict is not None
    assert len(casa_dict["_kids"]) == 1
    assert casa_dict["_kids"] == casa_idea.get_kids_dict()
    assert casa_dict["reasonunits"] == casa_idea.get_reasonunits_dict()
    assert casa_dict["awardlinks"] == casa_idea.get_awardlinks_dict()
    assert casa_dict["awardlinks"] == x1_awardlinks
    assert casa_dict["laborunit"] == sue_laborunit.get_dict()
    assert casa_dict["healerlink"] == yao_healerlink.get_dict()
    assert casa_dict["originunit"] == casa_idea.get_originunit_dict()
    assert casa_dict["mass"] == casa_idea.mass
    assert casa_dict["idea_label"] == casa_idea.idea_label
    assert casa_dict["_uid"] == casa_idea._uid
    assert casa_dict["begin"] == casa_idea.begin
    assert casa_dict["close"] == casa_idea.close
    assert casa_dict["numor"] == casa_idea.numor
    assert casa_dict["denom"] == casa_idea.denom
    assert casa_dict["morph"] == casa_idea.morph
    assert casa_dict["gogo_want"] == casa_idea.gogo_want
    assert casa_dict["stop_want"] == casa_idea.stop_want
    assert casa_dict["pledge"] == casa_idea.pledge
    assert casa_dict["problem_bool"] == casa_idea.problem_bool
    assert casa_dict["problem_bool"] == x_problem_bool
    assert casa_idea._is_expanded
    assert casa_dict.get("_is_expanded") is None
    assert len(casa_dict["factunits"]) == len(casa_idea.get_factunits_dict())


def test_IdeaUnit_get_dict_ReturnsCorrectDictWithoutEmptyAttributes():
    # ESTABLISH
    casa_idea = ideaunit_shop()

    # WHEN
    casa_dict = casa_idea.get_dict()

    # THEN
    assert casa_dict is not None
    assert casa_dict == {"mass": 1}


def test_IdeaUnit_get_dict_ReturnsDictWith_attrs_CorrectlySetTrue():
    # ESTABLISH
    casa_idea = ideaunit_shop()
    casa_idea._is_expanded = False
    casa_idea.pledge = True
    ignore_str = "ignore"

    a_str = "a"
    a_way = create_way(root_label(), a_str)
    casa_idea.set_factunit(factunit_shop(a_way, a_way))

    yao_str = "Yao"
    casa_idea.set_awardlink(awardlink_shop(yao_str))

    x_laborunit = casa_idea.laborunit
    x_laborunit.set_laborlink(labor_title=yao_str)

    x_originunit = casa_idea._originunit
    x_originunit.set_originhold(yao_str, 1)

    clean_str = "clean"
    casa_idea.add_kid(ideaunit_shop(clean_str))

    assert not casa_idea._is_expanded
    assert casa_idea.pledge
    assert casa_idea.factunits is not None
    assert casa_idea.awardlinks is not None
    assert casa_idea.laborunit is not None
    assert casa_idea._originunit is not None
    assert casa_idea._kids != {}

    # WHEN
    casa_dict = casa_idea.get_dict()

    # THEN
    assert casa_dict.get("_is_expanded") is False
    assert casa_dict.get("pledge")
    assert casa_dict.get("factunits") is not None
    assert casa_dict.get("awardlinks") is not None
    assert casa_dict.get("laborunit") is not None
    assert casa_dict.get("originunit") is not None
    assert casa_dict.get("_kids") is not None


def test_IdeaUnit_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # ESTABLISH
    casa_idea = ideaunit_shop()
    assert casa_idea._is_expanded
    assert casa_idea.pledge is False
    assert casa_idea.factunits == {}
    assert casa_idea.awardlinks == {}
    assert casa_idea.laborunit == laborunit_shop()
    assert casa_idea.healerlink == healerlink_shop()
    assert casa_idea._originunit == originunit_shop()
    assert casa_idea._kids == {}

    # WHEN
    casa_dict = casa_idea.get_dict()

    # THEN
    assert casa_dict.get("_is_expanded") is None
    assert casa_dict.get("pledge") is None
    assert casa_dict.get("factunits") is None
    assert casa_dict.get("awardlinks") is None
    assert casa_dict.get("laborunit") is None
    assert casa_dict.get("healerlink") is None
    assert casa_dict.get("originunit") is None
    assert casa_dict.get("_kids") is None
