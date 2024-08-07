from src.bud.healer import healerhold_shop
from src.bud.examples.example_buds import get_budunit_with_4_levels
from src.bud.idea import ideaunit_shop
from src.bud.reason_idea import reasonunit_shop, factunit_shop
from src.bud.bud import budunit_shop
from src.bud.group import awardlink_shop
from pytest import raises as pytest_raises
from src._road.road import default_road_delimiter_if_none


def test_BudUnit_set_idea_RaisesErrorWhen_parent_road_IsInvalid():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    invalid_rootnode_swim_road = "swimming"
    assert invalid_rootnode_swim_road != zia_bud._real_id
    casa_text = "casa"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_idea(
            ideaunit_shop(casa_text), parent_road=invalid_rootnode_swim_road
        )
    assert (
        str(excinfo.value)
        == f"set_idea failed because parent_road '{invalid_rootnode_swim_road}' has an invalid root node"
    )


def test_BudUnit_set_idea_RaisesErrorWhen_parent_road_IdeaDoesNotExist():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_road = zia_bud.make_l1_road("swimming")
    casa_text = "casa"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_idea(
            ideaunit_shop(casa_text),
            parent_road=swim_road,
            create_missing_ancestors=False,
        )
    assert (
        str(excinfo.value)
        == f"set_idea failed because '{swim_road}' idea does not exist."
    )


