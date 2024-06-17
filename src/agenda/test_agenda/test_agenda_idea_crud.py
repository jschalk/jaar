from src.agenda.healer import healerhold_shop
from src.agenda.examples.example_agendas import get_agenda_with_4_levels
from src.agenda.idea import ideaunit_shop
from src.agenda.reason_idea import reasonunit_shop, factunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.belief import balancelink_shop
from pytest import raises as pytest_raises
from src._road.road import default_road_delimiter_if_none


def test_AgendaUnit_add_idea_RaisesErrorWhen_parent_road_IsInvalid():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")
    invalid_rootnode_swim_road = "swimming"
    assert invalid_rootnode_swim_road != zia_agenda._real_id
    casa_text = "casa"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_agenda.add_idea(
            ideaunit_shop(casa_text), parent_road=invalid_rootnode_swim_road
        )
    assert (
        str(excinfo.value)
        == f"add_idea failed because parent_road '{invalid_rootnode_swim_road}' has an invalid root node"
    )


def test_AgendaUnit_add_idea_RaisesErrorWhen_parent_road_IdeaDoesNotExist():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")
    swim_road = zia_agenda.make_l1_road("swimming")
    casa_text = "casa"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_agenda.add_idea(
            ideaunit_shop(casa_text),
            parent_road=swim_road,
            create_missing_ancestors=False,
        )
    assert (
        str(excinfo.value)
        == f"add_idea failed because '{swim_road}' idea does not exist."
    )


def test_AgendaUnit_add_idea_RaisesErrorWhen_label_IsNotNode():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")
    swim_road = zia_agenda.make_l1_road("swimming")
    casa_text = "casa"
    casa_road = zia_agenda.make_l1_road(casa_text)
    run_text = "run"
    run_road = zia_agenda.make_road(casa_road, run_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_agenda.add_idea(ideaunit_shop(run_road), parent_road=swim_road)
    assert (
        str(excinfo.value) == f"add_idea failed because '{run_road}' is not a RoadNode."
    )


def test_AgendaUnit_add_l1_idea_CorrectlySetsAttr():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")
    casa_text = "casa"
    casa_road = zia_agenda.make_l1_road(casa_text)
    assert zia_agenda.idea_exists(casa_road) is False

    # WHEN
    zia_agenda.add_l1_idea(ideaunit_shop(casa_text))

    # THEN
    assert zia_agenda.idea_exists(casa_road)


def test_AgendaUnit_IdeaUnit_kids_CanHaveKids():
    # GIVEN / WHEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._weight == 10
    assert sue_agenda._idearoot._kids
    print(f"{len(sue_agenda._idearoot._kids)=} {sue_agenda._idearoot._parent_road=}")
    assert sue_agenda.get_level_count(level=0) == 1
    weekdays_kids = sue_agenda._idearoot._kids["weekdays"]._kids
    weekdays_len = len(weekdays_kids)
    print(f"{weekdays_len=} {sue_agenda._idearoot._parent_road=}")
    # for idea in weekdays_kids.values():
    #     print(f"{idea._label=}")
    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=1) == 4
    assert sue_agenda.get_level_count(level=2) == 10
    assert sue_agenda.get_level_count(level=3) == 2


def test_AgendaUnit_add_idea_CanAddKidTo_idearoot():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.calc_agenda_metrics()

    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=1) == 4

    new_idea_parent_road = sue_agenda._real_id

    # WHEN
    sue_agenda.add_idea(ideaunit_shop("new_idea"), parent_road=new_idea_parent_road)
    sue_agenda.calc_agenda_metrics()

    # THEN
    print(f"{(sue_agenda._owner_id == new_idea_parent_road[0])=}")
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_agenda.get_idea_count() == 18
    assert sue_agenda.get_level_count(level=1) == 5


def test_AgendaUnit_add_idea_CanAddKidToKidIdea():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=2) == 10

    # WHEN
    new_idea_parent_road = sue_agenda.make_l1_road("casa")
    sue_agenda.add_idea(ideaunit_shop("new_york"), parent_road=new_idea_parent_road)
    sue_agenda.calc_agenda_metrics()

    # THEN
    # print(f"{(sue_agenda._owner_id == new_idea_parent_road[0])=}")
    # print(sue_agenda._idearoot._kids["casa"])
    # print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_agenda.get_idea_count() == 18
    assert sue_agenda.get_level_count(level=2) == 11
    new_york_idea = sue_agenda._idearoot._kids["casa"]._kids["new_york"]
    assert new_york_idea._parent_road == sue_agenda.make_l1_road("casa")
    assert new_york_idea._road_delimiter == sue_agenda._road_delimiter
    new_york_idea.set_parent_road(parent_road="testing")
    assert (
        sue_agenda._idearoot._kids["casa"]._kids["new_york"]._parent_road == "testing"
    )
    assert sue_agenda.get_intent_dict()


