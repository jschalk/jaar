from src._world.healer import healerhold_shop
from src._world.examples.example_worlds import get_world_with_4_levels
from src._world.idea import ideaunit_shop
from src._world.reason_idea import reasonunit_shop, factunit_shop
from src._world.world import worldunit_shop
from src._world.lobbybox import awardlink_shop
from pytest import raises as pytest_raises
from src._road.road import default_road_delimiter_if_none


def test_WorldUnit_add_idea_RaisesErrorWhen_parent_road_IsInvalid():
    # GIVEN
    zia_world = worldunit_shop("Zia")
    invalid_rootnode_swim_road = "swimming"
    assert invalid_rootnode_swim_road != zia_world._real_id
    casa_text = "casa"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_world.add_idea(
            ideaunit_shop(casa_text), parent_road=invalid_rootnode_swim_road
        )
    assert (
        str(excinfo.value)
        == f"add_idea failed because parent_road '{invalid_rootnode_swim_road}' has an invalid root node"
    )


def test_WorldUnit_add_idea_RaisesErrorWhen_parent_road_IdeaDoesNotExist():
    # GIVEN
    zia_world = worldunit_shop("Zia")
    swim_road = zia_world.make_l1_road("swimming")
    casa_text = "casa"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_world.add_idea(
            ideaunit_shop(casa_text),
            parent_road=swim_road,
            create_missing_ancestors=False,
        )
    assert (
        str(excinfo.value)
        == f"add_idea failed because '{swim_road}' idea does not exist."
    )


