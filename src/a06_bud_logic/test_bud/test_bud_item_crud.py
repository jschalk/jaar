from src.a01_way_logic.way import default_bridge_if_None, create_way, to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_item import factunit_shop
from src.a05_item_logic.healer import healerlink_shop
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import get_budunit_with_4_levels
from pytest import raises as pytest_raises


def test_BudUnit_set_item_RaisesErrorWhen_parent_way_IsInvalid():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    invalid_roottag_swim_way = create_way("swimming")
    assert invalid_roottag_swim_way != zia_bud.fisc_tag
    casa_str = "casa"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_item(itemunit_shop(casa_str), parent_way=invalid_roottag_swim_way)
    exception_str = f"set_item failed because parent_way '{invalid_roottag_swim_way}' has an invalid root tag. Should be {zia_bud.fisc_tag}."
    assert str(excinfo.value) == exception_str


def test_BudUnit_set_item_RaisesErrorWhen_parent_way_ItemDoesNotExist():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_way = zia_bud.make_l1_way("swimming")
    casa_str = "casa"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_item(
            itemunit_shop(casa_str),
            parent_way=swim_way,
            create_missing_ancestors=False,
        )
    exception_str = f"set_item failed because '{swim_way}' item does not exist."
    assert str(excinfo.value) == exception_str