def test_AgendaUnit_add_idea_CanAddKidToGrandkidIdea():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.calc_agenda_metrics()

    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=3) == 2
    wkday_road = sue_agenda.make_l1_road("weekdays")
    new_idea_parent_road = sue_agenda.make_road(wkday_road, "Wednesday")

    # WHEN
    sue_agenda.add_idea(ideaunit_shop("new_idea"), parent_road=new_idea_parent_road)
    sue_agenda.calc_agenda_metrics()

    # THEN
    print(f"{(sue_agenda._owner_id == new_idea_parent_road[0])=}")
    print(sue_agenda._idearoot._kids["casa"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_agenda.get_idea_count() == 18
    assert sue_agenda.get_level_count(level=3) == 3


def test_AgendaUnit_add_idea_CorrectlyAddsIdeaObjWithNonstandard_delimiter():
    # GIVEN
    slash_text = "/"
    assert slash_text != default_road_delimiter_if_none()
    bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_text)
    casa_text = "casa"
    week_text = "week"
    wed_text = "Wednesday"
    casa_road = bob_agenda.make_l1_road(casa_text)
    week_road = bob_agenda.make_l1_road(week_text)
    wed_road = bob_agenda.make_road(week_road, wed_text)
    bob_agenda.add_l1_idea(ideaunit_shop(casa_text))
    bob_agenda.add_l1_idea(ideaunit_shop(week_text))
    bob_agenda.add_idea(ideaunit_shop(wed_text), week_road)
    print(f"{bob_agenda._idearoot._kids.keys()=}")
    assert len(bob_agenda._idearoot._kids) == 2
    wed_idea = bob_agenda.get_idea_obj(wed_road)
    assert wed_idea._road_delimiter == slash_text
    assert wed_idea._road_delimiter == bob_agenda._road_delimiter

    # WHEN
    bob_agenda.edit_idea_attr(
        road=casa_road, reason_base=week_road, reason_premise=wed_road
    )

    # THEN
    casa_idea = bob_agenda.get_idea_obj(casa_road)
    assert casa_idea._reasonunits.get(week_road) != None


def test_AgendaUnit_add_idea_CanCreateRoadUnitToGrandkidIdea():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.calc_agenda_metrics()

    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=3) == 2
    ww2_road = sue_agenda.make_l1_road("ww2")
    battles_road = sue_agenda.make_road(ww2_road, "battles")
    new_idea_parent_road = sue_agenda.make_road(battles_road, "coralsea")
    new_idea = ideaunit_shop(_label="USS Saratoga")

    # WHEN
    sue_agenda.add_idea(new_idea, parent_road=new_idea_parent_road)
    sue_agenda.calc_agenda_metrics()

    # THEN
    print(sue_agenda._idearoot._kids["ww2"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_agenda._idearoot._kids["ww2"]._label == "ww2"
    assert sue_agenda._idearoot._kids["ww2"]._kids["battles"]._label == "battles"
    assert sue_agenda.get_idea_count() == 21
    assert sue_agenda.get_level_count(level=3) == 3


def test_AgendaUnit_add_idea_CreatesIdeaUnitsreferencedBy_reasonunits():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.calc_agenda_metrics()

    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=3) == 2
    casa_road = sue_agenda.make_l1_road("casa")
    new_idea_parent_road = sue_agenda.make_road(casa_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(clean_cookery_text, _weight=40, pledge=True)

    buildings_text = "buildings"
    buildings_road = sue_agenda.make_l1_road(buildings_text)
    cookery_room_text = "cookery"
    cookery_room_road = sue_agenda.make_road(buildings_road, cookery_room_text)
    cookery_dirty_text = "dirty"
    cookery_dirty_road = sue_agenda.make_road(cookery_room_road, cookery_dirty_text)
    reason_x = reasonunit_shop(base=cookery_room_road)
    reason_x.set_premise(premise=cookery_dirty_road)
    clean_cookery_idea.set_reasonunit(reason=reason_x)

    assert sue_agenda._idearoot.get_kid(buildings_text) is None

    # WHEN
    sue_agenda.add_idea(
        idea_kid=clean_cookery_idea,
        parent_road=new_idea_parent_road,
        create_missing_ideas=True,
    )
    sue_agenda.calc_agenda_metrics()

    # THEN
    print(f"{(len(new_idea_parent_road) == 1)=}")
    # for idea_kid in sue_agenda._idearoot._kids.values():
    #     print(f"{idea_kid._label=}")
    assert sue_agenda._idearoot.get_kid(buildings_text) != None
    assert sue_agenda.get_idea_obj(road=buildings_road) != None
    assert sue_agenda.get_idea_obj(road=cookery_dirty_road) != None
    assert sue_agenda.get_idea_count() == 22
    assert sue_agenda.get_level_count(level=3) == 4


def test_AgendaUnit_add_idea_CorrectlySets_agenda_real_id():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    agenda_real_id = "Texas"
    sue_agenda.set_real_id(real_id=agenda_real_id)
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._real_id == agenda_real_id

    casa_road = sue_agenda.make_l1_road("casa")
    clean_road = sue_agenda.make_road(casa_road, "cleaning")
    cookery_text = "cookery ready to use"
    cookery_road = sue_agenda.make_road(clean_road, cookery_text)

    # WHEN
    sue_agenda.add_idea(ideaunit_shop(cookery_text), clean_road)

    # THEN
    cookery_idea = sue_agenda.get_idea_obj(cookery_road)
    assert cookery_idea._agenda_real_id == agenda_real_id


def test_AgendaUnit_del_idea_obj_Level0CannotBeDeleted():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    root_road = sue_agenda._real_id

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.del_idea_obj(road=root_road)
    assert str(excinfo.value) == "Idearoot cannot be deleted"


def test_AgendaUnit_del_idea_obj_Level1CanBeDeleted_ChildrenDeleted():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = sue_agenda.make_road(week_road, sun_text)
    assert sue_agenda.get_idea_obj(road=week_road)
    assert sue_agenda.get_idea_obj(road=sun_road)

    # WHEN
    sue_agenda.del_idea_obj(road=week_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=week_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{week_road}'"
    new_sunday_road = sue_agenda.make_l1_road("Sunday")
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=new_sunday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{new_sunday_road}'"


def test_AgendaUnit_del_idea_obj_Level1CanBeDeleted_ChildrenInherited():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.calc_agenda_metrics()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    old_sunday_road = sue_agenda.make_road(week_road, sun_text)
    assert sue_agenda.get_idea_obj(road=old_sunday_road)

    # WHEN
    sue_agenda.del_idea_obj(road=week_road, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=old_sunday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{old_sunday_road}'"
    new_sunday_road = sue_agenda.make_l1_road(sun_text)
    assert sue_agenda.get_idea_obj(road=new_sunday_road)
    new_sunday_idea = sue_agenda.get_idea_obj(road=new_sunday_road)
    assert new_sunday_idea._parent_road == sue_agenda._real_id


def test_AgendaUnit_del_idea_obj_LevelNCanBeDeleted_ChildrenInherited():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    texas_text = "Texas"
    oregon_text = "Oregon"
    usa_texas_road = sue_agenda.make_road(usa_road, texas_text)
    usa_oregon_road = sue_agenda.make_road(usa_road, oregon_text)
    states_texas_road = sue_agenda.make_road(states_road, texas_text)
    states_oregon_road = sue_agenda.make_road(states_road, oregon_text)
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._idea_dict.get(usa_road) != None
    assert sue_agenda._idea_dict.get(usa_texas_road) != None
    assert sue_agenda._idea_dict.get(usa_oregon_road) != None
    assert sue_agenda._idea_dict.get(states_texas_road) is None
    assert sue_agenda._idea_dict.get(states_oregon_road) is None

    # WHEN
    sue_agenda.del_idea_obj(road=usa_road, del_children=False)

    # THEN
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._idea_dict.get(states_texas_road) != None
    assert sue_agenda._idea_dict.get(states_oregon_road) != None
    assert sue_agenda._idea_dict.get(usa_texas_road) is None
    assert sue_agenda._idea_dict.get(usa_oregon_road) is None
    assert sue_agenda._idea_dict.get(usa_road) is None


def test_AgendaUnit_del_idea_obj_Level2CanBeDeleted_ChildrenDeleted():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    wkday_road = sue_agenda.make_l1_road("weekdays")
    monday_road = sue_agenda.make_road(wkday_road, "Monday")
    assert sue_agenda.get_idea_obj(road=monday_road)

    # WHEN
    sue_agenda.del_idea_obj(road=monday_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=monday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{monday_road}'"


def test_AgendaUnit_del_idea_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    texas_text = "Texas"
    usa_texas_road = sue_agenda.make_road(usa_road, texas_text)
    assert sue_agenda.get_idea_obj(road=usa_texas_road)

    # WHEN
    sue_agenda.del_idea_obj(road=usa_texas_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=usa_texas_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{usa_texas_road}'"


def test_AgendaUnit_edit_idea_attr_IsAbleToEditAnyAncestor_Idea():
    sue_agenda = get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = sue_agenda.make_l1_road(casa_text)
    print(f"{casa_road=}")
    old_weight = sue_agenda._idearoot._kids[casa_text]._weight
    assert old_weight == 30
    sue_agenda.edit_idea_attr(road=casa_road, weight=23)
    new_weight = sue_agenda._idearoot._kids[casa_text]._weight
    assert new_weight == 23

    # uid: int = None,
    sue_agenda._idearoot._kids[casa_text]._uid = 34
    x_uid = sue_agenda._idearoot._kids[casa_text]._uid
    assert x_uid == 34
    sue_agenda.edit_idea_attr(road=casa_road, uid=23)
    uid_new = sue_agenda._idearoot._kids[casa_text]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    sue_agenda._idearoot._kids[casa_text]._begin = 39
    x_begin = sue_agenda._idearoot._kids[casa_text]._begin
    assert x_begin == 39
    sue_agenda._idearoot._kids[casa_text]._close = 43
    x_close = sue_agenda._idearoot._kids[casa_text]._close
    assert x_close == 43
    sue_agenda.edit_idea_attr(road=casa_road, begin=25, close=29)
    assert sue_agenda._idearoot._kids[casa_text]._begin == 25
    assert sue_agenda._idearoot._kids[casa_text]._close == 29

    # factunit: factunit_shop = None,
    # sue_agenda._idearoot._kids[casa_text]._factunits = None
    assert sue_agenda._idearoot._kids[casa_text]._factunits == {}
    wkdays_road = sue_agenda.make_l1_road("weekdays")
    fact_road = sue_agenda.make_road(wkdays_road, "Sunday")
    factunit_x = factunit_shop(base=fact_road, pick=fact_road)

    casa_factunits = sue_agenda._idearoot._kids[casa_text]._factunits
    print(f"{casa_factunits=}")
    sue_agenda.edit_idea_attr(road=casa_road, factunit=factunit_x)
    casa_factunits = sue_agenda._idearoot._kids[casa_text]._factunits
    print(f"{casa_factunits=}")
    assert sue_agenda._idearoot._kids[casa_text]._factunits == {
        factunit_x.base: factunit_x
    }

    # _descendant_pledge_count: int = None,
    sue_agenda._idearoot._kids[casa_text]._descendant_pledge_count = 81
    x_descendant_pledge_count = sue_agenda._idearoot._kids[
        casa_text
    ]._descendant_pledge_count
    assert x_descendant_pledge_count == 81
    sue_agenda.edit_idea_attr(road=casa_road, descendant_pledge_count=67)
    _descendant_pledge_count_new = sue_agenda._idearoot._kids[
        casa_text
    ]._descendant_pledge_count
    assert _descendant_pledge_count_new == 67

    # _all_other_cred: bool = None,
    sue_agenda._idearoot._kids[casa_text]._all_other_cred = 74
    x_all_other_cred = sue_agenda._idearoot._kids[casa_text]._all_other_cred
    assert x_all_other_cred == 74
    sue_agenda.edit_idea_attr(road=casa_road, all_other_cred=59)
    _all_other_cred_new = sue_agenda._idearoot._kids[casa_text]._all_other_cred
    assert _all_other_cred_new == 59

    # _all_other_debt: bool = None,
    sue_agenda._idearoot._kids[casa_text]._all_other_debt = 74
    x_all_other_debt = sue_agenda._idearoot._kids[casa_text]._all_other_debt
    assert x_all_other_debt == 74
    sue_agenda.edit_idea_attr(road=casa_road, all_other_debt=59)
    _all_other_debt_new = sue_agenda._idearoot._kids[casa_text]._all_other_debt
    assert _all_other_debt_new == 59

    # _balancelink: dict = None,
    sue_agenda._idearoot._kids[casa_text]._balancelinks = {
        "fun": balancelink_shop(belief_id="fun", credor_weight=1, debtor_weight=7)
    }
    _balancelinks = sue_agenda._idearoot._kids[casa_text]._balancelinks
    assert _balancelinks == {
        "fun": balancelink_shop(belief_id="fun", credor_weight=1, debtor_weight=7)
    }
    sue_agenda.edit_idea_attr(
        road=casa_road,
        balancelink=balancelink_shop(belief_id="fun", credor_weight=4, debtor_weight=8),
    )
    assert sue_agenda._idearoot._kids[casa_text]._balancelinks == {
        "fun": balancelink_shop(belief_id="fun", credor_weight=4, debtor_weight=8)
    }

    # _is_expanded: dict = None,
    sue_agenda._idearoot._kids[casa_text]._is_expanded = "what"
    _is_expanded = sue_agenda._idearoot._kids[casa_text]._is_expanded
    assert _is_expanded == "what"
    sue_agenda.edit_idea_attr(road=casa_road, is_expanded=True)
    assert sue_agenda._idearoot._kids[casa_text]._is_expanded == True

    # pledge: dict = None,
    sue_agenda._idearoot._kids[casa_text].pledge = "funfun3"
    pledge = sue_agenda._idearoot._kids[casa_text].pledge
    assert pledge == "funfun3"
    sue_agenda.edit_idea_attr(road=casa_road, pledge=True)
    assert sue_agenda._idearoot._kids[casa_text].pledge == True

    # _range_source_road: dict = None,
    sue_agenda._idearoot._kids[casa_text]._range_source_road = "fun3rol"
    range_source_road = sue_agenda._idearoot._kids[casa_text]._range_source_road
    assert range_source_road == "fun3rol"
    end_road = sue_agenda.make_road(casa_road, "end")
    sue_agenda.edit_idea_attr(road=casa_road, range_source_road=end_road)
    assert sue_agenda._idearoot._kids[casa_text]._range_source_road == end_road

    # _healerhold:
    sue_agenda._idearoot._kids[casa_text]._healerhold = "fun3rol"
    src_healerhold = sue_agenda._idearoot._kids[casa_text]._healerhold
    assert src_healerhold == "fun3rol"
    sue_text = "Sue"
    yao_text = "Yao"
    x_healerhold = healerhold_shop({sue_text, yao_text})
    sue_agenda.add_otherunit(sue_text)
    sue_agenda.add_otherunit(yao_text)
    sue_agenda.edit_idea_attr(road=casa_road, healerhold=x_healerhold)
    assert sue_agenda._idearoot._kids[casa_text]._healerhold == x_healerhold

    # _problem_bool: bool
    sue_agenda._idearoot._kids[casa_text]._problem_bool = "fun3rol"
    src_problem_bool = sue_agenda._idearoot._kids[casa_text]._problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True
    sue_agenda.edit_idea_attr(road=casa_road, problem_bool=x_problem_bool)
    assert sue_agenda._idearoot._kids[casa_text]._problem_bool == x_problem_bool

    print(f"{casa_road=} {end_road=}")


def test_AgendaUnit_edit_idea_attr_agendaIsAbleToEdit_meld_strategy_AnyIdeaIfInvaildThrowsError():
    sue_agenda = get_agenda_with_4_levels()
    casa_road = sue_agenda.make_l1_road("casa")

    # WHEN / THEN
    ineligible_meld_strategy = "yahoo9"
    with pytest_raises(Exception) as excinfo:
        sue_agenda.edit_idea_attr(casa_road, meld_strategy=ineligible_meld_strategy)
    assert (
        str(excinfo.value)
        == f"'{ineligible_meld_strategy}' is ineligible meld_strategy."
    )


def test_AgendaUnit_edit_idea_attr_agendaIsAbleToEditDenomAnyIdeaIfInvaildDenomThrowsError():
    yao_agenda = agendaunit_shop("Yao")
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_idea_attr(road="", denom=46)
    assert str(excinfo.value) == "Root Idea cannot have numor denom reest."

    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    casa_idea = ideaunit_shop(casa_text)
    yao_agenda.add_l1_idea(casa_idea)
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    clean_road = yao_agenda.make_road(casa_road, clean_text)
    yao_agenda.add_idea(clean_idea, parent_road=casa_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_idea_attr(road=clean_road, denom=46)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{clean_road}' if parent '{casa_road}' or ideaunit._numeric_road does not have begin/close range"
    )

    # GIVEN
    yao_agenda.edit_idea_attr(road=casa_road, begin=44, close=110)
    yao_agenda.edit_idea_attr(road=clean_road, denom=11)
    clean_idea = yao_agenda.get_idea_obj(road=clean_road)
    assert clean_idea._begin == 4
    assert clean_idea._close == 10


def test_AgendaUnit_edit_idea_attr_agendaIsAbleToEditDenomAnyIdeaInvaildDenomThrowsError():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    casa = "casa"
    w_road = yao_agenda.make_l1_road(casa)
    casa_idea = ideaunit_shop(casa, _begin=8, _close=14)
    yao_agenda.add_l1_idea(casa_idea)

    clean = "clean"
    clean_idea = ideaunit_shop(clean, _denom=1)
    c_road = yao_agenda.make_road(w_road, clean)
    yao_agenda.add_idea(clean_idea, parent_road=w_road)

    clean_idea = yao_agenda.get_idea_obj(road=c_road)

    day = "day_range"
    day_idea = ideaunit_shop(day, _begin=44, _close=110)
    day_road = yao_agenda.make_l1_road(day)
    yao_agenda.add_l1_idea(day_idea)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_idea_attr(road=c_road, numeric_road=day_road)
    assert (
        str(excinfo.value)
        == "Idea has begin-close range parent, cannot have numeric_road"
    )

    yao_agenda.edit_idea_attr(road=w_road, numeric_road=day_road)


def test_AgendaUnit_edit_idea_attr_agendaWhenParentAndNumeric_roadBothHaveRangeThrowError():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    yao_agenda.add_l1_idea(ideaunit_shop(casa_text))
    day_text = "day_range"
    day_idea = ideaunit_shop(day_text, _begin=44, _close=110)
    day_road = yao_agenda.make_l1_road(day_text)
    yao_agenda.add_l1_idea(day_idea)

    casa_idea = yao_agenda.get_idea_obj(road=casa_road)
    assert casa_idea._begin is None
    assert casa_idea._close is None

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_idea_attr(road=casa_road, denom=11)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{casa_road}' if parent '{yao_agenda._real_id}' or ideaunit._numeric_road does not have begin/close range"
    )

    # WHEN
    yao_agenda.edit_idea_attr(road=casa_road, numeric_road=day_road)

    # THEN
    casa_idea3 = yao_agenda.get_idea_obj(road=casa_road)
    assert casa_idea3._addin is None
    assert casa_idea3._numor is None
    assert casa_idea3._denom is None
    assert casa_idea3._reest is None
    assert casa_idea3._begin == 44
    assert casa_idea3._close == 110
    yao_agenda.edit_idea_attr(road=casa_road, denom=11, numeric_road=day_road)
    assert casa_idea3._begin == 4
    assert casa_idea3._close == 10
    assert casa_idea3._numor == 1
    assert casa_idea3._denom == 11
    assert casa_idea3._reest is False
    assert casa_idea3._addin == 0


def test_AgendaUnit_edit_idea_attr_RaisesErrorWhen_healerhold_belief_ids_DoNotExist():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    yao_agenda.add_l1_idea(ideaunit_shop(casa_text))
    day_text = "day_range"
    day_idea = ideaunit_shop(day_text, _begin=44, _close=110)
    day_road = yao_agenda.make_l1_road(day_text)
    yao_agenda.add_l1_idea(day_idea)

    casa_idea = yao_agenda.get_idea_obj(road=casa_road)
    assert casa_idea._begin is None
    assert casa_idea._close is None

    # WHEN / THEN
    sue_text = "Sue"
    x_healerhold = healerhold_shop({sue_text})
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_idea_attr(road=casa_road, healerhold=x_healerhold)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit healerhold because belief_id '{sue_text}' does not exist as belief in Agenda"
    )


def test_AgendaUnit_add_idea_MustReorderKidsDictToBeAlphabetical():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    casa_text = "casa"
    noa_agenda.add_l1_idea(ideaunit_shop(casa_text))
    swim_text = "swim"
    noa_agenda.add_l1_idea(ideaunit_shop(swim_text))

    # WHEN
    idea_list = list(noa_agenda._idearoot._kids.values())

    # THEN
    assert idea_list[0]._label == casa_text


def test_AgendaUnit_add_idea_adoptee_RaisesErrorIfAdopteeIdeaDoesNotHaveCorrectParent():
    noa_agenda = agendaunit_shop("Noa")
    sports_text = "sports"
    sports_road = noa_agenda.make_l1_road(sports_text)
    noa_agenda.add_l1_idea(ideaunit_shop(sports_text))
    swim_text = "swim"
    noa_agenda.add_idea(ideaunit_shop(swim_text), parent_road=sports_road)

    # WHEN / THEN
    summer_text = "summer"
    hike_text = "hike"
    hike_road = noa_agenda.make_road(sports_road, hike_text)
    with pytest_raises(Exception) as excinfo:
        noa_agenda.add_idea(
            idea_kid=ideaunit_shop(summer_text),
            parent_road=sports_road,
            adoptees=[swim_text, hike_text],
        )
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{hike_road}'"


def test_AgendaUnit_add_idea_adoptee_CorrectlyAddsAdoptee():
    noa_agenda = agendaunit_shop("Noa")
    sports_text = "sports"
    sports_road = noa_agenda.make_l1_road(sports_text)
    noa_agenda.add_l1_idea(ideaunit_shop(sports_text))
    swim_text = "swim"
    noa_agenda.add_idea(ideaunit_shop(swim_text), parent_road=sports_road)
    hike_text = "hike"
    noa_agenda.add_idea(ideaunit_shop(hike_text), parent_road=sports_road)

    noa_agenda.calc_agenda_metrics()
    sports_swim_road = noa_agenda.make_road(sports_road, swim_text)
    sports_hike_road = noa_agenda.make_road(sports_road, hike_text)
    assert noa_agenda._idea_dict.get(sports_swim_road) != None
    assert noa_agenda._idea_dict.get(sports_hike_road) != None
    summer_text = "summer"
    summer_road = noa_agenda.make_road(sports_road, summer_text)
    summer_swim_road = noa_agenda.make_road(summer_road, swim_text)
    summer_hike_road = noa_agenda.make_road(summer_road, hike_text)
    assert noa_agenda._idea_dict.get(summer_swim_road) is None
    assert noa_agenda._idea_dict.get(summer_hike_road) is None

    # WHEN / THEN
    noa_agenda.add_idea(
        idea_kid=ideaunit_shop(summer_text),
        parent_road=sports_road,
        adoptees=[swim_text, hike_text],
    )

    # THEN
    summer_idea = noa_agenda.get_idea_obj(summer_road)
    print(f"{summer_idea._kids.keys()=}")
    noa_agenda.calc_agenda_metrics()
    assert noa_agenda._idea_dict.get(summer_swim_road) != None
    assert noa_agenda._idea_dict.get(summer_hike_road) != None
    assert noa_agenda._idea_dict.get(sports_swim_road) is None
    assert noa_agenda._idea_dict.get(sports_hike_road) is None


def test_AgendaUnit_add_idea_bundling_SetsNewParentWithWeightEqualToSumOfAdoptedIdeas():
    noa_agenda = agendaunit_shop("Noa")
    sports_text = "sports"
    sports_road = noa_agenda.make_l1_road(sports_text)
    noa_agenda.add_l1_idea(ideaunit_shop(sports_text, _weight=2))
    swim_text = "swim"
    swim_weight = 3
    noa_agenda.add_idea(ideaunit_shop(swim_text, _weight=swim_weight), sports_road)
    hike_text = "hike"
    hike_weight = 5
    noa_agenda.add_idea(ideaunit_shop(hike_text, _weight=hike_weight), sports_road)
    bball_text = "bball"
    bball_weight = 7
    noa_agenda.add_idea(ideaunit_shop(bball_text, _weight=bball_weight), sports_road)

    noa_agenda.calc_agenda_metrics()
    sports_swim_road = noa_agenda.make_road(sports_road, swim_text)
    sports_hike_road = noa_agenda.make_road(sports_road, hike_text)
    sports_bball_road = noa_agenda.make_road(sports_road, bball_text)
    assert noa_agenda._idea_dict.get(sports_swim_road)._weight == swim_weight
    assert noa_agenda._idea_dict.get(sports_hike_road)._weight == hike_weight
    assert noa_agenda._idea_dict.get(sports_bball_road)._weight == bball_weight
    summer_text = "summer"
    summer_road = noa_agenda.make_road(sports_road, summer_text)
    summer_swim_road = noa_agenda.make_road(summer_road, swim_text)
    summer_hike_road = noa_agenda.make_road(summer_road, hike_text)
    summer_bball_road = noa_agenda.make_road(summer_road, bball_text)
    assert noa_agenda._idea_dict.get(summer_swim_road) is None
    assert noa_agenda._idea_dict.get(summer_hike_road) is None
    assert noa_agenda._idea_dict.get(summer_bball_road) is None

    # WHEN / THEN
    noa_agenda.add_idea(
        idea_kid=ideaunit_shop(summer_text),
        parent_road=sports_road,
        adoptees=[swim_text, hike_text],
        bundling=True,
    )

    # THEN
    noa_agenda.calc_agenda_metrics()
    assert noa_agenda._idea_dict.get(summer_road)._weight == swim_weight + hike_weight
    assert noa_agenda._idea_dict.get(summer_swim_road)._weight == swim_weight
    assert noa_agenda._idea_dict.get(summer_hike_road)._weight == hike_weight
    assert noa_agenda._idea_dict.get(summer_bball_road) is None
    assert noa_agenda._idea_dict.get(sports_swim_road) is None
    assert noa_agenda._idea_dict.get(sports_hike_road) is None
    assert noa_agenda._idea_dict.get(sports_bball_road) != None


def test_AgendaUnit_del_idea_obj_DeletingBundledIdeaReturnsIdeasToOriginalState():
    noa_agenda = agendaunit_shop("Noa")
    sports_text = "sports"
    sports_road = noa_agenda.make_l1_road(sports_text)
    noa_agenda.add_l1_idea(ideaunit_shop(sports_text, _weight=2))
    swim_text = "swim"
    swim_weight = 3
    noa_agenda.add_idea(
        ideaunit_shop(swim_text, _weight=swim_weight), parent_road=sports_road
    )
    hike_text = "hike"
    hike_weight = 5
    noa_agenda.add_idea(
        ideaunit_shop(hike_text, _weight=hike_weight), parent_road=sports_road
    )
    bball_text = "bball"
    bball_weight = 7
    noa_agenda.add_idea(
        ideaunit_shop(bball_text, _weight=bball_weight), parent_road=sports_road
    )

    noa_agenda.calc_agenda_metrics()
    sports_swim_road = noa_agenda.make_road(sports_road, swim_text)
    sports_hike_road = noa_agenda.make_road(sports_road, hike_text)
    sports_bball_road = noa_agenda.make_road(sports_road, bball_text)
    assert noa_agenda._idea_dict.get(sports_swim_road)._weight == swim_weight
    assert noa_agenda._idea_dict.get(sports_hike_road)._weight == hike_weight
    assert noa_agenda._idea_dict.get(sports_bball_road)._weight == bball_weight
    summer_text = "summer"
    summer_road = noa_agenda.make_road(sports_road, summer_text)
    summer_swim_road = noa_agenda.make_road(summer_road, swim_text)
    summer_hike_road = noa_agenda.make_road(summer_road, hike_text)
    summer_bball_road = noa_agenda.make_road(summer_road, bball_text)
    assert noa_agenda._idea_dict.get(summer_swim_road) is None
    assert noa_agenda._idea_dict.get(summer_hike_road) is None
    assert noa_agenda._idea_dict.get(summer_bball_road) is None
    noa_agenda.add_idea(
        idea_kid=ideaunit_shop(summer_text),
        parent_road=sports_road,
        adoptees=[swim_text, hike_text],
        bundling=True,
    )
    noa_agenda.calc_agenda_metrics()
    assert noa_agenda._idea_dict.get(summer_road)._weight == swim_weight + hike_weight
    assert noa_agenda._idea_dict.get(summer_swim_road)._weight == swim_weight
    assert noa_agenda._idea_dict.get(summer_hike_road)._weight == hike_weight
    assert noa_agenda._idea_dict.get(summer_bball_road) is None
    assert noa_agenda._idea_dict.get(sports_swim_road) is None
    assert noa_agenda._idea_dict.get(sports_hike_road) is None
    assert noa_agenda._idea_dict.get(sports_bball_road) != None
    print(f"{noa_agenda._idea_dict.keys()=}")

    # WHEN
    noa_agenda.del_idea_obj(road=summer_road, del_children=False)

    # THEN
    noa_agenda.calc_agenda_metrics()
    print(f"{noa_agenda._idea_dict.keys()=}")
    assert noa_agenda._idea_dict.get(sports_swim_road)._weight == swim_weight
    assert noa_agenda._idea_dict.get(sports_hike_road)._weight == hike_weight
    assert noa_agenda._idea_dict.get(sports_bball_road)._weight == bball_weight