def test_WorldUnit_add_idea_RaisesErrorWhen_label_IsNotNode():
    # GIVEN
    zia_world = worldunit_shop("Zia")
    swim_road = zia_world.make_l1_road("swimming")
    casa_text = "casa"
    casa_road = zia_world.make_l1_road(casa_text)
    run_text = "run"
    run_road = zia_world.make_road(casa_road, run_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_world.add_idea(ideaunit_shop(run_road), parent_road=swim_road)
    assert (
        str(excinfo.value) == f"add_idea failed because '{run_road}' is not a RoadNode."
    )


def test_WorldUnit_add_l1_idea_CorrectlySetsAttr():
    # GIVEN
    zia_world = worldunit_shop("Zia")
    casa_text = "casa"
    casa_road = zia_world.make_l1_road(casa_text)
    assert zia_world.idea_exists(casa_road) is False

    # WHEN
    zia_world.add_l1_idea(ideaunit_shop(casa_text))

    # THEN
    assert zia_world.idea_exists(casa_road)


def test_WorldUnit_IdeaUnit_kids_CanHaveKids():
    # GIVEN / WHEN
    sue_world = get_world_with_4_levels()
    sue_world.calc_world_metrics()

    # THEN
    assert sue_world._weight == 10
    assert sue_world._idearoot._kids
    print(f"{len(sue_world._idearoot._kids)=} {sue_world._idearoot._parent_road=}")
    assert sue_world.get_level_count(level=0) == 1
    weekdays_kids = sue_world._idearoot._kids["weekdays"]._kids
    weekdays_len = len(weekdays_kids)
    print(f"{weekdays_len=} {sue_world._idearoot._parent_road=}")
    # for idea in weekdays_kids.values():
    #     print(f"{idea._label=}")
    assert sue_world.get_idea_count() == 17
    assert sue_world.get_level_count(level=1) == 4
    assert sue_world.get_level_count(level=2) == 10
    assert sue_world.get_level_count(level=3) == 2


def test_WorldUnit_add_idea_CanAddKidTo_idearoot():
    # GIVEN
    sue_world = get_world_with_4_levels()
    sue_world.calc_world_metrics()

    assert sue_world.get_idea_count() == 17
    assert sue_world.get_level_count(level=1) == 4

    new_idea_parent_road = sue_world._real_id

    # WHEN
    sue_world.add_idea(ideaunit_shop("new_idea"), parent_road=new_idea_parent_road)
    sue_world.calc_world_metrics()

    # THEN
    print(f"{(sue_world._owner_id == new_idea_parent_road[0])=}")
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_world.get_idea_count() == 18
    assert sue_world.get_level_count(level=1) == 5


def test_WorldUnit_add_idea_CanAddKidToKidIdea():
    # GIVEN
    sue_world = get_world_with_4_levels()
    sue_world.calc_world_metrics()
    assert sue_world.get_idea_count() == 17
    assert sue_world.get_level_count(level=2) == 10

    # WHEN
    new_idea_parent_road = sue_world.make_l1_road("casa")
    sue_world.add_idea(ideaunit_shop("new_york"), parent_road=new_idea_parent_road)
    sue_world.calc_world_metrics()

    # THEN
    # print(f"{(sue_world._owner_id == new_idea_parent_road[0])=}")
    # print(sue_world._idearoot._kids["casa"])
    # print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_world.get_idea_count() == 18
    assert sue_world.get_level_count(level=2) == 11
    new_york_idea = sue_world._idearoot._kids["casa"]._kids["new_york"]
    assert new_york_idea._parent_road == sue_world.make_l1_road("casa")
    assert new_york_idea._road_delimiter == sue_world._road_delimiter
    new_york_idea.set_parent_road(parent_road="testing")
    assert sue_world._idearoot._kids["casa"]._kids["new_york"]._parent_road == "testing"
    assert sue_world.get_agenda_dict()


def test_WorldUnit_add_idea_CanAddKidToGrandkidIdea():
    # GIVEN
    sue_world = get_world_with_4_levels()
    sue_world.calc_world_metrics()

    assert sue_world.get_idea_count() == 17
    assert sue_world.get_level_count(level=3) == 2
    wkday_road = sue_world.make_l1_road("weekdays")
    new_idea_parent_road = sue_world.make_road(wkday_road, "Wednesday")

    # WHEN
    sue_world.add_idea(ideaunit_shop("new_idea"), parent_road=new_idea_parent_road)
    sue_world.calc_world_metrics()

    # THEN
    print(f"{(sue_world._owner_id == new_idea_parent_road[0])=}")
    print(sue_world._idearoot._kids["casa"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_world.get_idea_count() == 18
    assert sue_world.get_level_count(level=3) == 3


def test_WorldUnit_add_idea_CorrectlyAddsIdeaObjWithNonstandard_delimiter():
    # GIVEN
    slash_text = "/"
    assert slash_text != default_road_delimiter_if_none()
    bob_world = worldunit_shop("Bob", _road_delimiter=slash_text)
    casa_text = "casa"
    week_text = "week"
    wed_text = "Wednesday"
    casa_road = bob_world.make_l1_road(casa_text)
    week_road = bob_world.make_l1_road(week_text)
    wed_road = bob_world.make_road(week_road, wed_text)
    bob_world.add_l1_idea(ideaunit_shop(casa_text))
    bob_world.add_l1_idea(ideaunit_shop(week_text))
    bob_world.add_idea(ideaunit_shop(wed_text), week_road)
    print(f"{bob_world._idearoot._kids.keys()=}")
    assert len(bob_world._idearoot._kids) == 2
    wed_idea = bob_world.get_idea_obj(wed_road)
    assert wed_idea._road_delimiter == slash_text
    assert wed_idea._road_delimiter == bob_world._road_delimiter

    # WHEN
    bob_world.edit_idea_attr(
        road=casa_road, reason_base=week_road, reason_premise=wed_road
    )

    # THEN
    casa_idea = bob_world.get_idea_obj(casa_road)
    assert casa_idea._reasonunits.get(week_road) != None


def test_WorldUnit_add_idea_CanCreateRoadUnitToGrandkidIdea():
    # GIVEN
    sue_world = get_world_with_4_levels()
    sue_world.calc_world_metrics()

    assert sue_world.get_idea_count() == 17
    assert sue_world.get_level_count(level=3) == 2
    ww2_road = sue_world.make_l1_road("ww2")
    battles_road = sue_world.make_road(ww2_road, "battles")
    new_idea_parent_road = sue_world.make_road(battles_road, "coralsea")
    new_idea = ideaunit_shop(_label="USS Saratoga")

    # WHEN
    sue_world.add_idea(new_idea, parent_road=new_idea_parent_road)
    sue_world.calc_world_metrics()

    # THEN
    print(sue_world._idearoot._kids["ww2"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_world._idearoot._kids["ww2"]._label == "ww2"
    assert sue_world._idearoot._kids["ww2"]._kids["battles"]._label == "battles"
    assert sue_world.get_idea_count() == 21
    assert sue_world.get_level_count(level=3) == 3


def test_WorldUnit_add_idea_CreatesIdeaUnitsUsedBy_reasonunits():
    # GIVEN
    sue_world = get_world_with_4_levels()
    sue_world.calc_world_metrics()

    assert sue_world.get_idea_count() == 17
    assert sue_world.get_level_count(level=3) == 2
    casa_road = sue_world.make_l1_road("casa")
    new_idea_parent_road = sue_world.make_road(casa_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(clean_cookery_text, _weight=40, pledge=True)

    buildings_text = "buildings"
    buildings_road = sue_world.make_l1_road(buildings_text)
    cookery_room_text = "cookery"
    cookery_room_road = sue_world.make_road(buildings_road, cookery_room_text)
    cookery_dirty_text = "dirty"
    cookery_dirty_road = sue_world.make_road(cookery_room_road, cookery_dirty_text)
    reason_x = reasonunit_shop(base=cookery_room_road)
    reason_x.set_premise(premise=cookery_dirty_road)
    clean_cookery_idea.set_reasonunit(reason=reason_x)

    assert sue_world._idearoot.get_kid(buildings_text) is None

    # WHEN
    sue_world.add_idea(
        idea_kid=clean_cookery_idea,
        parent_road=new_idea_parent_road,
        create_missing_ideas=True,
    )
    sue_world.calc_world_metrics()

    # THEN
    print(f"{(len(new_idea_parent_road) == 1)=}")
    # for idea_kid in sue_world._idearoot._kids.values():
    #     print(f"{idea_kid._label=}")
    assert sue_world._idearoot.get_kid(buildings_text) != None
    assert sue_world.get_idea_obj(buildings_road) != None
    assert sue_world.get_idea_obj(cookery_dirty_road) != None
    assert sue_world.get_idea_count() == 22
    assert sue_world.get_level_count(level=3) == 4


def test_WorldUnit_add_idea_CorrectlySets_world_real_id_AND_coin():
    # GIVEN'
    x_coin = 500
    sue_world = get_world_with_4_levels()
    sue_world._coin = x_coin
    world_real_id = "Texas"
    sue_world.set_real_id(world_real_id)
    assert sue_world._real_id == world_real_id

    casa_road = sue_world.make_l1_road("casa")
    clean_road = sue_world.make_road(casa_road, "cleaning")
    cookery_text = "cookery ready to use"
    cookery_road = sue_world.make_road(clean_road, cookery_text)

    # WHEN
    sue_world.add_idea(ideaunit_shop(cookery_text), clean_road)

    # THEN
    cookery_idea = sue_world.get_idea_obj(cookery_road)
    assert cookery_idea._world_real_id == world_real_id
    assert cookery_idea._coin == x_coin


def test_WorldUnit_del_idea_obj_Level0CannotBeDeleted():
    # GIVEN
    sue_world = get_world_with_4_levels()
    root_road = sue_world._real_id

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_world.del_idea_obj(road=root_road)
    assert str(excinfo.value) == "Idearoot cannot be deleted"


def test_WorldUnit_del_idea_obj_Level1CanBeDeleted_ChildrenDeleted():
    # GIVEN
    sue_world = get_world_with_4_levels()
    week_text = "weekdays"
    week_road = sue_world.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = sue_world.make_road(week_road, sun_text)
    assert sue_world.get_idea_obj(week_road)
    assert sue_world.get_idea_obj(sun_road)

    # WHEN
    sue_world.del_idea_obj(road=week_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_world.get_idea_obj(week_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{week_road}'"
    new_sunday_road = sue_world.make_l1_road("Sunday")
    with pytest_raises(Exception) as excinfo:
        sue_world.get_idea_obj(new_sunday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{new_sunday_road}'"


def test_WorldUnit_del_idea_obj_Level1CanBeDeleted_ChildrenInherited():
    # GIVEN
    sue_world = get_world_with_4_levels()
    week_text = "weekdays"
    week_road = sue_world.make_l1_road(week_text)
    sun_text = "Sunday"
    old_sunday_road = sue_world.make_road(week_road, sun_text)
    assert sue_world.get_idea_obj(old_sunday_road)

    # WHEN
    sue_world.del_idea_obj(road=week_road, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_world.get_idea_obj(old_sunday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{old_sunday_road}'"
    new_sunday_road = sue_world.make_l1_road(sun_text)
    assert sue_world.get_idea_obj(new_sunday_road)
    new_sunday_idea = sue_world.get_idea_obj(new_sunday_road)
    assert new_sunday_idea._parent_road == sue_world._real_id


def test_WorldUnit_del_idea_obj_LevelNCanBeDeleted_ChildrenInherited():
    # GIVEN
    sue_world = get_world_with_4_levels()
    states_text = "nation-state"
    states_road = sue_world.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_world.make_road(states_road, usa_text)
    texas_text = "Texas"
    oregon_text = "Oregon"
    usa_texas_road = sue_world.make_road(usa_road, texas_text)
    usa_oregon_road = sue_world.make_road(usa_road, oregon_text)
    states_texas_road = sue_world.make_road(states_road, texas_text)
    states_oregon_road = sue_world.make_road(states_road, oregon_text)
    assert sue_world.idea_exists(usa_road)
    assert sue_world.idea_exists(usa_texas_road)
    assert sue_world.idea_exists(usa_oregon_road)
    assert sue_world.idea_exists(states_texas_road) is False
    assert sue_world.idea_exists(states_oregon_road) is False

    # WHEN
    sue_world.del_idea_obj(road=usa_road, del_children=False)

    # THEN
    assert sue_world.idea_exists(states_texas_road)
    assert sue_world.idea_exists(states_oregon_road)
    assert sue_world.idea_exists(usa_texas_road) is False
    assert sue_world.idea_exists(usa_oregon_road) is False
    assert sue_world.idea_exists(usa_road) is False


def test_WorldUnit_del_idea_obj_Level2CanBeDeleted_ChildrenDeleted():
    # GIVEN
    sue_world = get_world_with_4_levels()
    wkday_road = sue_world.make_l1_road("weekdays")
    monday_road = sue_world.make_road(wkday_road, "Monday")
    assert sue_world.get_idea_obj(monday_road)

    # WHEN
    sue_world.del_idea_obj(road=monday_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_world.get_idea_obj(monday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{monday_road}'"


def test_WorldUnit_del_idea_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # GIVEN
    sue_world = get_world_with_4_levels()
    states_text = "nation-state"
    states_road = sue_world.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_world.make_road(states_road, usa_text)
    texas_text = "Texas"
    usa_texas_road = sue_world.make_road(usa_road, texas_text)
    assert sue_world.get_idea_obj(usa_texas_road)

    # WHEN
    sue_world.del_idea_obj(road=usa_texas_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_world.get_idea_obj(usa_texas_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{usa_texas_road}'"


def test_WorldUnit_edit_idea_attr_IsAbleToEditAnyAncestor_Idea():
    sue_world = get_world_with_4_levels()
    casa_text = "casa"
    casa_road = sue_world.make_l1_road(casa_text)
    print(f"{casa_road=}")
    old_weight = sue_world._idearoot._kids[casa_text]._weight
    assert old_weight == 30
    sue_world.edit_idea_attr(road=casa_road, weight=23)
    new_weight = sue_world._idearoot._kids[casa_text]._weight
    assert new_weight == 23

    # uid: int = None,
    sue_world._idearoot._kids[casa_text]._uid = 34
    x_uid = sue_world._idearoot._kids[casa_text]._uid
    assert x_uid == 34
    sue_world.edit_idea_attr(road=casa_road, uid=23)
    uid_new = sue_world._idearoot._kids[casa_text]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    sue_world._idearoot._kids[casa_text]._begin = 39
    x_begin = sue_world._idearoot._kids[casa_text]._begin
    assert x_begin == 39
    sue_world._idearoot._kids[casa_text]._close = 43
    x_close = sue_world._idearoot._kids[casa_text]._close
    assert x_close == 43
    sue_world.edit_idea_attr(road=casa_road, begin=25, close=29)
    assert sue_world._idearoot._kids[casa_text]._begin == 25
    assert sue_world._idearoot._kids[casa_text]._close == 29

    # factunit: factunit_shop = None,
    # sue_world._idearoot._kids[casa_text]._factunits = None
    assert sue_world._idearoot._kids[casa_text]._factunits == {}
    wkdays_road = sue_world.make_l1_road("weekdays")
    fact_road = sue_world.make_road(wkdays_road, "Sunday")
    factunit_x = factunit_shop(base=fact_road, pick=fact_road)

    casa_factunits = sue_world._idearoot._kids[casa_text]._factunits
    print(f"{casa_factunits=}")
    sue_world.edit_idea_attr(road=casa_road, factunit=factunit_x)
    casa_factunits = sue_world._idearoot._kids[casa_text]._factunits
    print(f"{casa_factunits=}")
    assert sue_world._idearoot._kids[casa_text]._factunits == {
        factunit_x.base: factunit_x
    }

    # _descendant_pledge_count: int = None,
    sue_world._idearoot._kids[casa_text]._descendant_pledge_count = 81
    x_descendant_pledge_count = sue_world._idearoot._kids[
        casa_text
    ]._descendant_pledge_count
    assert x_descendant_pledge_count == 81
    sue_world.edit_idea_attr(road=casa_road, descendant_pledge_count=67)
    _descendant_pledge_count_new = sue_world._idearoot._kids[
        casa_text
    ]._descendant_pledge_count
    assert _descendant_pledge_count_new == 67

    # _all_char_cred: bool = None,
    sue_world._idearoot._kids[casa_text]._all_char_cred = 74
    x_all_char_cred = sue_world._idearoot._kids[casa_text]._all_char_cred
    assert x_all_char_cred == 74
    sue_world.edit_idea_attr(road=casa_road, all_char_cred=59)
    _all_char_cred_new = sue_world._idearoot._kids[casa_text]._all_char_cred
    assert _all_char_cred_new == 59

    # _all_char_debt: bool = None,
    sue_world._idearoot._kids[casa_text]._all_char_debt = 74
    x_all_char_debt = sue_world._idearoot._kids[casa_text]._all_char_debt
    assert x_all_char_debt == 74
    sue_world.edit_idea_attr(road=casa_road, all_char_debt=59)
    _all_char_debt_new = sue_world._idearoot._kids[casa_text]._all_char_debt
    assert _all_char_debt_new == 59

    # _awardlink: dict = None,
    sue_world._idearoot._kids[casa_text]._awardlinks = {
        "fun": awardlink_shop(lobby_id="fun", credor_weight=1, debtor_weight=7)
    }
    _awardlinks = sue_world._idearoot._kids[casa_text]._awardlinks
    assert _awardlinks == {
        "fun": awardlink_shop(lobby_id="fun", credor_weight=1, debtor_weight=7)
    }
    sue_world.edit_idea_attr(
        road=casa_road,
        awardlink=awardlink_shop(lobby_id="fun", credor_weight=4, debtor_weight=8),
    )
    assert sue_world._idearoot._kids[casa_text]._awardlinks == {
        "fun": awardlink_shop(lobby_id="fun", credor_weight=4, debtor_weight=8)
    }

    # _is_expanded: dict = None,
    sue_world._idearoot._kids[casa_text]._is_expanded = "what"
    _is_expanded = sue_world._idearoot._kids[casa_text]._is_expanded
    assert _is_expanded == "what"
    sue_world.edit_idea_attr(road=casa_road, is_expanded=True)
    assert sue_world._idearoot._kids[casa_text]._is_expanded == True

    # pledge: dict = None,
    sue_world._idearoot._kids[casa_text].pledge = "funfun3"
    pledge = sue_world._idearoot._kids[casa_text].pledge
    assert pledge == "funfun3"
    sue_world.edit_idea_attr(road=casa_road, pledge=True)
    assert sue_world._idearoot._kids[casa_text].pledge == True

    # _range_source_road: dict = None,
    sue_world._idearoot._kids[casa_text]._range_source_road = "fun3rol"
    range_source_road = sue_world._idearoot._kids[casa_text]._range_source_road
    assert range_source_road == "fun3rol"
    end_road = sue_world.make_road(casa_road, "end")
    sue_world.edit_idea_attr(road=casa_road, range_source_road=end_road)
    assert sue_world._idearoot._kids[casa_text]._range_source_road == end_road

    # _healerhold:
    sue_world._idearoot._kids[casa_text]._healerhold = "fun3rol"
    src_healerhold = sue_world._idearoot._kids[casa_text]._healerhold
    assert src_healerhold == "fun3rol"
    sue_text = "Sue"
    yao_text = "Yao"
    x_healerhold = healerhold_shop({sue_text, yao_text})
    sue_world.add_charunit(sue_text)
    sue_world.add_charunit(yao_text)
    sue_world.edit_idea_attr(road=casa_road, healerhold=x_healerhold)
    assert sue_world._idearoot._kids[casa_text]._healerhold == x_healerhold

    # _problem_bool: bool
    sue_world._idearoot._kids[casa_text]._problem_bool = "fun3rol"
    src_problem_bool = sue_world._idearoot._kids[casa_text]._problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True
    sue_world.edit_idea_attr(road=casa_road, problem_bool=x_problem_bool)
    assert sue_world._idearoot._kids[casa_text]._problem_bool == x_problem_bool

    print(f"{casa_road=} {end_road=}")


def test_WorldUnit_edit_idea_attr_worldIsAbleToEditDenomAnyIdeaIfInvaildDenomThrowsError():
    yao_world = worldunit_shop("Yao")
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_idea_attr(road="", denom=46)
    assert str(excinfo.value) == "Root Idea cannot have numor denom reest."

    casa_text = "casa"
    casa_road = yao_world.make_l1_road(casa_text)
    casa_idea = ideaunit_shop(casa_text)
    yao_world.add_l1_idea(casa_idea)
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    clean_road = yao_world.make_road(casa_road, clean_text)
    yao_world.add_idea(clean_idea, parent_road=casa_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_idea_attr(road=clean_road, denom=46)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{clean_road}' if parent '{casa_road}' or ideaunit._numeric_road does not have begin/close range"
    )

    # GIVEN
    yao_world.edit_idea_attr(road=casa_road, begin=44, close=110)
    yao_world.edit_idea_attr(road=clean_road, denom=11)
    clean_idea = yao_world.get_idea_obj(clean_road)
    assert clean_idea._begin == 4
    assert clean_idea._close == 10


def test_WorldUnit_edit_idea_attr_worldIsAbleToEditDenomAnyIdeaInvaildDenomThrowsError():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    casa = "casa"
    w_road = yao_world.make_l1_road(casa)
    casa_idea = ideaunit_shop(casa, _begin=8, _close=14)
    yao_world.add_l1_idea(casa_idea)

    clean = "clean"
    clean_idea = ideaunit_shop(clean, _denom=1)
    c_road = yao_world.make_road(w_road, clean)
    yao_world.add_idea(clean_idea, parent_road=w_road)

    clean_idea = yao_world.get_idea_obj(c_road)

    day = "day_range"
    day_idea = ideaunit_shop(day, _begin=44, _close=110)
    day_road = yao_world.make_l1_road(day)
    yao_world.add_l1_idea(day_idea)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_idea_attr(road=c_road, numeric_road=day_road)
    assert (
        str(excinfo.value)
        == "Idea has begin-close range parent, cannot have numeric_road"
    )

    yao_world.edit_idea_attr(road=w_road, numeric_road=day_road)


def test_WorldUnit_edit_idea_attr_worldWhenParentAndNumeric_roadBothHaveRangeThrowError():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    casa_text = "casa"
    casa_road = yao_world.make_l1_road(casa_text)
    yao_world.add_l1_idea(ideaunit_shop(casa_text))
    day_text = "day_range"
    day_idea = ideaunit_shop(day_text, _begin=44, _close=110)
    day_road = yao_world.make_l1_road(day_text)
    yao_world.add_l1_idea(day_idea)

    casa_idea = yao_world.get_idea_obj(casa_road)
    assert casa_idea._begin is None
    assert casa_idea._close is None

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_idea_attr(road=casa_road, denom=11)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{casa_road}' if parent '{yao_world._real_id}' or ideaunit._numeric_road does not have begin/close range"
    )

    # WHEN
    yao_world.edit_idea_attr(road=casa_road, numeric_road=day_road)

    # THEN
    casa_idea3 = yao_world.get_idea_obj(casa_road)
    assert casa_idea3._addin is None
    assert casa_idea3._numor is None
    assert casa_idea3._denom is None
    assert casa_idea3._reest is None
    assert casa_idea3._begin == 44
    assert casa_idea3._close == 110
    yao_world.edit_idea_attr(road=casa_road, denom=11, numeric_road=day_road)
    assert casa_idea3._begin == 4
    assert casa_idea3._close == 10
    assert casa_idea3._numor == 1
    assert casa_idea3._denom == 11
    assert casa_idea3._reest is False
    assert casa_idea3._addin == 0


def test_WorldUnit_edit_idea_attr_RaisesErrorWhen_healerhold_lobby_ids_DoNotExist():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    casa_text = "casa"
    casa_road = yao_world.make_l1_road(casa_text)
    yao_world.add_l1_idea(ideaunit_shop(casa_text))
    day_text = "day_range"
    day_idea = ideaunit_shop(day_text, _begin=44, _close=110)
    day_road = yao_world.make_l1_road(day_text)
    yao_world.add_l1_idea(day_idea)

    casa_idea = yao_world.get_idea_obj(casa_road)
    assert casa_idea._begin is None
    assert casa_idea._close is None

    # WHEN / THEN
    sue_text = "Sue"
    x_healerhold = healerhold_shop({sue_text})
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_idea_attr(road=casa_road, healerhold=x_healerhold)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit healerhold because lobby_id '{sue_text}' does not exist as lobby in World"
    )


def test_WorldUnit_add_idea_MustReorderKidsDictToBeAlphabetical():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    casa_text = "casa"
    bob_world.add_l1_idea(ideaunit_shop(casa_text))
    swim_text = "swim"
    bob_world.add_l1_idea(ideaunit_shop(swim_text))

    # WHEN
    idea_list = list(bob_world._idearoot._kids.values())

    # THEN
    assert idea_list[0]._label == casa_text


def test_WorldUnit_add_idea_adoptee_RaisesErrorIfAdopteeIdeaDoesNotHaveCorrectParent():
    bob_world = worldunit_shop("Bob")
    sports_text = "sports"
    sports_road = bob_world.make_l1_road(sports_text)
    bob_world.add_l1_idea(ideaunit_shop(sports_text))
    swim_text = "swim"
    bob_world.add_idea(ideaunit_shop(swim_text), parent_road=sports_road)

    # WHEN / THEN
    summer_text = "summer"
    hike_text = "hike"
    hike_road = bob_world.make_road(sports_road, hike_text)
    with pytest_raises(Exception) as excinfo:
        bob_world.add_idea(
            idea_kid=ideaunit_shop(summer_text),
            parent_road=sports_road,
            adoptees=[swim_text, hike_text],
        )
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{hike_road}'"


def test_WorldUnit_add_idea_adoptee_CorrectlyAddsAdoptee():
    bob_world = worldunit_shop("Bob")
    sports_text = "sports"
    sports_road = bob_world.make_l1_road(sports_text)
    bob_world.add_l1_idea(ideaunit_shop(sports_text))
    swim_text = "swim"
    bob_world.add_idea(ideaunit_shop(swim_text), parent_road=sports_road)
    hike_text = "hike"
    bob_world.add_idea(ideaunit_shop(hike_text), parent_road=sports_road)

    sports_swim_road = bob_world.make_road(sports_road, swim_text)
    sports_hike_road = bob_world.make_road(sports_road, hike_text)
    assert bob_world.idea_exists(sports_swim_road)
    assert bob_world.idea_exists(sports_hike_road)
    summer_text = "summer"
    summer_road = bob_world.make_road(sports_road, summer_text)
    summer_swim_road = bob_world.make_road(summer_road, swim_text)
    summer_hike_road = bob_world.make_road(summer_road, hike_text)
    assert bob_world.idea_exists(summer_swim_road) is False
    assert bob_world.idea_exists(summer_hike_road) is False

    # WHEN / THEN
    bob_world.add_idea(
        idea_kid=ideaunit_shop(summer_text),
        parent_road=sports_road,
        adoptees=[swim_text, hike_text],
    )

    # THEN
    summer_idea = bob_world.get_idea_obj(summer_road)
    print(f"{summer_idea._kids.keys()=}")
    assert bob_world.idea_exists(summer_swim_road)
    assert bob_world.idea_exists(summer_hike_road)
    assert bob_world.idea_exists(sports_swim_road) is False
    assert bob_world.idea_exists(sports_hike_road) is False


def test_WorldUnit_add_idea_bundling_SetsNewParentWithWeightEqualToSumOfAdoptedIdeas():
    bob_world = worldunit_shop("Bob")
    sports_text = "sports"
    sports_road = bob_world.make_l1_road(sports_text)
    bob_world.add_l1_idea(ideaunit_shop(sports_text, _weight=2))
    swim_text = "swim"
    swim_weight = 3
    bob_world.add_idea(ideaunit_shop(swim_text, _weight=swim_weight), sports_road)
    hike_text = "hike"
    hike_weight = 5
    bob_world.add_idea(ideaunit_shop(hike_text, _weight=hike_weight), sports_road)
    bball_text = "bball"
    bball_weight = 7
    bob_world.add_idea(ideaunit_shop(bball_text, _weight=bball_weight), sports_road)

    sports_swim_road = bob_world.make_road(sports_road, swim_text)
    sports_hike_road = bob_world.make_road(sports_road, hike_text)
    sports_bball_road = bob_world.make_road(sports_road, bball_text)
    assert bob_world.get_idea_obj(sports_swim_road)._weight == swim_weight
    assert bob_world.get_idea_obj(sports_hike_road)._weight == hike_weight
    assert bob_world.get_idea_obj(sports_bball_road)._weight == bball_weight
    summer_text = "summer"
    summer_road = bob_world.make_road(sports_road, summer_text)
    summer_swim_road = bob_world.make_road(summer_road, swim_text)
    summer_hike_road = bob_world.make_road(summer_road, hike_text)
    summer_bball_road = bob_world.make_road(summer_road, bball_text)
    assert bob_world.idea_exists(summer_swim_road) is False
    assert bob_world.idea_exists(summer_hike_road) is False
    assert bob_world.idea_exists(summer_bball_road) is False

    # WHEN / THEN
    bob_world.add_idea(
        idea_kid=ideaunit_shop(summer_text),
        parent_road=sports_road,
        adoptees=[swim_text, hike_text],
        bundling=True,
    )

    # THEN
    assert bob_world.get_idea_obj(summer_road)._weight == swim_weight + hike_weight
    assert bob_world.get_idea_obj(summer_swim_road)._weight == swim_weight
    assert bob_world.get_idea_obj(summer_hike_road)._weight == hike_weight
    assert bob_world.idea_exists(summer_bball_road) is False
    assert bob_world.idea_exists(sports_swim_road) is False
    assert bob_world.idea_exists(sports_hike_road) is False
    assert bob_world.idea_exists(sports_bball_road)


def test_WorldUnit_del_idea_obj_DeletingBundledIdeaReturnsIdeasToOriginalState():
    bob_world = worldunit_shop("Bob")
    sports_text = "sports"
    sports_road = bob_world.make_l1_road(sports_text)
    bob_world.add_l1_idea(ideaunit_shop(sports_text, _weight=2))
    swim_text = "swim"
    swim_weight = 3
    bob_world.add_idea(ideaunit_shop(swim_text, _weight=swim_weight), sports_road)
    hike_text = "hike"
    hike_weight = 5
    bob_world.add_idea(ideaunit_shop(hike_text, _weight=hike_weight), sports_road)
    bball_text = "bball"
    bball_weight = 7
    bob_world.add_idea(ideaunit_shop(bball_text, _weight=bball_weight), sports_road)

    sports_swim_road = bob_world.make_road(sports_road, swim_text)
    sports_hike_road = bob_world.make_road(sports_road, hike_text)
    sports_bball_road = bob_world.make_road(sports_road, bball_text)
    assert bob_world.get_idea_obj(sports_swim_road)._weight == swim_weight
    assert bob_world.get_idea_obj(sports_hike_road)._weight == hike_weight
    assert bob_world.get_idea_obj(sports_bball_road)._weight == bball_weight
    summer_text = "summer"
    summer_road = bob_world.make_road(sports_road, summer_text)
    summer_swim_road = bob_world.make_road(summer_road, swim_text)
    summer_hike_road = bob_world.make_road(summer_road, hike_text)
    summer_bball_road = bob_world.make_road(summer_road, bball_text)
    assert bob_world.idea_exists(summer_swim_road) is False
    assert bob_world.idea_exists(summer_hike_road) is False
    assert bob_world.idea_exists(summer_bball_road) is False
    bob_world.add_idea(
        idea_kid=ideaunit_shop(summer_text),
        parent_road=sports_road,
        adoptees=[swim_text, hike_text],
        bundling=True,
    )
    assert bob_world.get_idea_obj(summer_road)._weight == swim_weight + hike_weight
    assert bob_world.get_idea_obj(summer_swim_road)._weight == swim_weight
    assert bob_world.get_idea_obj(summer_hike_road)._weight == hike_weight
    assert bob_world.idea_exists(summer_bball_road) is False
    assert bob_world.idea_exists(sports_swim_road) is False
    assert bob_world.idea_exists(sports_hike_road) is False
    assert bob_world.idea_exists(sports_bball_road)
    print(f"{bob_world._idea_dict.keys()=}")

    # WHEN
    bob_world.del_idea_obj(road=summer_road, del_children=False)

    # THEN
    sports_swim_idea = bob_world.get_idea_obj(sports_swim_road)
    sports_hike_idea = bob_world.get_idea_obj(sports_hike_road)
    sports_bball_idea = bob_world.get_idea_obj(sports_bball_road)
    assert sports_swim_idea._weight == swim_weight
    assert sports_hike_idea._weight == hike_weight
    assert sports_bball_idea._weight == bball_weight


def test_WorldUnit_set_awardlink_correctly_sets_awardlinks():
    # GIVEN
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_world.add_charunit(yao_text)
    sue_world.add_charunit(zia_text)
    sue_world.add_charunit(Xio_text)

    assert len(sue_world._chars) == 3
    assert len(sue_world.get_lobby_ids_dict()) == 3
    swim_text = "swim"
    sue_world.add_l1_idea(ideaunit_shop(swim_text))
    awardlink_yao = awardlink_shop(yao_text, credor_weight=10)
    awardlink_zia = awardlink_shop(zia_text, credor_weight=10)
    awardlink_Xio = awardlink_shop(Xio_text, credor_weight=10)
    swim_road = sue_world.make_l1_road(swim_text)
    sue_world.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    sue_world.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    sue_world.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    street_text = "streets"
    sue_world.add_idea(ideaunit_shop(street_text), parent_road=swim_road)
    assert sue_world._idearoot._awardlinks in (None, {})
    assert len(sue_world._idearoot._kids[swim_text]._awardlinks) == 3

    # WHEN
    idea_dict = sue_world.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=} ")
    swim_idea = idea_dict.get(swim_road)
    street_idea = idea_dict.get(sue_world.make_road(swim_road, street_text))

    assert len(swim_idea._awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    assert street_idea._awardlinks in (None, {})
    assert len(street_idea._awardheirs) == 3

    print(f"{len(idea_dict)}")
    print(f"{swim_idea._awardlinks}")
    print(f"{swim_idea._awardheirs}")
    print(f"{swim_idea._awardheirs}")
    assert len(sue_world._idearoot._kids["swim"]._awardheirs) == 3


def test_WorldUnit_set_awardlink_correctly_deletes_awardlinks():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    x_world.add_charunit(yao_text)
    x_world.add_charunit(zia_text)
    x_world.add_charunit(Xio_text)

    swim_text = "swim"
    swim_road = x_world.make_road(prom_text, swim_text)

    x_world.add_l1_idea(ideaunit_shop(swim_text))
    awardlink_yao = awardlink_shop(yao_text, credor_weight=10)
    awardlink_zia = awardlink_shop(zia_text, credor_weight=10)
    awardlink_Xio = awardlink_shop(Xio_text, credor_weight=10)

    swim_idea = x_world.get_idea_obj(swim_road)
    x_world.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    x_world.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    x_world.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    assert len(swim_idea._awardlinks) == 3
    assert len(x_world._idearoot._kids[swim_text]._awardlinks) == 3

    # WHEN
    x_world.edit_idea_attr(swim_road, awardlink_del=yao_text)

    # THEN
    swim_idea = x_world.get_idea_obj(swim_road)
    print(f"{swim_idea._label=}")
    print(f"{swim_idea._awardlinks=}")
    print(f"{swim_idea._awardheirs=}")

    assert len(x_world._idearoot._kids[swim_text]._awardlinks) == 2


def test_WorldUnit__get_filtered_awardlinks_idea_CorrectlyFiltersIdea_awardlinks():
    # GIVEN
    bob_text = "Bob"
    x1_world = worldunit_shop(bob_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_world.add_charunit(xia_text)
    x1_world.add_charunit(zoa_text)

    casa_text = "casa"
    casa_road = x1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_world.make_l1_road(swim_text)
    x1_world.add_l1_idea(ideaunit_shop(casa_text))
    x1_world.add_l1_idea(ideaunit_shop(swim_text))
    x1_world.edit_idea_attr(swim_road, awardlink=awardlink_shop(xia_text))
    x1_world.edit_idea_attr(swim_road, awardlink=awardlink_shop(zoa_text))
    x1_world_swim_idea = x1_world.get_idea_obj(swim_road)
    assert len(x1_world_swim_idea._awardlinks) == 2
    x_world = worldunit_shop(bob_text)
    x_world.add_charunit(xia_text)

    # WHEN
    filtered_idea = x_world._get_filtered_awardlinks_idea(x1_world_swim_idea)

    # THEN
    assert len(filtered_idea._awardlinks) == 1
    assert list(filtered_idea._awardlinks.keys()) == [xia_text]


def test_WorldUnit_add_idea_CorrectlyFiltersIdea_awardlinks():
    # GIVEN
    bob_text = "Bob"
    x1_world = worldunit_shop(bob_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_world.add_charunit(xia_text)
    x1_world.add_charunit(zoa_text)

    casa_text = "casa"
    casa_road = x1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_world.make_l1_road(swim_text)
    x1_world.add_l1_idea(ideaunit_shop(casa_text))
    x1_world.add_l1_idea(ideaunit_shop(swim_text))
    x1_world.edit_idea_attr(swim_road, awardlink=awardlink_shop(xia_text))
    x1_world.edit_idea_attr(swim_road, awardlink=awardlink_shop(zoa_text))
    x1_world_swim_idea = x1_world.get_idea_obj(swim_road)
    assert len(x1_world_swim_idea._awardlinks) == 2

    # WHEN
    x_world = worldunit_shop(bob_text)
    x_world.add_charunit(xia_text)
    x_world.add_l1_idea(x1_world_swim_idea, create_missing_ideas=False)

    # THEN
    x_world_swim_idea = x_world.get_idea_obj(swim_road)
    assert len(x_world_swim_idea._awardlinks) == 1
    assert list(x_world_swim_idea._awardlinks.keys()) == [xia_text]
