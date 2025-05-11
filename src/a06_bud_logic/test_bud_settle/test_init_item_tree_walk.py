from src.a01_way_logic.way import to_way
from src.a04_reason_logic.reason_item import reasonunit_shop
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop, get_sorted_item_list
from src.a06_bud_logic._utils.example_buds import get_budunit_with_4_levels


def test_BudUnit_set_item_dict_Scenario0():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    root_way = to_way(yao_bud.fisc_tag)
    root_item = yao_bud.get_item_obj(root_way)
    assert not root_item.begin
    assert not root_item.close
    assert not root_item._gogo_calc
    assert not root_item._stop_calc
    assert yao_bud._item_dict == {}
    assert yao_bud._reason_bases == set()

    # WHEN
    yao_bud._set_item_dict()

    # THEN
    assert not root_item.begin
    assert not root_item.close
    assert not root_item._gogo_calc
    assert not root_item._stop_calc
    assert yao_bud._item_dict == {root_item.get_way(): root_item}
    assert yao_bud._reason_bases == set()


def test_BudUnit_set_item_dict_Scenario1():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 7
    time0_close = 31
    root_way = to_way(yao_bud.fisc_tag)
    yao_bud.edit_item_attr(root_way, begin=time0_begin, close=time0_close)
    root_way = to_way(yao_bud.fisc_tag)
    root_item = yao_bud.get_item_obj(root_way)
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert not root_item._gogo_calc
    assert not root_item._stop_calc

    # WHEN
    yao_bud._set_item_dict()

    # THEN
    assert root_item.begin == time0_begin
    assert root_item.close == time0_close
    assert not root_item._gogo_calc
    assert not root_item._stop_calc


def test_BudUnit_set_item_dict_Clears_gogo_calc_stop_calc():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    root_way = to_way(sue_bud.fisc_tag)
    root_item = sue_bud.get_item_obj(root_way)
    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    usa_str = "USA"
    usa_way = sue_bud.make_way(states_way, usa_str)
    texas_str = "Texas"
    texas_way = sue_bud.make_way(usa_way, texas_str)
    texas_item = sue_bud.get_item_obj(texas_way)
    texas_item._gogo_calc = 7
    texas_item._stop_calc = 11
    texas_item._range_evaluated = True
    assert not root_item._gogo_calc
    assert not root_item._stop_calc
    assert texas_item._range_evaluated
    assert texas_item._gogo_calc
    assert texas_item._stop_calc

    # WHEN
    sue_bud._set_item_dict()

    # THEN
    assert not root_item.begin
    assert not root_item.close
    assert not texas_item._range_evaluated
    assert not texas_item._gogo_calc
    assert not texas_item._stop_calc


def test_BudUnit_set_item_dict_Sets_reason_bases():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    polis_str = "polis"
    polis_way = sue_bud.make_l1_way(polis_str)
    sue_bud.add_item(polis_way)
    sue_bud.add_item(states_way)
    sue_bud.edit_item_attr(states_way, reason_base=polis_way, reason_premise=polis_way)
    states_item = sue_bud.get_item_obj(states_way)
    assert states_item.base_reasonunit_exists(polis_way)
    assert sue_bud._reason_bases == set()

    # WHEN
    sue_bud._set_item_dict()

    # THEN
    assert sue_bud._reason_bases == {polis_way}


def test_BudUnit_set_item_CreatesItemUnitsUsedBy_reasonunits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    cleaning_way = sue_bud.make_way(casa_way, "cleaning")
    clean_cookery_str = "clean_cookery"
    clean_cookery_item = itemunit_shop(clean_cookery_str, mass=40, pledge=True)

    buildings_str = "buildings"
    buildings_way = sue_bud.make_l1_way(buildings_str)
    cookery_room_str = "cookery"
    cookery_room_way = sue_bud.make_way(buildings_way, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_way = sue_bud.make_way(cookery_room_way, cookery_dirty_str)
    cookery_reasonunit = reasonunit_shop(base=cookery_room_way)
    cookery_reasonunit.set_premise(premise=cookery_dirty_way)
    clean_cookery_item.set_reasonunit(cookery_reasonunit)

    assert sue_bud.item_exists(buildings_way) is False

    # WHEN
    sue_bud.set_item(clean_cookery_item, cleaning_way, create_missing_items=True)

    # THEN
    assert sue_bud.item_exists(buildings_way)


def test_get_sorted_item_list_ReturnsObj():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    cat_way = sue_bud.make_l1_way("cat have dinner")
    week_way = sue_bud.make_l1_way("weekdays")
    sun_way = sue_bud.make_way(week_way, "Sunday")
    mon_way = sue_bud.make_way(week_way, "Monday")
    tue_way = sue_bud.make_way(week_way, "Tuesday")
    wed_way = sue_bud.make_way(week_way, "Wednesday")
    thu_way = sue_bud.make_way(week_way, "Thursday")
    fri_way = sue_bud.make_way(week_way, "Friday")
    sat_way = sue_bud.make_way(week_way, "Saturday")
    states_way = sue_bud.make_l1_way("nation-state")
    usa_way = sue_bud.make_way(states_way, "USA")
    france_way = sue_bud.make_way(states_way, "France")
    brazil_way = sue_bud.make_way(states_way, "Brazil")
    texas_way = sue_bud.make_way(usa_way, "Texas")
    oregon_way = sue_bud.make_way(usa_way, "Oregon")
    sue_bud._set_item_dict()

    # WHEN
    x_sorted_item_list = get_sorted_item_list(list(sue_bud._item_dict.values()))

    # THEN
    assert x_sorted_item_list is not None
    assert len(x_sorted_item_list) == 17
    assert x_sorted_item_list[0] == sue_bud.itemroot
    assert x_sorted_item_list[1] == sue_bud.get_item_obj(casa_way)
    assert x_sorted_item_list[11] == sue_bud.get_item_obj(mon_way)
