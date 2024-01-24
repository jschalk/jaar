from src.agenda.examples.example_agendas import get_agenda_with_4_levels
from src.agenda.idea import ideaunit_shop
from src.agenda.reason_idea import reasonunit_shop, beliefunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.group import balancelink_shop
from pytest import raises as pytest_raises
from src._prime.road import default_road_delimiter_if_none


def test_agenda_add_idea_RaisesErrorWhen_parent_road_IsInvalid():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    invalid_rootnode_swim_road = "swimming"
    assert invalid_rootnode_swim_road != yue_agenda._economy_id
    work_text = "work"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yue_agenda.add_idea(
            ideaunit_shop(work_text), parent_road=invalid_rootnode_swim_road
        )
    assert (
        str(excinfo.value)
        == f"add_idea failed because parent_road '{invalid_rootnode_swim_road}' has an invalid root node"
    )


def test_agenda_add_idea_RaisesErrorWhen_parent_road_IdeaDoesNotExist():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    swim_road = yue_agenda.make_l1_road("swimming")
    work_text = "work"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yue_agenda.add_idea(
            ideaunit_shop(work_text),
            parent_road=swim_road,
            create_missing_ancestors=False,
        )
    assert (
        str(excinfo.value)
        == f"add_idea failed because '{swim_road}' idea does not exist."
    )


def test_agenda_add_l1_idea_CorrectlySetsAttr():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    work_text = "work"
    work_road = yue_agenda.make_l1_road(work_text)
    assert yue_agenda.idea_exists(work_road) == False

    # WHEN
    yue_agenda.add_l1_idea(ideaunit_shop(work_text))

    # THEN
    assert yue_agenda.idea_exists(work_road)


def test_agenda_idea_kid_CanHaveKids():
    # GIVEN / WHEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.set_agenda_metrics()

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


def test_agenda_add_idea_CanAddKidTo_idearoot():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.set_agenda_metrics()

    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=1) == 4

    new_idea_parent_road = sue_agenda._economy_id

    # WHEN
    sue_agenda.add_idea(ideaunit_shop("new_idea"), parent_road=new_idea_parent_road)
    sue_agenda.set_agenda_metrics()

    # THEN
    print(f"{(sue_agenda._agent_id == new_idea_parent_road[0])=}")
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_agenda.get_idea_count() == 18
    assert sue_agenda.get_level_count(level=1) == 5


def test_agenda_add_idea_CanAddKidToKidIdea():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.set_agenda_metrics()
    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=2) == 10

    # WHEN
    new_idea_parent_road = sue_agenda.make_l1_road("work")
    sue_agenda.add_idea(ideaunit_shop("new_york"), parent_road=new_idea_parent_road)
    sue_agenda.set_agenda_metrics()

    # THEN
    # print(f"{(sue_agenda._agent_id == new_idea_parent_road[0])=}")
    # print(sue_agenda._idearoot._kids["work"])
    # print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_agenda.get_idea_count() == 18
    assert sue_agenda.get_level_count(level=2) == 11
    new_york_idea = sue_agenda._idearoot._kids["work"]._kids["new_york"]
    assert new_york_idea._parent_road == sue_agenda.make_l1_road("work")
    assert new_york_idea._road_delimiter == sue_agenda._road_delimiter
    new_york_idea.set_parent_road(parent_road="testing")
    assert (
        sue_agenda._idearoot._kids["work"]._kids["new_york"]._parent_road == "testing"
    )
    assert sue_agenda.get_intent_dict()