def test_BudUnit_set_idea_RaisesErrorWhen_label_IsNotNode():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_road = zia_bud.make_l1_road("swimming")
    casa_text = "casa"
    casa_road = zia_bud.make_l1_road(casa_text)
    run_text = "run"
    run_road = zia_bud.make_road(casa_road, run_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_idea(ideaunit_shop(run_road), parent_road=swim_road)
    assert (
        str(excinfo.value) == f"set_idea failed because '{run_road}' is not a RoadNode."
    )


def test_BudUnit_set_l1_idea_CorrectlySetsAttr():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_text = "casa"
    casa_road = zia_bud.make_l1_road(casa_text)
    assert zia_bud.idea_exists(casa_road) is False

    # WHEN
    zia_bud.set_l1_idea(ideaunit_shop(casa_text))

    # THEN
    assert zia_bud.idea_exists(casa_road)


def test_BudUnit_add_idea_SetsAttr_Scenario0():
    # ESTABLISH
    bob_text = "Bob"
    slash_text = "/"
    bob_budunit = budunit_shop(bob_text, _road_delimiter=slash_text)
    casa_road = bob_budunit.make_l1_road("casa")
    assert not bob_budunit.idea_exists(casa_road)

    # WHEN
    bob_budunit.add_idea(casa_road)

    # THEN
    assert bob_budunit.idea_exists(casa_road)
    casa_ideaunit = bob_budunit.get_idea_obj(casa_road)
    assert casa_ideaunit._road_delimiter == bob_budunit._road_delimiter
    assert not casa_ideaunit.pledge


def test_BudUnit_add_idea_SetsAttr_Scenario1():
    # ESTABLISH
    bob_text = "Bob"
    bob_budunit = budunit_shop(bob_text)
    casa_road = bob_budunit.make_l1_road("casa")
    casa_mass = 13
    casa_pledge = True

    # WHEN
    bob_budunit.add_idea(casa_road, mass=casa_mass, pledge=casa_pledge)

    # THEN
    casa_ideaunit = bob_budunit.get_idea_obj(casa_road)
    assert casa_ideaunit._mass == casa_mass
    assert casa_ideaunit.pledge


def test_BudUnit_add_idea_ReturnsObj():
    # ESTABLISH
    bob_text = "Bob"
    bob_budunit = budunit_shop(bob_text)
    casa_road = bob_budunit.make_l1_road("casa")
    casa_mass = 13

    # WHEN
    casa_ideaunit = bob_budunit.add_idea(casa_road, mass=casa_mass)

    # THEN
    assert casa_ideaunit._label == "casa"
    assert casa_ideaunit._mass == casa_mass


def test_BudUnit_IdeaUnit_kids_CanHaveKids():
    # ESTABLISH / WHEN
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._idearoot._kids
    print(f"{len(sue_bud._idearoot._kids)=} {sue_bud._idearoot._parent_road=}")
    assert sue_bud.get_level_count(level=0) == 1
    weekdays_kids = sue_bud._idearoot._kids["weekdays"]._kids
    weekdays_len = len(weekdays_kids)
    print(f"{weekdays_len=} {sue_bud._idearoot._parent_road=}")
    # for idea in weekdays_kids.values():
    #     print(f"{idea._label=}")
    assert len(sue_bud._idea_dict) == 17
    assert sue_bud.get_level_count(level=1) == 4
    assert sue_bud.get_level_count(level=2) == 10
    assert sue_bud.get_level_count(level=3) == 2


def test_BudUnit_set_idea_CanAddKidTo_idearoot():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()

    assert len(sue_bud._idea_dict) == 17
    assert sue_bud.get_level_count(level=1) == 4

    new_idea_parent_road = sue_bud._real_id

    # WHEN
    sue_bud.set_idea(ideaunit_shop("new_idea"), parent_road=new_idea_parent_road)
    sue_bud.settle_bud()

    # THEN
    print(f"{(sue_bud._owner_id == new_idea_parent_road[0])=}")
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert len(sue_bud._idea_dict) == 18
    assert sue_bud.get_level_count(level=1) == 5


def test_BudUnit_set_idea_CanAddKidToKidIdea():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    assert len(sue_bud._idea_dict) == 17
    assert sue_bud.get_level_count(level=2) == 10

    # WHEN
    new_idea_parent_road = sue_bud.make_l1_road("casa")
    sue_bud.set_idea(ideaunit_shop("new_york"), parent_road=new_idea_parent_road)
    sue_bud.settle_bud()

    # THEN
    # print(f"{(sue_bud._owner_id == new_idea_parent_road[0])=}")
    # print(sue_bud._idearoot._kids["casa"])
    # print(f"{(len(new_idea_parent_road) == 1)=}")
    assert len(sue_bud._idea_dict) == 18
    assert sue_bud.get_level_count(level=2) == 11
    new_york_idea = sue_bud._idearoot._kids["casa"]._kids["new_york"]
    assert new_york_idea._parent_road == sue_bud.make_l1_road("casa")
    assert new_york_idea._road_delimiter == sue_bud._road_delimiter
    new_york_idea.set_parent_road(parent_road="testing")
    assert sue_bud._idearoot._kids["casa"]._kids["new_york"]._parent_road == "testing"
    assert sue_bud.get_agenda_dict()


def test_BudUnit_set_idea_CanAddKidToGrandkidIdea():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()

    assert len(sue_bud._idea_dict) == 17
    assert sue_bud.get_level_count(level=3) == 2
    wkday_road = sue_bud.make_l1_road("weekdays")
    new_idea_parent_road = sue_bud.make_road(wkday_road, "Wednesday")

    # WHEN
    sue_bud.set_idea(ideaunit_shop("new_idea"), parent_road=new_idea_parent_road)
    sue_bud.settle_bud()

    # THEN
    print(f"{(sue_bud._owner_id == new_idea_parent_road[0])=}")
    print(sue_bud._idearoot._kids["casa"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert len(sue_bud._idea_dict) == 18
    assert sue_bud.get_level_count(level=3) == 3


def test_BudUnit_set_idea_CorrectlyAddsIdeaObjWithNonstandard_delimiter():
    # ESTABLISH
    slash_text = "/"
    assert slash_text != default_road_delimiter_if_none()
    bob_bud = budunit_shop("Bob", _road_delimiter=slash_text)
    casa_text = "casa"
    week_text = "week"
    wed_text = "Wednesday"
    casa_road = bob_bud.make_l1_road(casa_text)
    week_road = bob_bud.make_l1_road(week_text)
    wed_road = bob_bud.make_road(week_road, wed_text)
    bob_bud.set_l1_idea(ideaunit_shop(casa_text))
    bob_bud.set_l1_idea(ideaunit_shop(week_text))
    bob_bud.set_idea(ideaunit_shop(wed_text), week_road)
    print(f"{bob_bud._idearoot._kids.keys()=}")
    assert len(bob_bud._idearoot._kids) == 2
    wed_idea = bob_bud.get_idea_obj(wed_road)
    assert wed_idea._road_delimiter == slash_text
    assert wed_idea._road_delimiter == bob_bud._road_delimiter

    # WHEN
    bob_bud.edit_idea_attr(
        road=casa_road, reason_base=week_road, reason_premise=wed_road
    )

    # THEN
    casa_idea = bob_bud.get_idea_obj(casa_road)
    assert casa_idea._reasonunits.get(week_road) is not None


def test_BudUnit_set_idea_CanCreateRoadUnitToGrandkidIdea():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()

    assert len(sue_bud._idea_dict) == 17
    assert sue_bud.get_level_count(level=3) == 2
    ww2_road = sue_bud.make_l1_road("ww2")
    battles_road = sue_bud.make_road(ww2_road, "battles")
    new_idea_parent_road = sue_bud.make_road(battles_road, "coralsea")
    new_idea = ideaunit_shop(_label="USS Saratoga")

    # WHEN
    sue_bud.set_idea(new_idea, parent_road=new_idea_parent_road)
    sue_bud.settle_bud()

    # THEN
    print(sue_bud._idearoot._kids["ww2"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert sue_bud._idearoot._kids["ww2"]._label == "ww2"
    assert sue_bud._idearoot._kids["ww2"]._kids["battles"]._label == "battles"
    assert len(sue_bud._idea_dict) == 21
    assert sue_bud.get_level_count(level=3) == 3


def test_BudUnit_set_idea_CreatesIdeaUnitsUsedBy_reasonunits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()

    assert len(sue_bud._idea_dict) == 17
    assert sue_bud.get_level_count(level=3) == 2
    casa_road = sue_bud.make_l1_road("casa")
    new_idea_parent_road = sue_bud.make_road(casa_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(clean_cookery_text, _mass=40, pledge=True)

    buildings_text = "buildings"
    buildings_road = sue_bud.make_l1_road(buildings_text)
    cookery_room_text = "cookery"
    cookery_room_road = sue_bud.make_road(buildings_road, cookery_room_text)
    cookery_dirty_text = "dirty"
    cookery_dirty_road = sue_bud.make_road(cookery_room_road, cookery_dirty_text)
    reason_x = reasonunit_shop(base=cookery_room_road)
    reason_x.set_premise(premise=cookery_dirty_road)
    clean_cookery_idea.set_reasonunit(reason=reason_x)

    assert sue_bud._idearoot.get_kid(buildings_text) is None

    # WHEN
    sue_bud.set_idea(
        idea_kid=clean_cookery_idea,
        parent_road=new_idea_parent_road,
        create_missing_ideas=True,
    )
    sue_bud.settle_bud()

    # THEN
    print(f"{(len(new_idea_parent_road) == 1)=}")
    # for idea_kid in sue_bud._idearoot._kids.values():
    #     print(f"{idea_kid._label=}")
    assert sue_bud._idearoot.get_kid(buildings_text) is not None
    assert sue_bud.get_idea_obj(buildings_road) is not None
    assert sue_bud.get_idea_obj(cookery_dirty_road) is not None
    assert len(sue_bud._idea_dict) == 22
    assert sue_bud.get_level_count(level=3) == 4


def test_BudUnit_set_idea_CorrectlySets_bud_real_id_AND_fund_coin():
    # ESTABLISH'
    x_fund_coin = 500
    sue_bud = get_budunit_with_4_levels()
    sue_bud._fund_coin = x_fund_coin
    bud_real_id = "Texas"
    sue_bud.set_real_id(bud_real_id)
    assert sue_bud._real_id == bud_real_id

    casa_road = sue_bud.make_l1_road("casa")
    clean_road = sue_bud.make_road(casa_road, "cleaning")
    cookery_text = "cookery ready to use"
    cookery_road = sue_bud.make_road(clean_road, cookery_text)

    # WHEN
    sue_bud.set_idea(ideaunit_shop(cookery_text), clean_road)

    # THEN
    cookery_idea = sue_bud.get_idea_obj(cookery_road)
    assert cookery_idea._bud_real_id == bud_real_id
    assert cookery_idea._fund_coin == x_fund_coin


def test_BudUnit_del_idea_obj_Level0CannotBeDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    root_road = sue_bud._real_id

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.del_idea_obj(road=root_road)
    assert str(excinfo.value) == "Idearoot cannot be deleted"


def test_BudUnit_del_idea_obj_Level1CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_text = "weekdays"
    week_road = sue_bud.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = sue_bud.make_road(week_road, sun_text)
    assert sue_bud.get_idea_obj(week_road)
    assert sue_bud.get_idea_obj(sun_road)

    # WHEN
    sue_bud.del_idea_obj(road=week_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_idea_obj(week_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{week_road}'"
    new_sunday_road = sue_bud.make_l1_road("Sunday")
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_idea_obj(new_sunday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{new_sunday_road}'"


def test_BudUnit_del_idea_obj_Level1CanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_text = "weekdays"
    week_road = sue_bud.make_l1_road(week_text)
    sun_text = "Sunday"
    old_sunday_road = sue_bud.make_road(week_road, sun_text)
    assert sue_bud.get_idea_obj(old_sunday_road)

    # WHEN
    sue_bud.del_idea_obj(road=week_road, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_idea_obj(old_sunday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{old_sunday_road}'"
    new_sunday_road = sue_bud.make_l1_road(sun_text)
    assert sue_bud.get_idea_obj(new_sunday_road)
    new_sunday_idea = sue_bud.get_idea_obj(new_sunday_road)
    assert new_sunday_idea._parent_road == sue_bud._real_id


def test_BudUnit_del_idea_obj_LevelNCanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    states_text = "nation-state"
    states_road = sue_bud.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_bud.make_road(states_road, usa_text)
    texas_text = "Texas"
    oregon_text = "Oregon"
    usa_texas_road = sue_bud.make_road(usa_road, texas_text)
    usa_oregon_road = sue_bud.make_road(usa_road, oregon_text)
    states_texas_road = sue_bud.make_road(states_road, texas_text)
    states_oregon_road = sue_bud.make_road(states_road, oregon_text)
    assert sue_bud.idea_exists(usa_road)
    assert sue_bud.idea_exists(usa_texas_road)
    assert sue_bud.idea_exists(usa_oregon_road)
    assert sue_bud.idea_exists(states_texas_road) is False
    assert sue_bud.idea_exists(states_oregon_road) is False

    # WHEN
    sue_bud.del_idea_obj(road=usa_road, del_children=False)

    # THEN
    assert sue_bud.idea_exists(states_texas_road)
    assert sue_bud.idea_exists(states_oregon_road)
    assert sue_bud.idea_exists(usa_texas_road) is False
    assert sue_bud.idea_exists(usa_oregon_road) is False
    assert sue_bud.idea_exists(usa_road) is False


def test_BudUnit_del_idea_obj_Level2CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    wkday_road = sue_bud.make_l1_road("weekdays")
    monday_road = sue_bud.make_road(wkday_road, "Monday")
    assert sue_bud.get_idea_obj(monday_road)

    # WHEN
    sue_bud.del_idea_obj(road=monday_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_idea_obj(monday_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{monday_road}'"


def test_BudUnit_del_idea_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    states_text = "nation-state"
    states_road = sue_bud.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_bud.make_road(states_road, usa_text)
    texas_text = "Texas"
    usa_texas_road = sue_bud.make_road(usa_road, texas_text)
    assert sue_bud.get_idea_obj(usa_texas_road)

    # WHEN
    sue_bud.del_idea_obj(road=usa_texas_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_idea_obj(usa_texas_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{usa_texas_road}'"


def test_BudUnit_edit_idea_attr_IsAbleToEditAnyAncestor_Idea():
    sue_bud = get_budunit_with_4_levels()
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    print(f"{casa_road=}")
    old_mass = sue_bud._idearoot._kids[casa_text]._mass
    assert old_mass == 30
    sue_bud.edit_idea_attr(road=casa_road, mass=23)
    new_mass = sue_bud._idearoot._kids[casa_text]._mass
    assert new_mass == 23

    # uid: int = None,
    sue_bud._idearoot._kids[casa_text]._uid = 34
    x_uid = sue_bud._idearoot._kids[casa_text]._uid
    assert x_uid == 34
    sue_bud.edit_idea_attr(road=casa_road, uid=23)
    uid_new = sue_bud._idearoot._kids[casa_text]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    sue_bud._idearoot._kids[casa_text]._begin = 39
    x_begin = sue_bud._idearoot._kids[casa_text]._begin
    assert x_begin == 39
    sue_bud._idearoot._kids[casa_text]._close = 43
    x_close = sue_bud._idearoot._kids[casa_text]._close
    assert x_close == 43
    sue_bud.edit_idea_attr(road=casa_road, begin=25, close=29)
    assert sue_bud._idearoot._kids[casa_text]._begin == 25
    assert sue_bud._idearoot._kids[casa_text]._close == 29

    # factunit: factunit_shop = None,
    # sue_bud._idearoot._kids[casa_text]._factunits = None
    assert sue_bud._idearoot._kids[casa_text]._factunits == {}
    wkdays_road = sue_bud.make_l1_road("weekdays")
    fact_road = sue_bud.make_road(wkdays_road, "Sunday")
    factunit_x = factunit_shop(base=fact_road, pick=fact_road)

    casa_factunits = sue_bud._idearoot._kids[casa_text]._factunits
    print(f"{casa_factunits=}")
    sue_bud.edit_idea_attr(road=casa_road, factunit=factunit_x)
    casa_factunits = sue_bud._idearoot._kids[casa_text]._factunits
    print(f"{casa_factunits=}")
    assert sue_bud._idearoot._kids[casa_text]._factunits == {
        factunit_x.base: factunit_x
    }

    # _descendant_pledge_count: int = None,
    sue_bud._idearoot._kids[casa_text]._descendant_pledge_count = 81
    x_descendant_pledge_count = sue_bud._idearoot._kids[
        casa_text
    ]._descendant_pledge_count
    assert x_descendant_pledge_count == 81
    sue_bud.edit_idea_attr(road=casa_road, descendant_pledge_count=67)
    _descendant_pledge_count_new = sue_bud._idearoot._kids[
        casa_text
    ]._descendant_pledge_count
    assert _descendant_pledge_count_new == 67

    # _all_acct_cred: bool = None,
    sue_bud._idearoot._kids[casa_text]._all_acct_cred = 74
    x_all_acct_cred = sue_bud._idearoot._kids[casa_text]._all_acct_cred
    assert x_all_acct_cred == 74
    sue_bud.edit_idea_attr(road=casa_road, all_acct_cred=59)
    _all_acct_cred_new = sue_bud._idearoot._kids[casa_text]._all_acct_cred
    assert _all_acct_cred_new == 59

    # _all_acct_debt: bool = None,
    sue_bud._idearoot._kids[casa_text]._all_acct_debt = 74
    x_all_acct_debt = sue_bud._idearoot._kids[casa_text]._all_acct_debt
    assert x_all_acct_debt == 74
    sue_bud.edit_idea_attr(road=casa_road, all_acct_debt=59)
    _all_acct_debt_new = sue_bud._idearoot._kids[casa_text]._all_acct_debt
    assert _all_acct_debt_new == 59

    # _awardlink: dict = None,
    sue_bud._idearoot._kids[casa_text]._awardlinks = {
        "fun": awardlink_shop(group_id="fun", give_force=1, take_force=7)
    }
    _awardlinks = sue_bud._idearoot._kids[casa_text]._awardlinks
    assert _awardlinks == {
        "fun": awardlink_shop(group_id="fun", give_force=1, take_force=7)
    }
    sue_bud.edit_idea_attr(
        road=casa_road,
        awardlink=awardlink_shop(group_id="fun", give_force=4, take_force=8),
    )
    assert sue_bud._idearoot._kids[casa_text]._awardlinks == {
        "fun": awardlink_shop(group_id="fun", give_force=4, take_force=8)
    }

    # _is_expanded: dict = None,
    sue_bud._idearoot._kids[casa_text]._is_expanded = "what"
    _is_expanded = sue_bud._idearoot._kids[casa_text]._is_expanded
    assert _is_expanded == "what"
    sue_bud.edit_idea_attr(road=casa_road, is_expanded=True)
    assert sue_bud._idearoot._kids[casa_text]._is_expanded == True

    # pledge: dict = None,
    sue_bud._idearoot._kids[casa_text].pledge = "funfun3"
    pledge = sue_bud._idearoot._kids[casa_text].pledge
    assert pledge == "funfun3"
    sue_bud.edit_idea_attr(road=casa_road, pledge=True)
    assert sue_bud._idearoot._kids[casa_text].pledge == True

    # _range_source_road: dict = None,
    sue_bud._idearoot._kids[casa_text]._range_source_road = "fun3rol"
    range_source_road = sue_bud._idearoot._kids[casa_text]._range_source_road
    assert range_source_road == "fun3rol"
    end_road = sue_bud.make_road(casa_road, "end")
    sue_bud.edit_idea_attr(road=casa_road, range_source_road=end_road)
    assert sue_bud._idearoot._kids[casa_text]._range_source_road == end_road

    # _healerhold:
    sue_bud._idearoot._kids[casa_text]._healerhold = "fun3rol"
    src_healerhold = sue_bud._idearoot._kids[casa_text]._healerhold
    assert src_healerhold == "fun3rol"
    sue_text = "Sue"
    yao_text = "Yao"
    x_healerhold = healerhold_shop({sue_text, yao_text})
    sue_bud.add_acctunit(sue_text)
    sue_bud.add_acctunit(yao_text)
    sue_bud.edit_idea_attr(road=casa_road, healerhold=x_healerhold)
    assert sue_bud._idearoot._kids[casa_text]._healerhold == x_healerhold

    # _problem_bool: bool
    sue_bud._idearoot._kids[casa_text]._problem_bool = "fun3rol"
    src_problem_bool = sue_bud._idearoot._kids[casa_text]._problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True
    sue_bud.edit_idea_attr(road=casa_road, problem_bool=x_problem_bool)
    assert sue_bud._idearoot._kids[casa_text]._problem_bool == x_problem_bool

    print(f"{casa_road=} {end_road=}")


def test_BudUnit_edit_idea_attr_budIsAbleToEditDenomAnyIdeaIfInvaildDenomThrowsError():
    yao_bud = budunit_shop("Yao")
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_idea_attr(road="", denom=46)
    assert str(excinfo.value) == "Root Idea cannot have numor denom reest."

    casa_text = "casa"
    casa_road = yao_bud.make_l1_road(casa_text)
    casa_idea = ideaunit_shop(casa_text)
    yao_bud.set_l1_idea(casa_idea)
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    clean_road = yao_bud.make_road(casa_road, clean_text)
    yao_bud.set_idea(clean_idea, parent_road=casa_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_idea_attr(road=clean_road, denom=46)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{clean_road}' if parent '{casa_road}' or ideaunit._numeric_road does not have begin/close range"
    )

    # ESTABLISH
    yao_bud.edit_idea_attr(road=casa_road, begin=44, close=110)
    yao_bud.edit_idea_attr(road=clean_road, denom=11)
    clean_idea = yao_bud.get_idea_obj(clean_road)
    assert clean_idea._begin == 4
    assert clean_idea._close == 10


def test_BudUnit_edit_idea_attr_budIsAbleToEditDenomAnyIdeaInvaildDenomThrowsError():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    casa = "casa"
    w_road = yao_bud.make_l1_road(casa)
    casa_idea = ideaunit_shop(casa, _begin=8, _close=14)
    yao_bud.set_l1_idea(casa_idea)

    clean = "clean"
    clean_idea = ideaunit_shop(clean, _denom=1)
    c_road = yao_bud.make_road(w_road, clean)
    yao_bud.set_idea(clean_idea, parent_road=w_road)

    clean_idea = yao_bud.get_idea_obj(c_road)

    day = "day_range"
    day_idea = ideaunit_shop(day, _begin=44, _close=110)
    day_road = yao_bud.make_l1_road(day)
    yao_bud.set_l1_idea(day_idea)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_idea_attr(road=c_road, numeric_road=day_road)
    assert (
        str(excinfo.value)
        == "Idea has begin-close range parent, cannot have numeric_road"
    )

    yao_bud.edit_idea_attr(road=w_road, numeric_road=day_road)


def test_BudUnit_edit_idea_attr_budWhenParentAndNumeric_roadBothHaveRangeThrowError():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    casa_text = "casa"
    casa_road = yao_bud.make_l1_road(casa_text)
    yao_bud.set_l1_idea(ideaunit_shop(casa_text))
    day_text = "day_range"
    day_idea = ideaunit_shop(day_text, _begin=44, _close=110)
    day_road = yao_bud.make_l1_road(day_text)
    yao_bud.set_l1_idea(day_idea)

    casa_idea = yao_bud.get_idea_obj(casa_road)
    assert casa_idea._begin is None
    assert casa_idea._close is None

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_idea_attr(road=casa_road, denom=11)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{casa_road}' if parent '{yao_bud._real_id}' or ideaunit._numeric_road does not have begin/close range"
    )

    # WHEN
    yao_bud.edit_idea_attr(road=casa_road, numeric_road=day_road)

    # THEN
    casa_idea3 = yao_bud.get_idea_obj(casa_road)
    assert casa_idea3._addin is None
    assert casa_idea3._numor is None
    assert casa_idea3._denom is None
    assert casa_idea3._reest is None
    assert casa_idea3._begin == 44
    assert casa_idea3._close == 110
    yao_bud.edit_idea_attr(road=casa_road, denom=11, numeric_road=day_road)
    assert casa_idea3._begin == 4
    assert casa_idea3._close == 10
    assert casa_idea3._numor == 1
    assert casa_idea3._denom == 11
    assert casa_idea3._reest is False
    assert casa_idea3._addin == 0


def test_BudUnit_edit_idea_attr_RaisesErrorWhen_healerhold_group_ids_DoNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    casa_text = "casa"
    casa_road = yao_bud.make_l1_road(casa_text)
    yao_bud.set_l1_idea(ideaunit_shop(casa_text))
    day_text = "day_range"
    day_idea = ideaunit_shop(day_text, _begin=44, _close=110)
    day_road = yao_bud.make_l1_road(day_text)
    yao_bud.set_l1_idea(day_idea)

    casa_idea = yao_bud.get_idea_obj(casa_road)
    assert casa_idea._begin is None
    assert casa_idea._close is None

    # WHEN / THEN
    sue_text = "Sue"
    x_healerhold = healerhold_shop({sue_text})
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_idea_attr(road=casa_road, healerhold=x_healerhold)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit healerhold because group_id '{sue_text}' does not exist as group in Bud"
    )


def test_BudUnit_set_idea_MustReorderKidsDictToBeAlphabetical():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    casa_text = "casa"
    bob_bud.set_l1_idea(ideaunit_shop(casa_text))
    swim_text = "swim"
    bob_bud.set_l1_idea(ideaunit_shop(swim_text))

    # WHEN
    idea_list = list(bob_bud._idearoot._kids.values())

    # THEN
    assert idea_list[0]._label == casa_text


def test_BudUnit_set_idea_adoptee_RaisesErrorIfAdopteeIdeaDoesNotHaveCorrectParent():
    bob_bud = budunit_shop("Bob")
    sports_text = "sports"
    sports_road = bob_bud.make_l1_road(sports_text)
    bob_bud.set_l1_idea(ideaunit_shop(sports_text))
    swim_text = "swim"
    bob_bud.set_idea(ideaunit_shop(swim_text), parent_road=sports_road)

    # WHEN / THEN
    summer_text = "summer"
    hike_text = "hike"
    hike_road = bob_bud.make_road(sports_road, hike_text)
    with pytest_raises(Exception) as excinfo:
        bob_bud.set_idea(
            idea_kid=ideaunit_shop(summer_text),
            parent_road=sports_road,
            adoptees=[swim_text, hike_text],
        )
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{hike_road}'"


def test_BudUnit_set_idea_adoptee_CorrectlyAddsAdoptee():
    bob_bud = budunit_shop("Bob")
    sports_text = "sports"
    sports_road = bob_bud.make_l1_road(sports_text)
    bob_bud.set_l1_idea(ideaunit_shop(sports_text))
    swim_text = "swim"
    bob_bud.set_idea(ideaunit_shop(swim_text), parent_road=sports_road)
    hike_text = "hike"
    bob_bud.set_idea(ideaunit_shop(hike_text), parent_road=sports_road)

    sports_swim_road = bob_bud.make_road(sports_road, swim_text)
    sports_hike_road = bob_bud.make_road(sports_road, hike_text)
    assert bob_bud.idea_exists(sports_swim_road)
    assert bob_bud.idea_exists(sports_hike_road)
    summer_text = "summer"
    summer_road = bob_bud.make_road(sports_road, summer_text)
    summer_swim_road = bob_bud.make_road(summer_road, swim_text)
    summer_hike_road = bob_bud.make_road(summer_road, hike_text)
    assert bob_bud.idea_exists(summer_swim_road) is False
    assert bob_bud.idea_exists(summer_hike_road) is False

    # WHEN / THEN
    bob_bud.set_idea(
        idea_kid=ideaunit_shop(summer_text),
        parent_road=sports_road,
        adoptees=[swim_text, hike_text],
    )

    # THEN
    summer_idea = bob_bud.get_idea_obj(summer_road)
    print(f"{summer_idea._kids.keys()=}")
    assert bob_bud.idea_exists(summer_swim_road)
    assert bob_bud.idea_exists(summer_hike_road)
    assert bob_bud.idea_exists(sports_swim_road) is False
    assert bob_bud.idea_exists(sports_hike_road) is False


def test_BudUnit_set_idea_bundling_SetsNewParentWithMassEqualToSumOfAdoptedIdeas():
    bob_bud = budunit_shop("Bob")
    sports_text = "sports"
    sports_road = bob_bud.make_l1_road(sports_text)
    bob_bud.set_l1_idea(ideaunit_shop(sports_text, _mass=2))
    swim_text = "swim"
    swim_mass = 3
    bob_bud.set_idea(ideaunit_shop(swim_text, _mass=swim_mass), sports_road)
    hike_text = "hike"
    hike_mass = 5
    bob_bud.set_idea(ideaunit_shop(hike_text, _mass=hike_mass), sports_road)
    bball_text = "bball"
    bball_mass = 7
    bob_bud.set_idea(ideaunit_shop(bball_text, _mass=bball_mass), sports_road)

    sports_swim_road = bob_bud.make_road(sports_road, swim_text)
    sports_hike_road = bob_bud.make_road(sports_road, hike_text)
    sports_bball_road = bob_bud.make_road(sports_road, bball_text)
    assert bob_bud.get_idea_obj(sports_swim_road)._mass == swim_mass
    assert bob_bud.get_idea_obj(sports_hike_road)._mass == hike_mass
    assert bob_bud.get_idea_obj(sports_bball_road)._mass == bball_mass
    summer_text = "summer"
    summer_road = bob_bud.make_road(sports_road, summer_text)
    summer_swim_road = bob_bud.make_road(summer_road, swim_text)
    summer_hike_road = bob_bud.make_road(summer_road, hike_text)
    summer_bball_road = bob_bud.make_road(summer_road, bball_text)
    assert bob_bud.idea_exists(summer_swim_road) is False
    assert bob_bud.idea_exists(summer_hike_road) is False
    assert bob_bud.idea_exists(summer_bball_road) is False

    # WHEN / THEN
    bob_bud.set_idea(
        idea_kid=ideaunit_shop(summer_text),
        parent_road=sports_road,
        adoptees=[swim_text, hike_text],
        bundling=True,
    )

    # THEN
    assert bob_bud.get_idea_obj(summer_road)._mass == swim_mass + hike_mass
    assert bob_bud.get_idea_obj(summer_swim_road)._mass == swim_mass
    assert bob_bud.get_idea_obj(summer_hike_road)._mass == hike_mass
    assert bob_bud.idea_exists(summer_bball_road) is False
    assert bob_bud.idea_exists(sports_swim_road) is False
    assert bob_bud.idea_exists(sports_hike_road) is False
    assert bob_bud.idea_exists(sports_bball_road)


def test_BudUnit_del_idea_obj_DeletingBundledIdeaReturnsIdeasToOriginalState():
    bob_bud = budunit_shop("Bob")
    sports_text = "sports"
    sports_road = bob_bud.make_l1_road(sports_text)
    bob_bud.set_l1_idea(ideaunit_shop(sports_text, _mass=2))
    swim_text = "swim"
    swim_mass = 3
    bob_bud.set_idea(ideaunit_shop(swim_text, _mass=swim_mass), sports_road)
    hike_text = "hike"
    hike_mass = 5
    bob_bud.set_idea(ideaunit_shop(hike_text, _mass=hike_mass), sports_road)
    bball_text = "bball"
    bball_mass = 7
    bob_bud.set_idea(ideaunit_shop(bball_text, _mass=bball_mass), sports_road)

    sports_swim_road = bob_bud.make_road(sports_road, swim_text)
    sports_hike_road = bob_bud.make_road(sports_road, hike_text)
    sports_bball_road = bob_bud.make_road(sports_road, bball_text)
    assert bob_bud.get_idea_obj(sports_swim_road)._mass == swim_mass
    assert bob_bud.get_idea_obj(sports_hike_road)._mass == hike_mass
    assert bob_bud.get_idea_obj(sports_bball_road)._mass == bball_mass
    summer_text = "summer"
    summer_road = bob_bud.make_road(sports_road, summer_text)
    summer_swim_road = bob_bud.make_road(summer_road, swim_text)
    summer_hike_road = bob_bud.make_road(summer_road, hike_text)
    summer_bball_road = bob_bud.make_road(summer_road, bball_text)
    assert bob_bud.idea_exists(summer_swim_road) is False
    assert bob_bud.idea_exists(summer_hike_road) is False
    assert bob_bud.idea_exists(summer_bball_road) is False
    bob_bud.set_idea(
        idea_kid=ideaunit_shop(summer_text),
        parent_road=sports_road,
        adoptees=[swim_text, hike_text],
        bundling=True,
    )
    assert bob_bud.get_idea_obj(summer_road)._mass == swim_mass + hike_mass
    assert bob_bud.get_idea_obj(summer_swim_road)._mass == swim_mass
    assert bob_bud.get_idea_obj(summer_hike_road)._mass == hike_mass
    assert bob_bud.idea_exists(summer_bball_road) is False
    assert bob_bud.idea_exists(sports_swim_road) is False
    assert bob_bud.idea_exists(sports_hike_road) is False
    assert bob_bud.idea_exists(sports_bball_road)
    print(f"{bob_bud._idea_dict.keys()=}")

    # WHEN
    bob_bud.del_idea_obj(road=summer_road, del_children=False)

    # THEN
    sports_swim_idea = bob_bud.get_idea_obj(sports_swim_road)
    sports_hike_idea = bob_bud.get_idea_obj(sports_hike_road)
    sports_bball_idea = bob_bud.get_idea_obj(sports_bball_road)
    assert sports_swim_idea._mass == swim_mass
    assert sports_hike_idea._mass == hike_mass
    assert sports_bball_idea._mass == bball_mass


def test_BudUnit_set_awardlink_correctly_sets_awardlinks():
    # ESTABLISH
    sue_text = "Sue"
    sue_bud = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_bud.add_acctunit(yao_text)
    sue_bud.add_acctunit(zia_text)
    sue_bud.add_acctunit(Xio_text)

    assert len(sue_bud._accts) == 3
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 3
    swim_text = "swim"
    sue_bud.set_l1_idea(ideaunit_shop(swim_text))
    awardlink_yao = awardlink_shop(yao_text, give_force=10)
    awardlink_zia = awardlink_shop(zia_text, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_text, give_force=10)
    swim_road = sue_bud.make_l1_road(swim_text)
    sue_bud.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    sue_bud.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    sue_bud.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    street_text = "streets"
    sue_bud.set_idea(ideaunit_shop(street_text), parent_road=swim_road)
    assert sue_bud._idearoot._awardlinks in (None, {})
    assert len(sue_bud._idearoot._kids[swim_text]._awardlinks) == 3

    # WHEN
    idea_dict = sue_bud.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=} ")
    swim_idea = idea_dict.get(swim_road)
    street_idea = idea_dict.get(sue_bud.make_road(swim_road, street_text))

    assert len(swim_idea._awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    assert street_idea._awardlinks in (None, {})
    assert len(street_idea._awardheirs) == 3

    print(f"{len(idea_dict)}")
    print(f"{swim_idea._awardlinks}")
    print(f"{swim_idea._awardheirs}")
    print(f"{swim_idea._awardheirs}")
    assert len(sue_bud._idearoot._kids["swim"]._awardheirs) == 3


def test_BudUnit_set_awardlink_correctly_deletes_awardlinks():
    # ESTABLISH
    prom_text = "prom"
    x_bud = budunit_shop(prom_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    x_bud.add_acctunit(yao_text)
    x_bud.add_acctunit(zia_text)
    x_bud.add_acctunit(Xio_text)

    swim_text = "swim"
    swim_road = x_bud.make_road(prom_text, swim_text)

    x_bud.set_l1_idea(ideaunit_shop(swim_text))
    awardlink_yao = awardlink_shop(yao_text, give_force=10)
    awardlink_zia = awardlink_shop(zia_text, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_text, give_force=10)

    swim_idea = x_bud.get_idea_obj(swim_road)
    x_bud.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    x_bud.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    x_bud.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    assert len(swim_idea._awardlinks) == 3
    assert len(x_bud._idearoot._kids[swim_text]._awardlinks) == 3

    # WHEN
    x_bud.edit_idea_attr(swim_road, awardlink_del=yao_text)

    # THEN
    swim_idea = x_bud.get_idea_obj(swim_road)
    print(f"{swim_idea._label=}")
    print(f"{swim_idea._awardlinks=}")
    print(f"{swim_idea._awardheirs=}")

    assert len(x_bud._idearoot._kids[swim_text]._awardlinks) == 2


def test_BudUnit__get_filtered_awardlinks_idea_CorrectlyFiltersIdea_awardlinks():
    # ESTABLISH
    bob_text = "Bob"
    x1_bud = budunit_shop(bob_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_bud.add_acctunit(xia_text)
    x1_bud.add_acctunit(zoa_text)

    casa_text = "casa"
    casa_road = x1_bud.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_bud.make_l1_road(swim_text)
    x1_bud.set_l1_idea(ideaunit_shop(casa_text))
    x1_bud.set_l1_idea(ideaunit_shop(swim_text))
    x1_bud.edit_idea_attr(swim_road, awardlink=awardlink_shop(xia_text))
    x1_bud.edit_idea_attr(swim_road, awardlink=awardlink_shop(zoa_text))
    x1_bud_swim_idea = x1_bud.get_idea_obj(swim_road)
    assert len(x1_bud_swim_idea._awardlinks) == 2
    x_bud = budunit_shop(bob_text)
    x_bud.add_acctunit(xia_text)

    # WHEN
    filtered_idea = x_bud._get_filtered_awardlinks_idea(x1_bud_swim_idea)

    # THEN
    assert len(filtered_idea._awardlinks) == 1
    assert list(filtered_idea._awardlinks.keys()) == [xia_text]


def test_BudUnit_set_idea_CorrectlyFiltersIdea_awardlinks():
    # ESTABLISH
    bob_text = "Bob"
    x1_bud = budunit_shop(bob_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_bud.add_acctunit(xia_text)
    x1_bud.add_acctunit(zoa_text)

    casa_text = "casa"
    casa_road = x1_bud.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_bud.make_l1_road(swim_text)
    x1_bud.set_l1_idea(ideaunit_shop(casa_text))
    x1_bud.set_l1_idea(ideaunit_shop(swim_text))
    x1_bud.edit_idea_attr(swim_road, awardlink=awardlink_shop(xia_text))
    x1_bud.edit_idea_attr(swim_road, awardlink=awardlink_shop(zoa_text))
    x1_bud_swim_idea = x1_bud.get_idea_obj(swim_road)
    assert len(x1_bud_swim_idea._awardlinks) == 2

    # WHEN
    x_bud = budunit_shop(bob_text)
    x_bud.add_acctunit(xia_text)
    x_bud.set_l1_idea(x1_bud_swim_idea, create_missing_ideas=False)

    # THEN
    x_bud_swim_idea = x_bud.get_idea_obj(swim_road)
    assert len(x_bud_swim_idea._awardlinks) == 1
    assert list(x_bud_swim_idea._awardlinks.keys()) == [xia_text]


def test_BudUnit_get_idea_obj_ReturnsIdea():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels()
    nation_text = "nation-state"
    nation_road = x_bud.make_l1_road(nation_text)
    brazil_text = "Brazil"
    brazil_road = x_bud.make_road(nation_road, brazil_text)

    # WHEN
    brazil_idea = x_bud.get_idea_obj(road=brazil_road)

    # THEN
    assert brazil_idea is not None
    assert brazil_idea._label == brazil_text

    # WHEN
    week_text = "weekdays"
    week_road = x_bud.make_l1_road(week_text)
    week_idea = x_bud.get_idea_obj(road=week_road)

    # THEN
    assert week_idea is not None
    assert week_idea._label == week_text

    # WHEN
    root_idea = x_bud.get_idea_obj(road=x_bud._real_id)

    # THEN
    assert root_idea is not None
    assert root_idea._label == x_bud._real_id

    # WHEN / THEN
    bobdylan_text = "bobdylan"
    wrong_road = x_bud.make_l1_road(bobdylan_text)
    with pytest_raises(Exception) as excinfo:
        x_bud.get_idea_obj(road=wrong_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{wrong_road}'"


def test_BudUnit_idea_exists_ReturnsCorrectBool():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    sue_bud.settle_bud()
    cat_road = sue_bud.make_l1_road("cat have dinner")
    week_road = sue_bud.make_l1_road("weekdays")
    casa_road = sue_bud.make_l1_road("casa")
    nation_road = sue_bud.make_l1_road("nation-state")
    sun_road = sue_bud.make_road(week_road, "Sunday")
    mon_road = sue_bud.make_road(week_road, "Monday")
    tue_road = sue_bud.make_road(week_road, "Tuesday")
    wed_road = sue_bud.make_road(week_road, "Wednesday")
    thu_road = sue_bud.make_road(week_road, "Thursday")
    fri_road = sue_bud.make_road(week_road, "Friday")
    sat_road = sue_bud.make_road(week_road, "Saturday")
    france_road = sue_bud.make_road(nation_road, "France")
    brazil_road = sue_bud.make_road(nation_road, "Brazil")
    usa_road = sue_bud.make_road(nation_road, "USA")
    texas_road = sue_bud.make_road(usa_road, "Texas")
    oregon_road = sue_bud.make_road(usa_road, "Oregon")
    # do not exist in bud
    sports_road = sue_bud.make_l1_road("sports")
    swim_road = sue_bud.make_road(sports_road, "swimming")
    idaho_road = sue_bud.make_road(usa_road, "Idaho")
    japan_road = sue_bud.make_road(nation_road, "Japan")

    # WHEN/THEN
    assert sue_bud.idea_exists("") is False
    assert sue_bud.idea_exists(None) is False
    assert sue_bud.idea_exists(sue_bud._real_id)
    assert sue_bud.idea_exists(cat_road)
    assert sue_bud.idea_exists(week_road)
    assert sue_bud.idea_exists(casa_road)
    assert sue_bud.idea_exists(nation_road)
    assert sue_bud.idea_exists(sun_road)
    assert sue_bud.idea_exists(mon_road)
    assert sue_bud.idea_exists(tue_road)
    assert sue_bud.idea_exists(wed_road)
    assert sue_bud.idea_exists(thu_road)
    assert sue_bud.idea_exists(fri_road)
    assert sue_bud.idea_exists(sat_road)
    assert sue_bud.idea_exists(usa_road)
    assert sue_bud.idea_exists(france_road)
    assert sue_bud.idea_exists(brazil_road)
    assert sue_bud.idea_exists(texas_road)
    assert sue_bud.idea_exists(oregon_road)
    assert sue_bud.idea_exists("B") is False
    assert sue_bud.idea_exists(sports_road) is False
    assert sue_bud.idea_exists(swim_road) is False
    assert sue_bud.idea_exists(idaho_road) is False
    assert sue_bud.idea_exists(japan_road) is False


def test_BudUnit_set_offtrack_fund_ReturnsObj():
    # ESTABLISH
    bob_budunit = budunit_shop("Bob")
    assert not bob_budunit._offtrack_fund

    # WHEN
    bob_budunit.set_offtrack_fund() == 0

    # THEN
    assert bob_budunit._offtrack_fund == 0

    # ESTABLISH
    casa_text = "casa"
    week_text = "week"
    wed_text = "Wednesday"
    casa_road = bob_budunit.make_l1_road(casa_text)
    week_road = bob_budunit.make_l1_road(week_text)
    wed_road = bob_budunit.make_road(week_road, wed_text)
    casa_idea = ideaunit_shop(casa_text, _fund_onset=70, _fund_cease=170)
    week_idea = ideaunit_shop(week_text, _fund_onset=70, _fund_cease=75)
    wed_idea = ideaunit_shop(wed_text, _fund_onset=72, _fund_cease=75)
    casa_idea._parent_road = bob_budunit._real_id
    week_idea._parent_road = bob_budunit._real_id
    wed_idea._parent_road = week_road
    bob_budunit.set_l1_idea(casa_idea)
    bob_budunit.set_l1_idea(week_idea)
    bob_budunit.set_idea(wed_idea, week_road)
    bob_budunit._offtrack_kids_mass_set.add(casa_road)
    bob_budunit._offtrack_kids_mass_set.add(week_road)
    assert bob_budunit._offtrack_fund == 0

    # WHEN
    bob_budunit.set_offtrack_fund()

    # THEN
    assert bob_budunit._offtrack_fund == 105

    # WHEN
    bob_budunit._offtrack_kids_mass_set.add(wed_road)
    bob_budunit.set_offtrack_fund()

    # THEN
    assert bob_budunit._offtrack_fund == 108


def test_BudUnit_allot_offtrack_fund_SetsCharUnit_fund_take_fund_give():
    # ESTABLISH
    bob_text = "Bob"
    yao_text = "Yao"
    sue_text = "Sue"
    bob_budunit = budunit_shop(bob_text)
    bob_budunit.add_acctunit(bob_text)
    bob_budunit.add_acctunit(yao_text, credit_score=2)
    bob_budunit.add_acctunit(sue_text, debtit_score=2)
    bob_budunit.set_offtrack_fund()
    assert bob_budunit._offtrack_fund == 0

    # WHEN
    bob_budunit._allot_offtrack_fund()

    # THEN
    assert bob_budunit.get_acct(bob_text)._fund_give == 0
    assert bob_budunit.get_acct(bob_text)._fund_take == 0
    assert bob_budunit.get_acct(yao_text)._fund_give == 0
    assert bob_budunit.get_acct(yao_text)._fund_take == 0
    assert bob_budunit.get_acct(sue_text)._fund_give == 0
    assert bob_budunit.get_acct(sue_text)._fund_take == 0

    # WHEN
    casa_text = "casa"
    week_text = "week"
    wed_text = "Wednesday"
    casa_road = bob_budunit.make_l1_road(casa_text)
    week_road = bob_budunit.make_l1_road(week_text)
    wed_road = bob_budunit.make_road(week_road, wed_text)
    casa_idea = ideaunit_shop(casa_text, _fund_onset=70, _fund_cease=170)
    week_idea = ideaunit_shop(week_text, _fund_onset=70, _fund_cease=75)
    wed_idea = ideaunit_shop(wed_text, _fund_onset=72, _fund_cease=75)
    casa_idea._parent_road = bob_budunit._real_id
    week_idea._parent_road = bob_budunit._real_id
    wed_idea._parent_road = week_road
    bob_budunit.set_l1_idea(casa_idea)
    bob_budunit.set_l1_idea(week_idea)
    bob_budunit.set_idea(wed_idea, week_road)
    bob_budunit._offtrack_kids_mass_set.add(casa_road)
    bob_budunit._offtrack_kids_mass_set.add(week_road)
    bob_budunit.set_offtrack_fund()
    assert bob_budunit._offtrack_fund == 105

    # WHEN
    bob_budunit._allot_offtrack_fund()

    # THEN
    assert bob_budunit.get_acct(bob_text)._fund_give == 26
    assert bob_budunit.get_acct(bob_text)._fund_take == 26
    assert bob_budunit.get_acct(yao_text)._fund_give == 53
    assert bob_budunit.get_acct(yao_text)._fund_take == 26
    assert bob_budunit.get_acct(sue_text)._fund_give == 26
    assert bob_budunit.get_acct(sue_text)._fund_take == 53

    bob_budunit._offtrack_kids_mass_set.add(wed_road)
    bob_budunit.set_offtrack_fund()

    # THEN
    assert bob_budunit._offtrack_fund == 108