def test_BudUnit_set_item_RaisesErrorWhen_item_tag_IsNotTag():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_way = zia_bud.make_l1_way("swimming")
    casa_str = "casa"
    casa_way = zia_bud.make_l1_way(casa_str)
    run_str = "run"
    run_way = zia_bud.make_way(casa_way, run_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_item(itemunit_shop(run_way), parent_way=swim_way)
    exception_str = f"set_item failed because '{run_way}' is not a TagUnit."
    assert str(excinfo.value) == exception_str


def test_BudUnit_set_item_CorrectlySetsAttr():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    assert not zia_bud.itemroot._kids.get(casa_str)

    # WHEN
    zia_bud.set_item(itemunit_shop(casa_str), parent_way=to_way(zia_bud.fisc_tag))

    # THEN
    print(f"{zia_bud.itemroot._kids.keys()=}")
    assert zia_bud.itemroot._kids.get(casa_str)


def test_BudUnit_item_exists_ReturnsObj():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_way = zia_bud.make_l1_way(casa_str)
    assert zia_bud.item_exists(casa_way) is False

    # WHEN
    zia_bud.set_item(itemunit_shop(casa_str), parent_way=to_way(zia_bud.fisc_tag))

    # THEN
    assert zia_bud.item_exists(casa_way)


def test_BudUnit_set_l1_item_CorrectlySetsAttr():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_way = zia_bud.make_l1_way(casa_str)
    assert not zia_bud.itemroot._kids.get(casa_way)

    # WHEN
    zia_bud.set_l1_item(itemunit_shop(casa_str))

    # THEN
    assert not zia_bud.itemroot._kids.get(casa_way)


def test_BudUnit_add_item_SetsAttr_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    slash_str = "/"
    bob_budunit = budunit_shop(bob_str, bridge=slash_str)
    casa_way = bob_budunit.make_l1_way("casa")
    assert not bob_budunit.item_exists(casa_way)

    # WHEN
    bob_budunit.add_item(casa_way)

    # THEN
    assert bob_budunit.item_exists(casa_way)
    casa_itemunit = bob_budunit.get_item_obj(casa_way)
    assert casa_itemunit.bridge == bob_budunit.bridge
    assert not casa_itemunit.pledge


def test_BudUnit_add_item_SetsAttr_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    bob_budunit = budunit_shop(bob_str)
    casa_way = bob_budunit.make_l1_way("casa")
    casa_mass = 13
    casa_pledge = True

    # WHEN
    bob_budunit.add_item(casa_way, mass=casa_mass, pledge=casa_pledge)

    # THEN
    casa_itemunit = bob_budunit.get_item_obj(casa_way)
    assert casa_itemunit.mass == casa_mass
    assert casa_itemunit.pledge


def test_BudUnit_add_item_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_budunit = budunit_shop(bob_str)
    casa_way = bob_budunit.make_l1_way("casa")
    casa_mass = 13

    # WHEN
    casa_itemunit = bob_budunit.add_item(casa_way, mass=casa_mass)

    # THEN
    assert casa_itemunit.item_tag == "casa"
    assert casa_itemunit.mass == casa_mass


def test_BudUnit_set_item_CorrectlyAddsItemObjWithNonDefault_bridge():
    # ESTABLISH
    slash_str = "/"
    assert slash_str != default_bridge_if_None()
    bob_bud = budunit_shop("Bob", bridge=slash_str)
    casa_str = "casa"
    week_str = "week"
    wed_str = "Wednesday"
    casa_way = bob_bud.make_l1_way(casa_str)
    week_way = bob_bud.make_l1_way(week_str)
    wed_way = bob_bud.make_way(week_way, wed_str)
    bob_bud.set_l1_item(itemunit_shop(casa_str))
    bob_bud.set_l1_item(itemunit_shop(week_str))
    bob_bud.set_item(itemunit_shop(wed_str), week_way)
    print(f"{bob_bud.itemroot._kids.keys()=}")
    assert len(bob_bud.itemroot._kids) == 2
    wed_item = bob_bud.get_item_obj(wed_way)
    assert wed_item.bridge == slash_str
    assert wed_item.bridge == bob_bud.bridge

    # WHEN
    bob_bud.edit_item_attr(casa_way, reason_base=week_way, reason_premise=wed_way)

    # THEN
    casa_item = bob_bud.get_item_obj(casa_way)
    assert casa_item.reasonunits.get(week_way) is not None


def test_BudUnit_set_item_CanCreateMissingItemUnits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    ww2_way = sue_bud.make_l1_way("ww2")
    battles_way = sue_bud.make_way(ww2_way, "battles")
    coralsea_way = sue_bud.make_way(battles_way, "coralsea")
    saratoga_item = itemunit_shop("USS Saratoga")
    assert sue_bud.item_exists(battles_way) is False
    assert sue_bud.item_exists(coralsea_way) is False

    # WHEN
    sue_bud.set_item(saratoga_item, parent_way=coralsea_way)

    # THEN
    assert sue_bud.item_exists(battles_way)
    assert sue_bud.item_exists(coralsea_way)


def test_BudUnit_del_item_obj_Level0CannotBeDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    root_way = to_way(sue_bud.fisc_tag)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.del_item_obj(way=root_way)
    assert str(excinfo.value) == "Itemroot cannot be deleted"


def test_BudUnit_del_item_obj_Level1CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    sun_str = "Sunday"
    sun_way = sue_bud.make_way(week_way, sun_str)
    assert sue_bud.get_item_obj(week_way)
    assert sue_bud.get_item_obj(sun_way)

    # WHEN
    sue_bud.del_item_obj(way=week_way)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(week_way)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{week_way}'"
    new_sunday_way = sue_bud.make_l1_way("Sunday")
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(new_sunday_way)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{new_sunday_way}'"


def test_BudUnit_del_item_obj_Level1CanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    sun_str = "Sunday"
    old_sunday_way = sue_bud.make_way(week_way, sun_str)
    assert sue_bud.get_item_obj(old_sunday_way)

    # WHEN
    sue_bud.del_item_obj(way=week_way, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(old_sunday_way)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{old_sunday_way}'"
    new_sunday_way = sue_bud.make_l1_way(sun_str)
    assert sue_bud.get_item_obj(new_sunday_way)
    new_sunday_item = sue_bud.get_item_obj(new_sunday_way)
    assert new_sunday_item.parent_way == to_way(sue_bud.fisc_tag)


def test_BudUnit_del_item_obj_LevelNCanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    usa_str = "USA"
    usa_way = sue_bud.make_way(states_way, usa_str)
    texas_str = "Texas"
    oregon_str = "Oregon"
    usa_texas_way = sue_bud.make_way(usa_way, texas_str)
    usa_oregon_way = sue_bud.make_way(usa_way, oregon_str)
    states_texas_way = sue_bud.make_way(states_way, texas_str)
    states_oregon_way = sue_bud.make_way(states_way, oregon_str)
    assert sue_bud.item_exists(usa_way)
    assert sue_bud.item_exists(usa_texas_way)
    assert sue_bud.item_exists(usa_oregon_way)
    assert sue_bud.item_exists(states_texas_way) is False
    assert sue_bud.item_exists(states_oregon_way) is False

    # WHEN
    sue_bud.del_item_obj(way=usa_way, del_children=False)

    # THEN
    assert sue_bud.item_exists(states_texas_way)
    assert sue_bud.item_exists(states_oregon_way)
    assert sue_bud.item_exists(usa_texas_way) is False
    assert sue_bud.item_exists(usa_oregon_way) is False
    assert sue_bud.item_exists(usa_way) is False


def test_BudUnit_del_item_obj_Level2CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    wkday_way = sue_bud.make_l1_way("weekdays")
    monday_way = sue_bud.make_way(wkday_way, "Monday")
    assert sue_bud.get_item_obj(monday_way)

    # WHEN
    sue_bud.del_item_obj(way=monday_way)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(monday_way)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{monday_way}'"


def test_BudUnit_del_item_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    usa_str = "USA"
    usa_way = sue_bud.make_way(states_way, usa_str)
    texas_str = "Texas"
    usa_texas_way = sue_bud.make_way(usa_way, texas_str)
    assert sue_bud.get_item_obj(usa_texas_way)

    # WHEN
    sue_bud.del_item_obj(way=usa_texas_way)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(usa_texas_way)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{usa_texas_way}'"


def test_BudUnit_edit_item_attr_IsAbleToEditAnyAncestor_Item():
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    print(f"{casa_way=}")
    old_mass = sue_bud.itemroot._kids[casa_str].mass
    assert old_mass == 30
    sue_bud.edit_item_attr(way=casa_way, mass=23)
    new_mass = sue_bud.itemroot._kids[casa_str].mass
    assert new_mass == 23

    # uid: int = None,
    sue_bud.itemroot._kids[casa_str]._uid = 34
    x_uid = sue_bud.itemroot._kids[casa_str]._uid
    assert x_uid == 34
    sue_bud.edit_item_attr(way=casa_way, uid=23)
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
    sue_bud.edit_item_attr(way=casa_way, begin=25, close=29)
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
    sue_bud.edit_item_attr(way=casa_way, gogo_want=425, stop_want=429)
    assert sue_bud.itemroot._kids[casa_str].gogo_want == 425
    assert sue_bud.itemroot._kids[casa_str].stop_want == 429

    # factunit: factunit_shop = None,
    # sue_bud.itemroot._kids[casa_str].factunits = None
    assert sue_bud.itemroot._kids[casa_str].factunits == {}
    wkdays_way = sue_bud.make_l1_way("weekdays")
    fact_way = sue_bud.make_way(wkdays_way, "Sunday")
    x_factunit = factunit_shop(fbase=fact_way, fneed=fact_way)

    casa_factunits = sue_bud.itemroot._kids[casa_str].factunits
    print(f"{casa_factunits=}")
    sue_bud.edit_item_attr(way=casa_way, factunit=x_factunit)
    casa_factunits = sue_bud.itemroot._kids[casa_str].factunits
    print(f"{casa_factunits=}")
    assert sue_bud.itemroot._kids[casa_str].factunits == {x_factunit.fbase: x_factunit}

    # _descendant_pledge_count: int = None,
    sue_bud.itemroot._kids[casa_str]._descendant_pledge_count = 81
    x_descendant_pledge_count = sue_bud.itemroot._kids[
        casa_str
    ]._descendant_pledge_count
    assert x_descendant_pledge_count == 81
    sue_bud.edit_item_attr(way=casa_way, descendant_pledge_count=67)
    _descendant_pledge_count_new = sue_bud.itemroot._kids[
        casa_str
    ]._descendant_pledge_count
    assert _descendant_pledge_count_new == 67

    # _all_acct_cred: bool = None,
    sue_bud.itemroot._kids[casa_str]._all_acct_cred = 74
    x_all_acct_cred = sue_bud.itemroot._kids[casa_str]._all_acct_cred
    assert x_all_acct_cred == 74
    sue_bud.edit_item_attr(way=casa_way, all_acct_cred=59)
    _all_acct_cred_new = sue_bud.itemroot._kids[casa_str]._all_acct_cred
    assert _all_acct_cred_new == 59

    # _all_acct_debt: bool = None,
    sue_bud.itemroot._kids[casa_str]._all_acct_debt = 74
    x_all_acct_debt = sue_bud.itemroot._kids[casa_str]._all_acct_debt
    assert x_all_acct_debt == 74
    sue_bud.edit_item_attr(way=casa_way, all_acct_debt=59)
    _all_acct_debt_new = sue_bud.itemroot._kids[casa_str]._all_acct_debt
    assert _all_acct_debt_new == 59

    # _awardlink: dict = None,
    sue_bud.itemroot._kids[casa_str].awardlinks = {
        "fun": awardlink_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    _awardlinks = sue_bud.itemroot._kids[casa_str].awardlinks
    assert _awardlinks == {
        "fun": awardlink_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    x_awardlink = awardlink_shop(awardee_title="fun", give_force=4, take_force=8)
    sue_bud.edit_item_attr(way=casa_way, awardlink=x_awardlink)
    assert sue_bud.itemroot._kids[casa_str].awardlinks == {"fun": x_awardlink}

    # _is_expanded: dict = None,
    sue_bud.itemroot._kids[casa_str]._is_expanded = "what"
    _is_expanded = sue_bud.itemroot._kids[casa_str]._is_expanded
    assert _is_expanded == "what"
    sue_bud.edit_item_attr(way=casa_way, is_expanded=True)
    assert sue_bud.itemroot._kids[casa_str]._is_expanded is True

    # pledge: dict = None,
    sue_bud.itemroot._kids[casa_str].pledge = "funfun3"
    pledge = sue_bud.itemroot._kids[casa_str].pledge
    assert pledge == "funfun3"
    sue_bud.edit_item_attr(way=casa_way, pledge=True)
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
    sue_bud.edit_item_attr(way=casa_way, healerlink=x_healerlink)
    assert sue_bud.itemroot._kids[casa_str].healerlink == x_healerlink

    # _problem_bool: bool
    sue_bud.itemroot._kids[casa_str].problem_bool = "fun3rol"
    src_problem_bool = sue_bud.itemroot._kids[casa_str].problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True
    sue_bud.edit_item_attr(way=casa_way, problem_bool=x_problem_bool)
    assert sue_bud.itemroot._kids[casa_str].problem_bool == x_problem_bool


def test_BudUnit_edit_item_attr_RaisesErrorWhen_healerlink_healer_names_DoNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    yao_bud.set_l1_item(itemunit_shop(casa_str))
    day_str = "day_range"
    day_item = itemunit_shop(day_str, begin=44, close=110)
    day_way = yao_bud.make_l1_way(day_str)
    yao_bud.set_l1_item(day_item)

    casa_item = yao_bud.get_item_obj(casa_way)
    assert casa_item.begin is None
    assert casa_item.close is None

    # WHEN / THEN
    sue_str = "Sue"
    x_healerlink = healerlink_shop({sue_str})
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_item_attr(way=casa_way, healerlink=x_healerlink)
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
    assert item_list[0].item_tag == casa_str


def test_BudUnit_set_item_adoptee_RaisesErrorIfAdopteeItemDoesNotHaveCorrectParent():
    bob_bud = budunit_shop("Bob")
    sports_str = "sports"
    sports_way = bob_bud.make_l1_way(sports_str)
    bob_bud.set_l1_item(itemunit_shop(sports_str))
    swim_str = "swim"
    bob_bud.set_item(itemunit_shop(swim_str), parent_way=sports_way)

    # WHEN / THEN
    summer_str = "summer"
    hike_str = "hike"
    hike_way = bob_bud.make_way(sports_way, hike_str)
    with pytest_raises(Exception) as excinfo:
        bob_bud.set_item(
            item_kid=itemunit_shop(summer_str),
            parent_way=sports_way,
            adoptees=[swim_str, hike_str],
        )
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{hike_way}'"


def test_BudUnit_set_item_adoptee_CorrectlyAddsAdoptee():
    bob_bud = budunit_shop("Bob")
    sports_str = "sports"
    sports_way = bob_bud.make_l1_way(sports_str)
    bob_bud.set_l1_item(itemunit_shop(sports_str))
    swim_str = "swim"
    bob_bud.set_item(itemunit_shop(swim_str), parent_way=sports_way)
    hike_str = "hike"
    bob_bud.set_item(itemunit_shop(hike_str), parent_way=sports_way)

    sports_swim_way = bob_bud.make_way(sports_way, swim_str)
    sports_hike_way = bob_bud.make_way(sports_way, hike_str)
    assert bob_bud.item_exists(sports_swim_way)
    assert bob_bud.item_exists(sports_hike_way)
    summer_str = "summer"
    summer_way = bob_bud.make_way(sports_way, summer_str)
    summer_swim_way = bob_bud.make_way(summer_way, swim_str)
    summer_hike_way = bob_bud.make_way(summer_way, hike_str)
    assert bob_bud.item_exists(summer_swim_way) is False
    assert bob_bud.item_exists(summer_hike_way) is False

    # WHEN / THEN
    bob_bud.set_item(
        item_kid=itemunit_shop(summer_str),
        parent_way=sports_way,
        adoptees=[swim_str, hike_str],
    )

    # THEN
    summer_item = bob_bud.get_item_obj(summer_way)
    print(f"{summer_item._kids.keys()=}")
    assert bob_bud.item_exists(summer_swim_way)
    assert bob_bud.item_exists(summer_hike_way)
    assert bob_bud.item_exists(sports_swim_way) is False
    assert bob_bud.item_exists(sports_hike_way) is False


def test_BudUnit_set_item_bundling_SetsNewParentWithMassEqualToSumOfAdoptedItems():
    bob_bud = budunit_shop("Bob")
    sports_str = "sports"
    sports_way = bob_bud.make_l1_way(sports_str)
    bob_bud.set_l1_item(itemunit_shop(sports_str, mass=2))
    swim_str = "swim"
    swim_mass = 3
    bob_bud.set_item(itemunit_shop(swim_str, mass=swim_mass), sports_way)
    hike_str = "hike"
    hike_mass = 5
    bob_bud.set_item(itemunit_shop(hike_str, mass=hike_mass), sports_way)
    bball_str = "bball"
    bball_mass = 7
    bob_bud.set_item(itemunit_shop(bball_str, mass=bball_mass), sports_way)

    sports_swim_way = bob_bud.make_way(sports_way, swim_str)
    sports_hike_way = bob_bud.make_way(sports_way, hike_str)
    sports_bball_way = bob_bud.make_way(sports_way, bball_str)
    assert bob_bud.get_item_obj(sports_swim_way).mass == swim_mass
    assert bob_bud.get_item_obj(sports_hike_way).mass == hike_mass
    assert bob_bud.get_item_obj(sports_bball_way).mass == bball_mass
    summer_str = "summer"
    summer_way = bob_bud.make_way(sports_way, summer_str)
    summer_swim_way = bob_bud.make_way(summer_way, swim_str)
    summer_hike_way = bob_bud.make_way(summer_way, hike_str)
    summer_bball_way = bob_bud.make_way(summer_way, bball_str)
    assert bob_bud.item_exists(summer_swim_way) is False
    assert bob_bud.item_exists(summer_hike_way) is False
    assert bob_bud.item_exists(summer_bball_way) is False

    # WHEN / THEN
    bob_bud.set_item(
        item_kid=itemunit_shop(summer_str),
        parent_way=sports_way,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )

    # THEN
    assert bob_bud.get_item_obj(summer_way).mass == swim_mass + hike_mass
    assert bob_bud.get_item_obj(summer_swim_way).mass == swim_mass
    assert bob_bud.get_item_obj(summer_hike_way).mass == hike_mass
    assert bob_bud.item_exists(summer_bball_way) is False
    assert bob_bud.item_exists(sports_swim_way) is False
    assert bob_bud.item_exists(sports_hike_way) is False
    assert bob_bud.item_exists(sports_bball_way)


def test_BudUnit_del_item_obj_DeletingBundledItemReturnsItemsToOriginalState():
    bob_bud = budunit_shop("Bob")
    sports_str = "sports"
    sports_way = bob_bud.make_l1_way(sports_str)
    bob_bud.set_l1_item(itemunit_shop(sports_str, mass=2))
    swim_str = "swim"
    swim_mass = 3
    bob_bud.set_item(itemunit_shop(swim_str, mass=swim_mass), sports_way)
    hike_str = "hike"
    hike_mass = 5
    bob_bud.set_item(itemunit_shop(hike_str, mass=hike_mass), sports_way)
    bball_str = "bball"
    bball_mass = 7
    bob_bud.set_item(itemunit_shop(bball_str, mass=bball_mass), sports_way)

    sports_swim_way = bob_bud.make_way(sports_way, swim_str)
    sports_hike_way = bob_bud.make_way(sports_way, hike_str)
    sports_bball_way = bob_bud.make_way(sports_way, bball_str)
    assert bob_bud.get_item_obj(sports_swim_way).mass == swim_mass
    assert bob_bud.get_item_obj(sports_hike_way).mass == hike_mass
    assert bob_bud.get_item_obj(sports_bball_way).mass == bball_mass
    summer_str = "summer"
    summer_way = bob_bud.make_way(sports_way, summer_str)
    summer_swim_way = bob_bud.make_way(summer_way, swim_str)
    summer_hike_way = bob_bud.make_way(summer_way, hike_str)
    summer_bball_way = bob_bud.make_way(summer_way, bball_str)
    assert bob_bud.item_exists(summer_swim_way) is False
    assert bob_bud.item_exists(summer_hike_way) is False
    assert bob_bud.item_exists(summer_bball_way) is False
    bob_bud.set_item(
        item_kid=itemunit_shop(summer_str),
        parent_way=sports_way,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )
    assert bob_bud.get_item_obj(summer_way).mass == swim_mass + hike_mass
    assert bob_bud.get_item_obj(summer_swim_way).mass == swim_mass
    assert bob_bud.get_item_obj(summer_hike_way).mass == hike_mass
    assert bob_bud.item_exists(summer_bball_way) is False
    assert bob_bud.item_exists(sports_swim_way) is False
    assert bob_bud.item_exists(sports_hike_way) is False
    assert bob_bud.item_exists(sports_bball_way)
    print(f"{bob_bud._item_dict.keys()=}")

    # WHEN
    bob_bud.del_item_obj(way=summer_way, del_children=False)

    # THEN
    sports_swim_item = bob_bud.get_item_obj(sports_swim_way)
    sports_hike_item = bob_bud.get_item_obj(sports_hike_way)
    sports_bball_item = bob_bud.get_item_obj(sports_bball_way)
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
    swim_way = yao_bud.make_l1_way(swim_str)

    yao_bud.set_l1_item(itemunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_item = yao_bud.get_item_obj(swim_way)
    yao_bud.edit_item_attr(swim_way, awardlink=awardlink_yao)
    yao_bud.edit_item_attr(swim_way, awardlink=awardlink_zia)
    yao_bud.edit_item_attr(swim_way, awardlink=awardlink_Xio)

    assert len(swim_item.awardlinks) == 3
    assert len(yao_bud.itemroot._kids[swim_str].awardlinks) == 3

    # WHEN
    yao_bud.edit_item_attr(swim_way, awardlink_del=yao_str)

    # THEN
    swim_item = yao_bud.get_item_obj(swim_way)
    print(f"{swim_item.item_tag=}")
    print(f"{swim_item.awardlinks=}")
    print(f"{swim_item._awardheirs=}")

    assert len(yao_bud.itemroot._kids[swim_str].awardlinks) == 2


def test_BudUnit__get_filtered_awardlinks_item_CorrectlyRemovesAcct_awardlinks():
    # ESTABLISH
    bob_str = "Bob"
    example_bud = budunit_shop(bob_str)
    xia_str = "Xia"
    run_str = ";runners"
    hike_str = ";hikers"
    example_bud.add_acctunit(xia_str)
    example_bud.get_acct(xia_str).add_membership(run_str)

    sports_str = "sports"
    sports_way = example_bud.make_l1_way(sports_str)
    example_bud.set_l1_item(itemunit_shop(sports_str))
    example_bud.edit_item_attr(sports_way, awardlink=awardlink_shop(run_str))
    example_bud.edit_item_attr(sports_way, awardlink=awardlink_shop(hike_str))
    example_bud_sports_item = example_bud.get_item_obj(sports_way)
    assert len(example_bud_sports_item.awardlinks) == 2
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(xia_str)
    bob_bud.get_acct(xia_str).add_membership(run_str)
    print(f"{example_bud_sports_item.awardlinks=}")

    # WHEN
    cleaned_item = bob_bud._get_filtered_awardlinks_item(example_bud_sports_item)

    # THEN
    assert len(cleaned_item.awardlinks) == 1
    assert list(cleaned_item.awardlinks.keys()) == [run_str]


def test_BudUnit__get_filtered_awardlinks_item_CorrectlyRemovesGroup_awardlink():
    # ESTABLISH
    bob_str = "Bob"
    example_bud = budunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_bud.add_acctunit(xia_str)
    example_bud.add_acctunit(zoa_str)

    swim_str = "swim"
    swim_way = example_bud.make_l1_way(swim_str)
    example_bud.set_l1_item(itemunit_shop(swim_str))
    example_bud.edit_item_attr(swim_way, awardlink=awardlink_shop(xia_str))
    example_bud.edit_item_attr(swim_way, awardlink=awardlink_shop(zoa_str))
    example_bud_swim_item = example_bud.get_item_obj(swim_way)
    assert len(example_bud_swim_item.awardlinks) == 2
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(xia_str)

    # WHEN
    cleaned_item = bob_bud._get_filtered_awardlinks_item(example_bud_swim_item)

    # THEN
    assert len(cleaned_item.awardlinks) == 1
    assert list(cleaned_item.awardlinks.keys()) == [xia_str]


def test_BudUnit_set_item_CorrectlyCleansItem_awardlinks():
    # ESTABLISH
    bob_str = "Bob"
    example_bud = budunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_bud.add_acctunit(xia_str)
    example_bud.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_way = example_bud.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = example_bud.make_l1_way(swim_str)
    example_bud.set_l1_item(itemunit_shop(casa_str))
    example_bud.set_l1_item(itemunit_shop(swim_str))
    example_bud.edit_item_attr(swim_way, awardlink=awardlink_shop(xia_str))
    example_bud.edit_item_attr(swim_way, awardlink=awardlink_shop(zoa_str))
    example_bud_swim_item = example_bud.get_item_obj(swim_way)
    assert len(example_bud_swim_item.awardlinks) == 2

    # WHEN
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(xia_str)
    bob_bud.set_l1_item(example_bud_swim_item, create_missing_items=False)

    # THEN
    bob_bud_swim_item = bob_bud.get_item_obj(swim_way)
    assert len(bob_bud_swim_item.awardlinks) == 1
    assert list(bob_bud_swim_item.awardlinks.keys()) == [xia_str]


def test_BudUnit_get_item_obj_ReturnsItem():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    nation_str = "nation-state"
    nation_way = sue_bud.make_l1_way(nation_str)
    brazil_str = "Brazil"
    brazil_way = sue_bud.make_way(nation_way, brazil_str)

    # WHEN
    brazil_item = sue_bud.get_item_obj(way=brazil_way)

    # THEN
    assert brazil_item is not None
    assert brazil_item.item_tag == brazil_str

    # WHEN
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    week_item = sue_bud.get_item_obj(way=week_way)

    # THEN
    assert week_item is not None
    assert week_item.item_tag == week_str

    # WHEN
    root_item = sue_bud.get_item_obj(to_way(sue_bud.fisc_tag))

    # THEN
    assert root_item is not None
    assert root_item.item_tag == sue_bud.fisc_tag

    # WHEN / THEN
    bobdylan_str = "bobdylan"
    wrong_way = sue_bud.make_l1_way(bobdylan_str)
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_item_obj(way=wrong_way)
    assert str(excinfo.value) == f"get_item_obj failed. no item at '{wrong_way}'"


def test_BudUnit_item_exists_ReturnsCorrectBool():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    cat_way = sue_bud.make_l1_way("cat have dinner")
    week_way = sue_bud.make_l1_way("weekdays")
    casa_way = sue_bud.make_l1_way("casa")
    nation_way = sue_bud.make_l1_way("nation-state")
    sun_way = sue_bud.make_way(week_way, "Sunday")
    mon_way = sue_bud.make_way(week_way, "Monday")
    tue_way = sue_bud.make_way(week_way, "Tuesday")
    wed_way = sue_bud.make_way(week_way, "Wednesday")
    thu_way = sue_bud.make_way(week_way, "Thursday")
    fri_way = sue_bud.make_way(week_way, "Friday")
    sat_way = sue_bud.make_way(week_way, "Saturday")
    france_way = sue_bud.make_way(nation_way, "France")
    brazil_way = sue_bud.make_way(nation_way, "Brazil")
    usa_way = sue_bud.make_way(nation_way, "USA")
    texas_way = sue_bud.make_way(usa_way, "Texas")
    oregon_way = sue_bud.make_way(usa_way, "Oregon")
    # do not exist in bud
    sports_way = sue_bud.make_l1_way("sports")
    swim_way = sue_bud.make_way(sports_way, "swimming")
    idaho_way = sue_bud.make_way(usa_way, "Idaho")
    japan_way = sue_bud.make_way(nation_way, "Japan")

    # WHEN / THEN
    assert sue_bud.item_exists("") is False
    assert sue_bud.item_exists(None) is False
    assert sue_bud.item_exists(to_way(sue_bud.fisc_tag))
    assert sue_bud.item_exists(cat_way)
    assert sue_bud.item_exists(week_way)
    assert sue_bud.item_exists(casa_way)
    assert sue_bud.item_exists(nation_way)
    assert sue_bud.item_exists(sun_way)
    assert sue_bud.item_exists(mon_way)
    assert sue_bud.item_exists(tue_way)
    assert sue_bud.item_exists(wed_way)
    assert sue_bud.item_exists(thu_way)
    assert sue_bud.item_exists(fri_way)
    assert sue_bud.item_exists(sat_way)
    assert sue_bud.item_exists(usa_way)
    assert sue_bud.item_exists(france_way)
    assert sue_bud.item_exists(brazil_way)
    assert sue_bud.item_exists(texas_way)
    assert sue_bud.item_exists(oregon_way)
    assert sue_bud.item_exists(to_way("B")) is False
    assert sue_bud.item_exists(sports_way) is False
    assert sue_bud.item_exists(swim_way) is False
    assert sue_bud.item_exists(idaho_way) is False
    assert sue_bud.item_exists(japan_way) is False


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
    casa_way = bob_budunit.make_l1_way(casa_str)
    week_way = bob_budunit.make_l1_way(week_str)
    wed_way = bob_budunit.make_way(week_way, wed_str)
    casa_item = itemunit_shop(casa_str, _fund_onset=70, _fund_cease=170)
    week_item = itemunit_shop(week_str, _fund_onset=70, _fund_cease=75)
    wed_item = itemunit_shop(wed_str, _fund_onset=72, _fund_cease=75)
    casa_item.parent_way = bob_budunit.fisc_tag
    week_item.parent_way = bob_budunit.fisc_tag
    wed_item.parent_way = week_way
    bob_budunit.set_l1_item(casa_item)
    bob_budunit.set_l1_item(week_item)
    bob_budunit.set_item(wed_item, week_way)
    bob_budunit._offtrack_kids_mass_set.add(casa_way)
    bob_budunit._offtrack_kids_mass_set.add(week_way)
    assert bob_budunit._offtrack_fund == 0

    # WHEN
    bob_budunit.set_offtrack_fund()

    # THEN
    assert bob_budunit._offtrack_fund == 105

    # WHEN
    bob_budunit._offtrack_kids_mass_set.add(wed_way)
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
    casa_way = bob_budunit.make_l1_way(casa_str)
    week_way = bob_budunit.make_l1_way(week_str)
    wed_way = bob_budunit.make_way(week_way, wed_str)
    casa_item = itemunit_shop(casa_str, _fund_onset=70, _fund_cease=170)
    week_item = itemunit_shop(week_str, _fund_onset=70, _fund_cease=75)
    wed_item = itemunit_shop(wed_str, _fund_onset=72, _fund_cease=75)
    casa_item.parent_way = bob_budunit.fisc_tag
    week_item.parent_way = bob_budunit.fisc_tag
    wed_item.parent_way = week_way
    bob_budunit.set_l1_item(casa_item)
    bob_budunit.set_l1_item(week_item)
    bob_budunit.set_item(wed_item, week_way)
    bob_budunit._offtrack_kids_mass_set.add(casa_way)
    bob_budunit._offtrack_kids_mass_set.add(week_way)
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

    bob_budunit._offtrack_kids_mass_set.add(wed_way)
    bob_budunit.set_offtrack_fund()

    # THEN
    assert bob_budunit._offtrack_fund == 108
