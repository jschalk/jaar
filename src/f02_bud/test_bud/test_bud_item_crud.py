from src.f01_road.road import default_bridge_if_None
from src.f02_bud.healer import healerlink_shop
from src.f02_bud.examples.example_buds import get_budunit_with_4_levels
from src.f02_bud.group import awardlink_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.reason_item import reasonunit_shop, factunit_shop
from src.f02_bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_set_item_RaisesErrorWhen_parent_road_IsInvalid():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    invalid_rootidea_swim_road = "swimming"
    assert invalid_rootidea_swim_road != zia_bud.cmty_idea
    casa_str = "casa"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_item(
            itemunit_shop(casa_str), parent_road=invalid_rootidea_swim_road
        )
    assert (
        str(excinfo.value)
        == f"set_item failed because parent_road '{invalid_rootidea_swim_road}' has an invalid root idea"
    )


def test_BudUnit_set_item_RaisesErrorWhen_parent_road_ItemDoesNotExist():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_road = zia_bud.make_l1_road("swimming")
    casa_str = "casa"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_item(
            itemunit_shop(casa_str),
            parent_road=swim_road,
            create_missing_ancestors=False,
        )
    assert (
        str(excinfo.value)
        == f"set_item failed because '{swim_road}' item does not exist."
    )