def test_agenda_add_idea_CanAddKidToGrandkidIdea():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.set_agenda_metrics()

    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=3) == 2
    wkday_road = sue_agenda.make_l1_road("weekdays")
    new_idea_parent_road = sue_agenda.make_road(wkday_road, "Wednesday")

    # WHEN
    sue_agenda.add_idea(ideaunit_shop("new_idea"), parent_road=new_idea_parent_road)
    sue_agenda.set_agenda_metrics()

    # THEN
    print(f"{(sue_agenda._agent_id == new_idea_parent_road[0])=}")
    print(sue_agenda._idearoot._kids["work"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_agenda.get_idea_count() == 18
    assert sue_agenda.get_level_count(level=3) == 3


def test_agenda_add_idea_CorrectlyAddsIdeaObjWithNonstandard_delimiter():
    # GIVEN
    slash_text = "/"
    assert slash_text != default_road_delimiter_if_none()
    bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_text)
    work_text = "work"
    week_text = "week"
    wed_text = "Wednesday"
    work_road = bob_agenda.make_l1_road(work_text)
    week_road = bob_agenda.make_l1_road(week_text)
    wed_road = bob_agenda.make_road(week_road, wed_text)
    bob_agenda.add_l1_idea(ideaunit_shop(work_text))
    bob_agenda.add_l1_idea(ideaunit_shop(week_text))
    bob_agenda.add_idea(ideaunit_shop(wed_text), week_road)
    print(f"{bob_agenda._idearoot._kids.keys()=}")
    assert len(bob_agenda._idearoot._kids) == 2
    wed_idea = bob_agenda.get_idea_obj(wed_road)
    assert wed_idea._road_delimiter == slash_text
    assert wed_idea._road_delimiter == bob_agenda._road_delimiter

    # WHEN
    bob_agenda.edit_idea_attr(
        road=work_road, reason_base=week_road, reason_premise=wed_road
    )

    # THEN
    work_idea = bob_agenda.get_idea_obj(work_road)
    assert work_idea._reasonunits.get(week_road) != None


def test_agenda_add_idea_CanCreateRoadUnitToGrandkidIdea():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.set_agenda_metrics()

    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=3) == 2
    ww2_road = sue_agenda.make_l1_road("ww2")
    battles_road = sue_agenda.make_road(ww2_road, "battles")
    new_idea_parent_road = sue_agenda.make_road(battles_road, "coralsea")
    new_idea = ideaunit_shop(_label="USS Saratoga")

    # WHEN
    sue_agenda.add_idea(new_idea, parent_road=new_idea_parent_road)
    sue_agenda.set_agenda_metrics()

    # THEN
    print(sue_agenda._idearoot._kids["ww2"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_agenda._idearoot._kids["ww2"]._label == "ww2"
    assert sue_agenda._idearoot._kids["ww2"]._kids["battles"]._label == "battles"
    assert sue_agenda.get_idea_count() == 21
    assert sue_agenda.get_level_count(level=3) == 3


def test_agenda_add_idea_creates_reasons_ideas():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.set_agenda_metrics()

    assert sue_agenda.get_idea_count() == 17
    assert sue_agenda.get_level_count(level=3) == 2
    work_road = sue_agenda.make_l1_road("work")
    new_idea_parent_road = sue_agenda.make_road(work_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(clean_cookery_text, _weight=40, promise=True)

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
        create_missing_ideas_groups=True,
    )
    sue_agenda.set_agenda_metrics()

    # THEN
    print(f"{(len(new_idea_parent_road) == 1)=}")
    # for idea_kid in sue_agenda._idearoot._kids.values():
    #     print(f"{idea_kid._label=}")
    assert sue_agenda._idearoot.get_kid(buildings_text) != None
    assert sue_agenda.get_idea_obj(road=buildings_road) != None
    assert sue_agenda.get_idea_obj(road=cookery_dirty_road) != None
    assert sue_agenda.get_idea_count() == 22
    assert sue_agenda.get_level_count(level=3) == 4


def test_agenda_add_idea_CorrectlySets_agenda_economy_id():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    agenda_economy_id = "Texas"
    sue_agenda.set_economy_id(economy_id=agenda_economy_id)
    sue_agenda.set_agenda_metrics()
    assert sue_agenda._economy_id == agenda_economy_id

    work_road = sue_agenda.make_l1_road("work")
    clean_road = sue_agenda.make_road(work_road, "cleaning")
    cookery_text = "cookery ready to use"
    cookery_road = sue_agenda.make_road(clean_road, cookery_text)

    # WHEN
    sue_agenda.add_idea(ideaunit_shop(cookery_text), clean_road)

    # THEN
    cookery_idea = sue_agenda.get_idea_obj(cookery_road)
    assert cookery_idea._agenda_economy_id == agenda_economy_id


def test_agenda_del_idea_kid_Level0CannotBeDeleted():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    root_road = sue_agenda._economy_id

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.del_idea_kid(road=root_road)
    assert str(excinfo.value) == "Idearoot cannot be deleted"


def test_agenda_del_idea_kid_Level1CanBeDeleted_ChildrenDeleted():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = sue_agenda.make_road(week_road, sun_text)
    assert sue_agenda.get_idea_obj(road=week_road)
    assert sue_agenda.get_idea_obj(road=sun_road)

    # WHEN
    sue_agenda.del_idea_kid(road=week_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=week_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{week_road}'"
    new_sunday_road = sue_agenda.make_l1_road("Sunday")
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=new_sunday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{new_sunday_road}'"


def test_agenda_del_idea_kid_Level1CanBeDeleted_ChildrenInherited():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_agenda.set_agenda_metrics()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    old_sunday_road = sue_agenda.make_road(week_road, sun_text)
    assert sue_agenda.get_idea_obj(road=old_sunday_road)

    # WHEN
    sue_agenda.del_idea_kid(road=week_road, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=old_sunday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{old_sunday_road}'"
    new_sunday_road = sue_agenda.make_l1_road(sun_text)
    assert sue_agenda.get_idea_obj(road=new_sunday_road)
    new_sunday_idea = sue_agenda.get_idea_obj(road=new_sunday_road)
    assert new_sunday_idea._parent_road == sue_agenda._economy_id


def test_agenda_del_idea_kid_LevelNCanBeDeleted_ChildrenInherited():
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
    sue_agenda.set_agenda_metrics()
    assert sue_agenda._idea_dict.get(usa_road) != None
    assert sue_agenda._idea_dict.get(usa_texas_road) != None
    assert sue_agenda._idea_dict.get(usa_oregon_road) != None
    assert sue_agenda._idea_dict.get(states_texas_road) is None
    assert sue_agenda._idea_dict.get(states_oregon_road) is None

    # WHEN
    sue_agenda.del_idea_kid(road=usa_road, del_children=False)

    # THEN
    sue_agenda.set_agenda_metrics()
    assert sue_agenda._idea_dict.get(states_texas_road) != None
    assert sue_agenda._idea_dict.get(states_oregon_road) != None
    assert sue_agenda._idea_dict.get(usa_texas_road) is None
    assert sue_agenda._idea_dict.get(usa_oregon_road) is None
    assert sue_agenda._idea_dict.get(usa_road) is None


def test_agenda_del_idea_kid_Level2CanBeDeleted_ChildrenDeleted():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    wkday_road = sue_agenda.make_l1_road("weekdays")
    monday_road = sue_agenda.make_road(wkday_road, "Monday")
    assert sue_agenda.get_idea_obj(road=monday_road)

    # WHEN
    sue_agenda.del_idea_kid(road=monday_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=monday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{monday_road}'"


def test_agenda_del_idea_kid_LevelNCanBeDeleted_ChildrenDeleted():
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
    sue_agenda.del_idea_kid(road=usa_texas_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_obj(road=usa_texas_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{usa_texas_road}'"


def test_agenda_edit_idea_attr_IsAbleToEditAnyAncestor_Idea():
    sue_agenda = get_agenda_with_4_levels()
    work_text = "work"
    work_road = sue_agenda.make_l1_road(work_text)
    print(f"{work_road=}")
    current_weight = sue_agenda._idearoot._kids[work_text]._weight
    assert current_weight == 30
    sue_agenda.edit_idea_attr(road=work_road, weight=23)
    new_weight = sue_agenda._idearoot._kids[work_text]._weight
    assert new_weight == 23

    # uid: int = None,
    sue_agenda._idearoot._kids[work_text]._uid = 34
    uid_curr = sue_agenda._idearoot._kids[work_text]._uid
    assert uid_curr == 34
    sue_agenda.edit_idea_attr(road=work_road, uid=23)
    uid_new = sue_agenda._idearoot._kids[work_text]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    sue_agenda._idearoot._kids[work_text]._begin = 39
    begin_curr = sue_agenda._idearoot._kids[work_text]._begin
    assert begin_curr == 39
    sue_agenda._idearoot._kids[work_text]._close = 43
    close_curr = sue_agenda._idearoot._kids[work_text]._close
    assert close_curr == 43
    sue_agenda.edit_idea_attr(road=work_road, begin=25, close=29)
    assert sue_agenda._idearoot._kids[work_text]._begin == 25
    assert sue_agenda._idearoot._kids[work_text]._close == 29

    # beliefunit: beliefunit_shop = None,
    # sue_agenda._idearoot._kids[work_text]._beliefunits = None
    assert sue_agenda._idearoot._kids[work_text]._beliefunits == {}
    wkdays_road = sue_agenda.make_l1_road("weekdays")
    belief_road = sue_agenda.make_road(wkdays_road, "Sunday")
    beliefunit_x = beliefunit_shop(base=belief_road, pick=belief_road)

    work_beliefunits = sue_agenda._idearoot._kids[work_text]._beliefunits
    print(f"{work_beliefunits=}")
    sue_agenda.edit_idea_attr(road=work_road, beliefunit=beliefunit_x)
    work_beliefunits = sue_agenda._idearoot._kids[work_text]._beliefunits
    print(f"{work_beliefunits=}")
    assert sue_agenda._idearoot._kids[work_text]._beliefunits == {
        beliefunit_x.base: beliefunit_x
    }

    # _descendant_promise_count: int = None,
    sue_agenda._idearoot._kids[work_text]._descendant_promise_count = 81
    _descendant_promise_count_curr = sue_agenda._idearoot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_curr == 81
    sue_agenda.edit_idea_attr(road=work_road, descendant_promise_count=67)
    _descendant_promise_count_new = sue_agenda._idearoot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_new == 67

    # _all_party_credit: bool = None,
    sue_agenda._idearoot._kids[work_text]._all_party_credit = 74
    _all_party_credit_curr = sue_agenda._idearoot._kids[work_text]._all_party_credit
    assert _all_party_credit_curr == 74
    sue_agenda.edit_idea_attr(road=work_road, all_party_credit=59)
    _all_party_credit_new = sue_agenda._idearoot._kids[work_text]._all_party_credit
    assert _all_party_credit_new == 59

    # _all_party_debt: bool = None,
    sue_agenda._idearoot._kids[work_text]._all_party_debt = 74
    _all_party_debt_curr = sue_agenda._idearoot._kids[work_text]._all_party_debt
    assert _all_party_debt_curr == 74
    sue_agenda.edit_idea_attr(road=work_road, all_party_debt=59)
    _all_party_debt_new = sue_agenda._idearoot._kids[work_text]._all_party_debt
    assert _all_party_debt_new == 59

    # _balancelink: dict = None,
    sue_agenda._idearoot._kids[work_text]._balancelinks = {
        "fun": balancelink_shop(brand="fun", creditor_weight=1, debtor_weight=7)
    }
    _balancelinks = sue_agenda._idearoot._kids[work_text]._balancelinks
    assert _balancelinks == {
        "fun": balancelink_shop(brand="fun", creditor_weight=1, debtor_weight=7)
    }
    sue_agenda.edit_idea_attr(
        road=work_road,
        balancelink=balancelink_shop(brand="fun", creditor_weight=4, debtor_weight=8),
    )
    assert sue_agenda._idearoot._kids[work_text]._balancelinks == {
        "fun": balancelink_shop(brand="fun", creditor_weight=4, debtor_weight=8)
    }

    # _is_expanded: dict = None,
    sue_agenda._idearoot._kids[work_text]._is_expanded = "what"
    _is_expanded = sue_agenda._idearoot._kids[work_text]._is_expanded
    assert _is_expanded == "what"
    sue_agenda.edit_idea_attr(road=work_road, is_expanded=True)
    assert sue_agenda._idearoot._kids[work_text]._is_expanded == True

    # promise: dict = None,
    sue_agenda._idearoot._kids[work_text].promise = "funfun3"
    action = sue_agenda._idearoot._kids[work_text].promise
    assert action == "funfun3"
    sue_agenda.edit_idea_attr(road=work_road, promise=True)
    assert sue_agenda._idearoot._kids[work_text].promise == True

    # _range_source_road: dict = None,
    sue_agenda._idearoot._kids[work_text]._range_source_road = "fun3rol"
    range_source_road = sue_agenda._idearoot._kids[work_text]._range_source_road
    assert range_source_road == "fun3rol"
    end_road = sue_agenda.make_road(work_road, "end")
    sue_agenda.edit_idea_attr(road=work_road, range_source_road=end_road)
    assert sue_agenda._idearoot._kids[work_text]._range_source_road == end_road

    print(f"{work_road=} {end_road=}")


def test_agenda_edit_idea_attr_agendaIsAbleToEdit_meld_strategy_AnyIdeaIfInvaildThrowsError():
    sue_agenda = get_agenda_with_4_levels()
    work_road = sue_agenda.make_l1_road("work")

    # WHEN / THEN
    ineligible_meld_strategy = "yahoo9"
    with pytest_raises(Exception) as excinfo:
        sue_agenda.edit_idea_attr(work_road, meld_strategy=ineligible_meld_strategy)
    assert (
        str(excinfo.value)
        == f"'{ineligible_meld_strategy}' is ineligible meld_strategy."
    )


def test_agenda_edit_idea_attr_agendaIsAbleToEditDenomAnyIdeaIfInvaildDenomThrowsError():
    yao_agenda = agendaunit_shop("Yao")
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_idea_attr(road="", denom=46)
    assert str(excinfo.value) == "Root Idea cannot have numor denom reest."

    work_text = "work"
    work_road = yao_agenda.make_l1_road(work_text)
    work_idea = ideaunit_shop(work_text)
    yao_agenda.add_l1_idea(work_idea)
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    clean_road = yao_agenda.make_road(work_road, clean_text)
    yao_agenda.add_idea(clean_idea, parent_road=work_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_idea_attr(road=clean_road, denom=46)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{clean_road}' if parent '{work_road}' or ideaunit._numeric_road does not have begin/close range"
    )

    # GIVEN
    yao_agenda.edit_idea_attr(road=work_road, begin=44, close=110)
    yao_agenda.edit_idea_attr(road=clean_road, denom=11)
    clean_idea = yao_agenda.get_idea_obj(road=clean_road)
    assert clean_idea._begin == 4
    assert clean_idea._close == 10


def test_agenda_edit_idea_attr_agendaIsAbleToEditDenomAnyIdeaInvaildDenomThrowsError():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    work = "work"
    w_road = yao_agenda.make_l1_road(work)
    work_idea = ideaunit_shop(work, _begin=8, _close=14)
    yao_agenda.add_l1_idea(work_idea)

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


def test_agenda_edit_idea_attr_agendaWhenParentAndNumeric_roadBothHaveRangeThrowError():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    work_text = "work"
    work_road = yao_agenda.make_l1_road(work_text)
    yao_agenda.add_l1_idea(ideaunit_shop(work_text))
    day_text = "day_range"
    day_idea = ideaunit_shop(day_text, _begin=44, _close=110)
    day_road = yao_agenda.make_l1_road(day_text)
    yao_agenda.add_l1_idea(day_idea)

    work_idea = yao_agenda.get_idea_obj(road=work_road)
    assert work_idea._begin is None
    assert work_idea._close is None

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_idea_attr(road=work_road, denom=11)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{work_road}' if parent '{yao_agenda._economy_id}' or ideaunit._numeric_road does not have begin/close range"
    )

    # WHEN
    yao_agenda.edit_idea_attr(road=work_road, numeric_road=day_road)

    # THEN
    work_idea3 = yao_agenda.get_idea_obj(road=work_road)
    assert work_idea3._addin is None
    assert work_idea3._numor is None
    assert work_idea3._denom is None
    assert work_idea3._reest is None
    assert work_idea3._begin == 44
    assert work_idea3._close == 110
    yao_agenda.edit_idea_attr(road=work_road, denom=11, numeric_road=day_road)
    assert work_idea3._begin == 4
    assert work_idea3._close == 10
    assert work_idea3._numor == 1
    assert work_idea3._denom == 11
    assert work_idea3._reest == False
    assert work_idea3._addin == 0


def test_agenda_add_idea_MustReorderKidsDictToBeAlphabetical():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    work_text = "work"
    noa_agenda.add_l1_idea(ideaunit_shop(work_text))
    swim_text = "swim"
    noa_agenda.add_l1_idea(ideaunit_shop(swim_text))

    # WHEN
    idea_list = list(noa_agenda._idearoot._kids.values())

    # THEN
    assert idea_list[0]._label == swim_text


def test_agenda_add_idea_adoptee_RaisesErrorIfAdopteeIdeaDoesNotHaveCorrectParent():
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


def test_agenda_add_idea_adoptee_CorrectlyAddsAdoptee():
    noa_agenda = agendaunit_shop("Noa")
    sports_text = "sports"
    sports_road = noa_agenda.make_l1_road(sports_text)
    noa_agenda.add_l1_idea(ideaunit_shop(sports_text))
    swim_text = "swim"
    noa_agenda.add_idea(ideaunit_shop(swim_text), parent_road=sports_road)
    hike_text = "hike"
    noa_agenda.add_idea(ideaunit_shop(hike_text), parent_road=sports_road)

    noa_agenda.set_agenda_metrics()
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
    noa_agenda.set_agenda_metrics()
    assert noa_agenda._idea_dict.get(summer_swim_road) != None
    assert noa_agenda._idea_dict.get(summer_hike_road) != None
    assert noa_agenda._idea_dict.get(sports_swim_road) is None
    assert noa_agenda._idea_dict.get(sports_hike_road) is None


def test_agenda_add_idea_bundling_SetsNewParentWithWeightEqualToSumOfAdoptedIdeas():
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

    noa_agenda.set_agenda_metrics()
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
    noa_agenda.set_agenda_metrics()
    assert noa_agenda._idea_dict.get(summer_road)._weight == swim_weight + hike_weight
    assert noa_agenda._idea_dict.get(summer_swim_road)._weight == swim_weight
    assert noa_agenda._idea_dict.get(summer_hike_road)._weight == hike_weight
    assert noa_agenda._idea_dict.get(summer_bball_road) is None
    assert noa_agenda._idea_dict.get(sports_swim_road) is None
    assert noa_agenda._idea_dict.get(sports_hike_road) is None
    assert noa_agenda._idea_dict.get(sports_bball_road) != None


def test_agenda_del_idea_kid_DeletingBundledIdeaReturnsIdeasToOriginalState():
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

    noa_agenda.set_agenda_metrics()
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
    noa_agenda.set_agenda_metrics()
    assert noa_agenda._idea_dict.get(summer_road)._weight == swim_weight + hike_weight
    assert noa_agenda._idea_dict.get(summer_swim_road)._weight == swim_weight
    assert noa_agenda._idea_dict.get(summer_hike_road)._weight == hike_weight
    assert noa_agenda._idea_dict.get(summer_bball_road) is None
    assert noa_agenda._idea_dict.get(sports_swim_road) is None
    assert noa_agenda._idea_dict.get(sports_hike_road) is None
    assert noa_agenda._idea_dict.get(sports_bball_road) != None
    print(f"{noa_agenda._idea_dict.keys()=}")

    # WHEN
    noa_agenda.del_idea_kid(road=summer_road, del_children=False)

    # THEN
    noa_agenda.set_agenda_metrics()
    print(f"{noa_agenda._idea_dict.keys()=}")
    assert noa_agenda._idea_dict.get(sports_swim_road)._weight == swim_weight
    assert noa_agenda._idea_dict.get(sports_hike_road)._weight == hike_weight
    assert noa_agenda._idea_dict.get(sports_bball_road)._weight == bball_weight