def test_BudUnit_set_item_RaisesErrorWhen_item_idee_IsNotIdea():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_road = zia_bud.make_l1_road("swimming")
    casa_str = "casa"
    casa_road = zia_bud.make_l1_road(casa_str)
    run_str = "run"
    run_road = zia_bud.make_road(casa_road, run_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_item(itemunit_shop(run_road), parent_road=swim_road)
    assert (
        str(excinfo.value) == f"set_item failed because '{run_road}' is not a IdeaUnit."
    )


def test_BudUnit_set_item_CorrectlySetsAttr():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    assert not zia_bud.itemroot._kids.get(casa_str)

    # WHEN
    zia_bud.set_item(itemunit_shop(casa_str), parent_road=zia_bud.cmty_idea)

    # THEN
    print(f"{zia_bud.itemroot._kids.keys()=}")
    assert zia_bud.itemroot._kids.get(casa_str)


def test_BudUnit_item_exists_ReturnsObj():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_road = zia_bud.make_l1_road(casa_str)
    assert zia_bud.item_exists(casa_road) is False

    # WHEN
    zia_bud.set_item(itemunit_shop(casa_str), parent_road=zia_bud.cmty_idea)

    # THEN
    assert zia_bud.item_exists(casa_road)


def test_BudUnit_set_l1_item_CorrectlySetsAttr():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_road = zia_bud.make_l1_road(casa_str)
    assert not zia_bud.itemroot._kids.get(casa_road)

    # WHEN
    zia_bud.set_l1_item(itemunit_shop(casa_str))

    # THEN
    assert not zia_bud.itemroot._kids.get(casa_road)


def test_BudUnit_add_item_SetsAttr_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    slash_str = "/"
    bob_budunit = budunit_shop(bob_str, bridge=slash_str)
    casa_road = bob_budunit.make_l1_road("casa")
    assert not bob_budunit.item_exists(casa_road)

    # WHEN
    bob_budunit.add_item(casa_road)

    # THEN
    assert bob_budunit.item_exists(casa_road)
    casa_itemunit = bob_budunit.get_item_obj(casa_road)
    assert casa_itemunit._bridge == bob_budunit.bridge
    assert not casa_itemunit.pledge


def test_BudUnit_add_item_SetsAttr_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    bob_budunit = budunit_shop(bob_str)
    casa_road = bob_budunit.make_l1_road("casa")
    casa_mass = 13
    casa_pledge = True

    # WHEN
    bob_budunit.add_item(casa_road, mass=casa_mass, pledge=casa_pledge)

    # THEN
    casa_itemunit = bob_budunit.get_item_obj(casa_road)
    assert casa_itemunit.mass == casa_mass
    assert casa_itemunit.pledge


def test_BudUnit_add_item_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_budunit = budunit_shop(bob_str)
    casa_road = bob_budunit.make_l1_road("casa")
    casa_mass = 13

    # WHEN
    casa_itemunit = bob_budunit.add_item(casa_road, mass=casa_mass)

    # THEN
    assert casa_itemunit._item_idee == "casa"
    assert casa_itemunit.mass == casa_mass


def test_BudUnit_set_item_CorrectlyAddsItemObjWithNonstandard_bridge():
    # ESTABLISH
    slash_str = "/"
    assert slash_str != default_bridge_if_None()
    bob_bud = budunit_shop("Bob", bridge=slash_str)
    casa_str = "casa"
    week_str = "week"
    wed_str = "Wednesday"
    casa_road = bob_bud.make_l1_road(casa_str)
    week_road = bob_bud.make_l1_road(week_str)
    wed_road = bob_bud.make_road(week_road, wed_str)
    bob_bud.set_l1_item(itemunit_shop(casa_str))
    bob_bud.set_l1_item(itemunit_shop(week_str))
    bob_bud.set_item(itemunit_shop(wed_str), week_road)
    print(f"{bob_bud.itemroot._kids.keys()=}")
    assert len(bob_bud.itemroot._kids) == 2
    wed_item = bob_bud.get_item_obj(wed_road)
    assert wed_item._bridge == slash_str
    assert wed_item._bridge == bob_bud.bridge

    # WHEN
    bob_bud.edit_item_attr(casa_road, reason_base=week_road, reason_premise=wed_road)

    # THEN
    casa_item = bob_bud.get_item_obj(casa_road)
    assert casa_item.reasonunits.get(week_road) is not None


def test_BudUnit_set_item_CanCreateMissingItemUnits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    ww2_road = sue_bud.make_l1_road("ww2")
    battles_road = sue_bud.make_road(ww2_road, "battles")
    coralsea_road = sue_bud.make_road(battles_road, "coralsea")
    saratoga_item = itemunit_shop("USS Saratoga")
    assert sue_bud.item_exists(battles_road) is False
    assert sue_bud.item_exists(coralsea_road) is False

    # WHEN
    sue_bud.set_item(saratoga_item, parent_road=coralsea_road)

    # THEN
    assert sue_bud.item_exists(battles_road)
    assert sue_bud.item_exists(coralsea_road)


def test_BudUnit_del_item_obj_Level0CannotBeDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    root_road = sue_bud.cmty_idea

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.del_item_obj(road=root_road)
    assert str(excinfo.value) == "Itemroot cannot be deleted"


def test_BudUnit_del_item_obj_Level1CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    sun_str = "Sunday"
    sun_road = sue_bud.make_road(week_road, sun_str)
    assert sue_bud.get_item_obj(week_road)
    assert sue_bud.get_item_obj(sun_road)

    # WHEN
    sue_bud.del_item_obj(road=week_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(week_road)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{week_road}'"
    new_sunday_road = sue_bud.make_l1_road("Sunday")
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(new_sunday_road)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{new_sunday_road}'"


def test_BudUnit_del_item_obj_Level1CanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    sun_str = "Sunday"
    old_sunday_road = sue_bud.make_road(week_road, sun_str)
    assert sue_bud.get_item_obj(old_sunday_road)

    # WHEN
    sue_bud.del_item_obj(road=week_road, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(old_sunday_road)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{old_sunday_road}'"
    new_sunday_road = sue_bud.make_l1_road(sun_str)
    assert sue_bud.get_item_obj(new_sunday_road)
    new_sunday_item = sue_bud.get_item_obj(new_sunday_road)
    assert new_sunday_item._parent_road == sue_bud.cmty_idea


def test_BudUnit_del_item_obj_LevelNCanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    states_str = "nation-state"
    states_road = sue_bud.make_l1_road(states_str)
    usa_str = "USA"
    usa_road = sue_bud.make_road(states_road, usa_str)
    texas_str = "Texas"
    oregon_str = "Oregon"
    usa_texas_road = sue_bud.make_road(usa_road, texas_str)
    usa_oregon_road = sue_bud.make_road(usa_road, oregon_str)
    states_texas_road = sue_bud.make_road(states_road, texas_str)
    states_oregon_road = sue_bud.make_road(states_road, oregon_str)
    assert sue_bud.item_exists(usa_road)
    assert sue_bud.item_exists(usa_texas_road)
    assert sue_bud.item_exists(usa_oregon_road)
    assert sue_bud.item_exists(states_texas_road) is False
    assert sue_bud.item_exists(states_oregon_road) is False

    # WHEN
    sue_bud.del_item_obj(road=usa_road, del_children=False)

    # THEN
    assert sue_bud.item_exists(states_texas_road)
    assert sue_bud.item_exists(states_oregon_road)
    assert sue_bud.item_exists(usa_texas_road) is False
    assert sue_bud.item_exists(usa_oregon_road) is False
    assert sue_bud.item_exists(usa_road) is False


def test_BudUnit_del_item_obj_Level2CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    wkday_road = sue_bud.make_l1_road("weekdays")
    monday_road = sue_bud.make_road(wkday_road, "Monday")
    assert sue_bud.get_item_obj(monday_road)

    # WHEN
    sue_bud.del_item_obj(road=monday_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(monday_road)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{monday_road}'"


def test_BudUnit_del_item_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    states_str = "nation-state"
    states_road = sue_bud.make_l1_road(states_str)
    usa_str = "USA"
    usa_road = sue_bud.make_road(states_road, usa_str)
    texas_str = "Texas"
    usa_texas_road = sue_bud.make_road(usa_road, texas_str)
    assert sue_bud.get_item_obj(usa_texas_road)

    # WHEN
    sue_bud.del_item_obj(road=usa_texas_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(usa_texas_road)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{usa_texas_road}'"


def test_BudUnit_edit_item_attr_IsAbleToEditAnyAncestor_Item():
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    print(f"{casa_road=}")
    old_mass = sue_bud.itemroot._kids[casa_str].mass
    assert old_mass == 30
    sue_bud.edit_item_attr(road=casa_road, mass=23)
    new_mass = sue_bud.itemroot._kids[casa_str].mass
    assert new_mass == 23

    # uid: int = None,
    sue_bud.itemroot._kids[casa_str]._uid = 34
    x_uid = sue_bud.itemroot._kids[casa_str]._uid
    assert x_uid == 34
    sue_bud.edit_item_attr(road=casa_road, uid=23)
    uid_new = sue_bud.itemroot._kids[casa_str]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    sue_bud.itemroot._kids[casa_str].begin = 39
    x_begin = sue_bud.itemroot._kids[casa_str].begin
    assert x_begin == 39
    sue_bud.itemroot._kids[casa_str].close = 43
    x_close = sue_bud.itemroot._kids[casa_str].close
    assert x_close == 43
    sue_bud.edit_item_attr(road=casa_road, begin=25, close=29)
    assert sue_bud.itemroot._kids[casa_str].begin == 25
    assert sue_bud.itemroot._kids[casa_str].close == 29

    # gogo_want: float = None,
    # stop_want: float = None,
    sue_bud.itemroot._kids[casa_str].gogo_want = 439
    x_gogo_want = sue_bud.itemroot._kids[casa_str].gogo_want
    assert x_gogo_want == 439
    sue_bud.itemroot._kids[casa_str].stop_want = 443
    x_stop_want = sue_bud.itemroot._kids[casa_str].stop_want
    assert x_stop_want == 443
    sue_bud.edit_item_attr(road=casa_road, gogo_want=425, stop_want=429)
    assert sue_bud.itemroot._kids[casa_str].gogo_want == 425
    assert sue_bud.itemroot._kids[casa_str].stop_want == 429

    # factunit: factunit_shop = None,
    # sue_bud.itemroot._kids[casa_str].factunits = None
    assert sue_bud.itemroot._kids[casa_str].factunits == {}
    wkdays_road = sue_bud.make_l1_road("weekdays")
    fact_road = sue_bud.make_road(wkdays_road, "Sunday")
    factunit_x = factunit_shop(base=fact_road, pick=fact_road)

    casa_factunits = sue_bud.itemroot._kids[casa_str].factunits
    print(f"{casa_factunits=}")
    sue_bud.edit_item_attr(road=casa_road, factunit=factunit_x)
    casa_factunits = sue_bud.itemroot._kids[casa_str].factunits
    print(f"{casa_factunits=}")
    assert sue_bud.itemroot._kids[casa_str].factunits == {factunit_x.base: factunit_x}

    # _descendant_pledge_count: int = None,
    sue_bud.itemroot._kids[casa_str]._descendant_pledge_count = 81
    x_descendant_pledge_count = sue_bud.itemroot._kids[
        casa_str
    ]._descendant_pledge_count
    assert x_descendant_pledge_count == 81
    sue_bud.edit_item_attr(road=casa_road, descendant_pledge_count=67)
    _descendant_pledge_count_new = sue_bud.itemroot._kids[
        casa_str
    ]._descendant_pledge_count
    assert _descendant_pledge_count_new == 67

    # _all_acct_cred: bool = None,
    sue_bud.itemroot._kids[casa_str]._all_acct_cred = 74
    x_all_acct_cred = sue_bud.itemroot._kids[casa_str]._all_acct_cred
    assert x_all_acct_cred == 74
    sue_bud.edit_item_attr(road=casa_road, all_acct_cred=59)
    _all_acct_cred_new = sue_bud.itemroot._kids[casa_str]._all_acct_cred
    assert _all_acct_cred_new == 59

    # _all_acct_debt: bool = None,
    sue_bud.itemroot._kids[casa_str]._all_acct_debt = 74
    x_all_acct_debt = sue_bud.itemroot._kids[casa_str]._all_acct_debt
    assert x_all_acct_debt == 74
    sue_bud.edit_item_attr(road=casa_road, all_acct_debt=59)
    _all_acct_debt_new = sue_bud.itemroot._kids[casa_str]._all_acct_debt
    assert _all_acct_debt_new == 59

    # _awardlink: dict = None,
    sue_bud.itemroot._kids[casa_str].awardlinks = {
        "fun": awardlink_shop(awardee_label="fun", give_force=1, take_force=7)
    }
    _awardlinks = sue_bud.itemroot._kids[casa_str].awardlinks
    assert _awardlinks == {
        "fun": awardlink_shop(awardee_label="fun", give_force=1, take_force=7)
    }
    x_awardlink = awardlink_shop(awardee_label="fun", give_force=4, take_force=8)
    sue_bud.edit_item_attr(road=casa_road, awardlink=x_awardlink)
    assert sue_bud.itemroot._kids[casa_str].awardlinks == {"fun": x_awardlink}

    # _is_expanded: dict = None,
    sue_bud.itemroot._kids[casa_str]._is_expanded = "what"
    _is_expanded = sue_bud.itemroot._kids[casa_str]._is_expanded
    assert _is_expanded == "what"
    sue_bud.edit_item_attr(road=casa_road, is_expanded=True)
    assert sue_bud.itemroot._kids[casa_str]._is_expanded is True

    # pledge: dict = None,
    sue_bud.itemroot._kids[casa_str].pledge = "funfun3"
    pledge = sue_bud.itemroot._kids[casa_str].pledge
    assert pledge == "funfun3"
    sue_bud.edit_item_attr(road=casa_road, pledge=True)
    assert sue_bud.itemroot._kids[casa_str].pledge is True

    # _healerlink:
    sue_bud.itemroot._kids[casa_str].healerlink = "fun3rol"
    src_healerlink = sue_bud.itemroot._kids[casa_str].healerlink
    assert src_healerlink == "fun3rol"
    sue_str = "Sue"
    yao_str = "Yao"
    x_healerlink = healerlink_shop({sue_str, yao_str})
    sue_bud.add_acctunit(sue_str)
    sue_bud.add_acctunit(yao_str)
    sue_bud.edit_item_attr(road=casa_road, healerlink=x_healerlink)
    assert sue_bud.itemroot._kids[casa_str].healerlink == x_healerlink

    # _problem_bool: bool
    sue_bud.itemroot._kids[casa_str].problem_bool = "fun3rol"
    src_problem_bool = sue_bud.itemroot._kids[casa_str].problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True
    sue_bud.edit_item_attr(road=casa_road, problem_bool=x_problem_bool)
    assert sue_bud.itemroot._kids[casa_str].problem_bool == x_problem_bool


def test_BudUnit_edit_item_attr_RaisesErrorWhen_healerlink_healer_names_DoNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    casa_str = "casa"
    casa_road = yao_bud.make_l1_road(casa_str)
    yao_bud.set_l1_item(itemunit_shop(casa_str))
    day_str = "day_range"
    day_item = itemunit_shop(day_str, begin=44, close=110)
    day_road = yao_bud.make_l1_road(day_str)
    yao_bud.set_l1_item(day_item)

    casa_item = yao_bud.get_item_obj(casa_road)
    assert casa_item.begin is None
    assert casa_item.close is None

    # WHEN / THEN
    sue_str = "Sue"
    x_healerlink = healerlink_shop({sue_str})
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_item_attr(road=casa_road, healerlink=x_healerlink)
    assert (
        str(excinfo.value)
        == f"Item cannot edit healerlink because group_label '{sue_str}' does not exist as group in Bud"
    )


def test_BudUnit_set_item_MustReorderKidsDictToBeAlphabetical():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    casa_str = "casa"
    bob_bud.set_l1_item(itemunit_shop(casa_str))
    swim_str = "swim"
    bob_bud.set_l1_item(itemunit_shop(swim_str))

    # WHEN
    item_list = list(bob_bud.itemroot._kids.values())

    # THEN
    assert item_list[0]._item_idee == casa_str


def test_BudUnit_set_item_adoptee_RaisesErrorIfAdopteeItemDoesNotHaveCorrectParent():
    bob_bud = budunit_shop("Bob")
    sports_str = "sports"
    sports_road = bob_bud.make_l1_road(sports_str)
    bob_bud.set_l1_item(itemunit_shop(sports_str))
    swim_str = "swim"
    bob_bud.set_item(itemunit_shop(swim_str), parent_road=sports_road)

    # WHEN / THEN
    summer_str = "summer"
    hike_str = "hike"
    hike_road = bob_bud.make_road(sports_road, hike_str)
    with pytest_raises(Exception) as excinfo:
        bob_bud.set_item(
            item_kid=itemunit_shop(summer_str),
            parent_road=sports_road,
            adoptees=[swim_str, hike_str],
        )
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{hike_road}'"


def test_BudUnit_set_item_adoptee_CorrectlyAddsAdoptee():
    bob_bud = budunit_shop("Bob")
    sports_str = "sports"
    sports_road = bob_bud.make_l1_road(sports_str)
    bob_bud.set_l1_item(itemunit_shop(sports_str))
    swim_str = "swim"
    bob_bud.set_item(itemunit_shop(swim_str), parent_road=sports_road)
    hike_str = "hike"
    bob_bud.set_item(itemunit_shop(hike_str), parent_road=sports_road)

    sports_swim_road = bob_bud.make_road(sports_road, swim_str)
    sports_hike_road = bob_bud.make_road(sports_road, hike_str)
    assert bob_bud.item_exists(sports_swim_road)
    assert bob_bud.item_exists(sports_hike_road)
    summer_str = "summer"
    summer_road = bob_bud.make_road(sports_road, summer_str)
    summer_swim_road = bob_bud.make_road(summer_road, swim_str)
    summer_hike_road = bob_bud.make_road(summer_road, hike_str)
    assert bob_bud.item_exists(summer_swim_road) is False
    assert bob_bud.item_exists(summer_hike_road) is False

    # WHEN / THEN
    bob_bud.set_item(
        item_kid=itemunit_shop(summer_str),
        parent_road=sports_road,
        adoptees=[swim_str, hike_str],
    )

    # THEN
    summer_item = bob_bud.get_item_obj(summer_road)
    print(f"{summer_item._kids.keys()=}")
    assert bob_bud.item_exists(summer_swim_road)
    assert bob_bud.item_exists(summer_hike_road)
    assert bob_bud.item_exists(sports_swim_road) is False
    assert bob_bud.item_exists(sports_hike_road) is False


def test_BudUnit_set_item_bundling_SetsNewParentWithMassEqualToSumOfAdoptedItems():
    bob_bud = budunit_shop("Bob")
    sports_str = "sports"
    sports_road = bob_bud.make_l1_road(sports_str)
    bob_bud.set_l1_item(itemunit_shop(sports_str, mass=2))
    swim_str = "swim"
    swim_mass = 3
    bob_bud.set_item(itemunit_shop(swim_str, mass=swim_mass), sports_road)
    hike_str = "hike"
    hike_mass = 5
    bob_bud.set_item(itemunit_shop(hike_str, mass=hike_mass), sports_road)
    bball_str = "bball"
    bball_mass = 7
    bob_bud.set_item(itemunit_shop(bball_str, mass=bball_mass), sports_road)

    sports_swim_road = bob_bud.make_road(sports_road, swim_str)
    sports_hike_road = bob_bud.make_road(sports_road, hike_str)
    sports_bball_road = bob_bud.make_road(sports_road, bball_str)
    assert bob_bud.get_item_obj(sports_swim_road).mass == swim_mass
    assert bob_bud.get_item_obj(sports_hike_road).mass == hike_mass
    assert bob_bud.get_item_obj(sports_bball_road).mass == bball_mass
    summer_str = "summer"
    summer_road = bob_bud.make_road(sports_road, summer_str)
    summer_swim_road = bob_bud.make_road(summer_road, swim_str)
    summer_hike_road = bob_bud.make_road(summer_road, hike_str)
    summer_bball_road = bob_bud.make_road(summer_road, bball_str)
    assert bob_bud.item_exists(summer_swim_road) is False
    assert bob_bud.item_exists(summer_hike_road) is False
    assert bob_bud.item_exists(summer_bball_road) is False

    # WHEN / THEN
    bob_bud.set_item(
        item_kid=itemunit_shop(summer_str),
        parent_road=sports_road,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )

    # THEN
    assert bob_bud.get_item_obj(summer_road).mass == swim_mass + hike_mass
    assert bob_bud.get_item_obj(summer_swim_road).mass == swim_mass
    assert bob_bud.get_item_obj(summer_hike_road).mass == hike_mass
    assert bob_bud.item_exists(summer_bball_road) is False
    assert bob_bud.item_exists(sports_swim_road) is False
    assert bob_bud.item_exists(sports_hike_road) is False
    assert bob_bud.item_exists(sports_bball_road)


def test_BudUnit_del_item_obj_DeletingBundledItemReturnsItemsToOriginalState():
    bob_bud = budunit_shop("Bob")
    sports_str = "sports"
    sports_road = bob_bud.make_l1_road(sports_str)
    bob_bud.set_l1_item(itemunit_shop(sports_str, mass=2))
    swim_str = "swim"
    swim_mass = 3
    bob_bud.set_item(itemunit_shop(swim_str, mass=swim_mass), sports_road)
    hike_str = "hike"
    hike_mass = 5
    bob_bud.set_item(itemunit_shop(hike_str, mass=hike_mass), sports_road)
    bball_str = "bball"
    bball_mass = 7
    bob_bud.set_item(itemunit_shop(bball_str, mass=bball_mass), sports_road)

    sports_swim_road = bob_bud.make_road(sports_road, swim_str)
    sports_hike_road = bob_bud.make_road(sports_road, hike_str)
    sports_bball_road = bob_bud.make_road(sports_road, bball_str)
    assert bob_bud.get_item_obj(sports_swim_road).mass == swim_mass
    assert bob_bud.get_item_obj(sports_hike_road).mass == hike_mass
    assert bob_bud.get_item_obj(sports_bball_road).mass == bball_mass
    summer_str = "summer"
    summer_road = bob_bud.make_road(sports_road, summer_str)
    summer_swim_road = bob_bud.make_road(summer_road, swim_str)
    summer_hike_road = bob_bud.make_road(summer_road, hike_str)
    summer_bball_road = bob_bud.make_road(summer_road, bball_str)
    assert bob_bud.item_exists(summer_swim_road) is False
    assert bob_bud.item_exists(summer_hike_road) is False
    assert bob_bud.item_exists(summer_bball_road) is False
    bob_bud.set_item(
        item_kid=itemunit_shop(summer_str),
        parent_road=sports_road,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )
    assert bob_bud.get_item_obj(summer_road).mass == swim_mass + hike_mass
    assert bob_bud.get_item_obj(summer_swim_road).mass == swim_mass
    assert bob_bud.get_item_obj(summer_hike_road).mass == hike_mass
    assert bob_bud.item_exists(summer_bball_road) is False
    assert bob_bud.item_exists(sports_swim_road) is False
    assert bob_bud.item_exists(sports_hike_road) is False
    assert bob_bud.item_exists(sports_bball_road)
    print(f"{bob_bud._item_dict.keys()=}")

    # WHEN
    bob_bud.del_item_obj(road=summer_road, del_children=False)

    # THEN
    sports_swim_item = bob_bud.get_item_obj(sports_swim_road)
    sports_hike_item = bob_bud.get_item_obj(sports_hike_road)
    sports_bball_item = bob_bud.get_item_obj(sports_bball_road)
    assert sports_swim_item.mass == swim_mass
    assert sports_hike_item.mass == hike_mass
    assert sports_bball_item.mass == bball_mass


def test_BudUnit_edit_item_attr_DeletesItemUnit_awardlinks():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    yao_bud.add_acctunit(yao_str)
    yao_bud.add_acctunit(zia_str)
    yao_bud.add_acctunit(Xio_str)

    swim_str = "swim"
    swim_road = yao_bud.make_road(yao_str, swim_str)

    yao_bud.set_l1_item(itemunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_item = yao_bud.get_item_obj(swim_road)
    yao_bud.edit_item_attr(swim_road, awardlink=awardlink_yao)
    yao_bud.edit_item_attr(swim_road, awardlink=awardlink_zia)
    yao_bud.edit_item_attr(swim_road, awardlink=awardlink_Xio)

    assert len(swim_item.awardlinks) == 3
    assert len(yao_bud.itemroot._kids[swim_str].awardlinks) == 3

    # WHEN
    yao_bud.edit_item_attr(swim_road, awardlink_del=yao_str)

    # THEN
    swim_item = yao_bud.get_item_obj(swim_road)
    print(f"{swim_item._item_idee=}")
    print(f"{swim_item.awardlinks=}")
    print(f"{swim_item._awardheirs=}")

    assert len(yao_bud.itemroot._kids[swim_str].awardlinks) == 2


def test_BudUnit__get_cleaned_awardlinks_item_CorrectlyRemovesItem_awardlinks():
    # ESTABLISH
    bob_str = "Bob"
    x1_bud = budunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    x1_bud.add_acctunit(xia_str)
    x1_bud.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_road = x1_bud.make_l1_road(casa_str)
    swim_str = "swim"
    swim_road = x1_bud.make_l1_road(swim_str)
    x1_bud.set_l1_item(itemunit_shop(casa_str))
    x1_bud.set_l1_item(itemunit_shop(swim_str))
    x1_bud.edit_item_attr(swim_road, awardlink=awardlink_shop(xia_str))
    x1_bud.edit_item_attr(swim_road, awardlink=awardlink_shop(zoa_str))
    x1_bud_swim_item = x1_bud.get_item_obj(swim_road)
    assert len(x1_bud_swim_item.awardlinks) == 2
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(xia_str)

    # WHEN
    cleaned_item = bob_bud._get_cleaned_awardlinks_item(x1_bud_swim_item)

    # THEN
    assert len(cleaned_item.awardlinks) == 1
    assert list(cleaned_item.awardlinks.keys()) == [xia_str]


def test_BudUnit_set_item_CorrectlyCleansItem_awardlinks():
    # ESTABLISH
    bob_str = "Bob"
    x1_bud = budunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    x1_bud.add_acctunit(xia_str)
    x1_bud.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_road = x1_bud.make_l1_road(casa_str)
    swim_str = "swim"
    swim_road = x1_bud.make_l1_road(swim_str)
    x1_bud.set_l1_item(itemunit_shop(casa_str))
    x1_bud.set_l1_item(itemunit_shop(swim_str))
    x1_bud.edit_item_attr(swim_road, awardlink=awardlink_shop(xia_str))
    x1_bud.edit_item_attr(swim_road, awardlink=awardlink_shop(zoa_str))
    x1_bud_swim_item = x1_bud.get_item_obj(swim_road)
    assert len(x1_bud_swim_item.awardlinks) == 2

    # WHEN
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(xia_str)
    bob_bud.set_l1_item(x1_bud_swim_item, create_missing_items=False)

    # THEN
    bob_bud_swim_item = bob_bud.get_item_obj(swim_road)
    assert len(bob_bud_swim_item.awardlinks) == 1
    assert list(bob_bud_swim_item.awardlinks.keys()) == [xia_str]


def test_BudUnit_get_item_obj_ReturnsItem():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    nation_str = "nation-state"
    nation_road = sue_bud.make_l1_road(nation_str)
    brazil_str = "Brazil"
    brazil_road = sue_bud.make_road(nation_road, brazil_str)

    # WHEN
    brazil_item = sue_bud.get_item_obj(road=brazil_road)

    # THEN
    assert brazil_item is not None
    assert brazil_item._item_idee == brazil_str

    # WHEN
    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    week_item = sue_bud.get_item_obj(road=week_road)

    # THEN
    assert week_item is not None
    assert week_item._item_idee == week_str

    # WHEN
    root_item = sue_bud.get_item_obj(road=sue_bud.cmty_idea)

    # THEN
    assert root_item is not None
    assert root_item._item_idee == sue_bud.cmty_idea

    # WHEN / THEN
    bobdylan_str = "bobdylan"
    wrong_road = sue_bud.make_l1_road(bobdylan_str)
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(road=wrong_road)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{wrong_road}'"


def test_BudUnit_item_exists_ReturnsCorrectBool():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
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

    # WHEN / THEN
    assert sue_bud.item_exists("") is False
    assert sue_bud.item_exists(None) is False
    assert sue_bud.item_exists(sue_bud.cmty_idea)
    assert sue_bud.item_exists(cat_road)
    assert sue_bud.item_exists(week_road)
    assert sue_bud.item_exists(casa_road)
    assert sue_bud.item_exists(nation_road)
    assert sue_bud.item_exists(sun_road)
    assert sue_bud.item_exists(mon_road)
    assert sue_bud.item_exists(tue_road)
    assert sue_bud.item_exists(wed_road)
    assert sue_bud.item_exists(thu_road)
    assert sue_bud.item_exists(fri_road)
    assert sue_bud.item_exists(sat_road)
    assert sue_bud.item_exists(usa_road)
    assert sue_bud.item_exists(france_road)
    assert sue_bud.item_exists(brazil_road)
    assert sue_bud.item_exists(texas_road)
    assert sue_bud.item_exists(oregon_road)
    assert sue_bud.item_exists("B") is False
    assert sue_bud.item_exists(sports_road) is False
    assert sue_bud.item_exists(swim_road) is False
    assert sue_bud.item_exists(idaho_road) is False
    assert sue_bud.item_exists(japan_road) is False


def test_BudUnit_set_offtrack_fund_ReturnsObj():
    # ESTABLISH
    bob_budunit = budunit_shop("Bob")
    assert not bob_budunit._offtrack_fund

    # WHEN
    bob_budunit.set_offtrack_fund() == 0

    # THEN
    assert bob_budunit._offtrack_fund == 0

    # ESTABLISH
    casa_str = "casa"
    week_str = "week"
    wed_str = "Wednesday"
    casa_road = bob_budunit.make_l1_road(casa_str)
    week_road = bob_budunit.make_l1_road(week_str)
    wed_road = bob_budunit.make_road(week_road, wed_str)
    casa_item = itemunit_shop(casa_str, _fund_onset=70, _fund_cease=170)
    week_item = itemunit_shop(week_str, _fund_onset=70, _fund_cease=75)
    wed_item = itemunit_shop(wed_str, _fund_onset=72, _fund_cease=75)
    casa_item._parent_road = bob_budunit.cmty_idea
    week_item._parent_road = bob_budunit.cmty_idea
    wed_item._parent_road = week_road
    bob_budunit.set_l1_item(casa_item)
    bob_budunit.set_l1_item(week_item)
    bob_budunit.set_item(wed_item, week_road)
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
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    bob_budunit = budunit_shop(bob_str)
    bob_budunit.add_acctunit(bob_str)
    bob_budunit.add_acctunit(yao_str, credit_belief=2)
    bob_budunit.add_acctunit(sue_str, debtit_belief=2)
    bob_budunit.set_offtrack_fund()
    assert bob_budunit._offtrack_fund == 0

    # WHEN
    bob_budunit._allot_offtrack_fund()

    # THEN
    assert bob_budunit.get_acct(bob_str)._fund_give == 0
    assert bob_budunit.get_acct(bob_str)._fund_take == 0
    assert bob_budunit.get_acct(yao_str)._fund_give == 0
    assert bob_budunit.get_acct(yao_str)._fund_take == 0
    assert bob_budunit.get_acct(sue_str)._fund_give == 0
    assert bob_budunit.get_acct(sue_str)._fund_take == 0

    # WHEN
    casa_str = "casa"
    week_str = "week"
    wed_str = "Wednesday"
    casa_road = bob_budunit.make_l1_road(casa_str)
    week_road = bob_budunit.make_l1_road(week_str)
    wed_road = bob_budunit.make_road(week_road, wed_str)
    casa_item = itemunit_shop(casa_str, _fund_onset=70, _fund_cease=170)
    week_item = itemunit_shop(week_str, _fund_onset=70, _fund_cease=75)
    wed_item = itemunit_shop(wed_str, _fund_onset=72, _fund_cease=75)
    casa_item._parent_road = bob_budunit.cmty_idea
    week_item._parent_road = bob_budunit.cmty_idea
    wed_item._parent_road = week_road
    bob_budunit.set_l1_item(casa_item)
    bob_budunit.set_l1_item(week_item)
    bob_budunit.set_item(wed_item, week_road)
    bob_budunit._offtrack_kids_mass_set.add(casa_road)
    bob_budunit._offtrack_kids_mass_set.add(week_road)
    bob_budunit.set_offtrack_fund()
    assert bob_budunit._offtrack_fund == 105

    # WHEN
    bob_budunit._allot_offtrack_fund()

    # THEN
    assert bob_budunit.get_acct(bob_str)._fund_give == 26
    assert bob_budunit.get_acct(bob_str)._fund_take == 26
    assert bob_budunit.get_acct(yao_str)._fund_give == 53
    assert bob_budunit.get_acct(yao_str)._fund_take == 26
    assert bob_budunit.get_acct(sue_str)._fund_give == 26
    assert bob_budunit.get_acct(sue_str)._fund_take == 53

    bob_budunit._offtrack_kids_mass_set.add(wed_road)
    bob_budunit.set_offtrack_fund()

    # THEN
    assert bob_budunit._offtrack_fund == 108
