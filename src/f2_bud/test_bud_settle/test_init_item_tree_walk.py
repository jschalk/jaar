from src.f2_bud.examples.example_buds import get_budunit_with_4_levels
from src.f2_bud.reason_item import reasonunit_shop
from src.f2_bud.item import itemunit_shop
from src.f2_bud.bud import budunit_shop, get_sorted_item_list
from pytest import raises as pytest_raises


def test_BudUnit_set_item_dict_Scenario0():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
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
    assert yao_bud._item_dict == {root_item.get_road(): root_item}
    assert yao_bud._reason_bases == set()


def test_BudUnit_set_item_dict_Scenario1():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    time0_begin = 7
    time0_close = 31
    yao_bud.edit_item_attr(yao_bud._fiscal_id, begin=time0_begin, close=time0_close)
    root_item = yao_bud.get_item_obj(yao_bud._fiscal_id)
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
    root_item = sue_bud.get_item_obj(sue_bud._fiscal_id)
    states_str = "nation-state"
    states_road = sue_bud.make_l1_road(states_str)
    usa_str = "USA"
    usa_road = sue_bud.make_road(states_road, usa_str)
    texas_str = "Texas"
    texas_road = sue_bud.make_road(usa_road, texas_str)
    texas_item = sue_bud.get_item_obj(texas_road)
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
    states_road = sue_bud.make_l1_road(states_str)
    polis_str = "polis"
    polis_road = sue_bud.make_l1_road(polis_str)
    sue_bud.add_item(polis_road)
    sue_bud.add_item(states_road)
    sue_bud.edit_item_attr(
        states_road, reason_base=polis_road, reason_premise=polis_road
    )
    states_item = sue_bud.get_item_obj(states_road)
    assert states_item.base_reasonunit_exists(polis_road)
    assert sue_bud._reason_bases == set()

    # WHEN
    sue_bud._set_item_dict()

    # THEN
    assert sue_bud._reason_bases == {polis_road}


def test_BudUnit_set_item_CreatesItemUnitsUsedBy_reasonunits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_road = sue_bud.make_l1_road("casa")
    cleaning_road = sue_bud.make_road(casa_road, "cleaning")
    clean_cookery_str = "clean_cookery"
    clean_cookery_item = itemunit_shop(clean_cookery_str, mass=40, pledge=True)

    buildings_str = "buildings"
    buildings_road = sue_bud.make_l1_road(buildings_str)
    cookery_room_str = "cookery"
    cookery_room_road = sue_bud.make_road(buildings_road, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_road = sue_bud.make_road(cookery_room_road, cookery_dirty_str)
    cookery_reasonunit = reasonunit_shop(base=cookery_room_road)
    cookery_reasonunit.set_premise(premise=cookery_dirty_road)
    clean_cookery_item.set_reasonunit(cookery_reasonunit)

    assert sue_bud.item_exists(buildings_road) is False

    # WHEN
    sue_bud.set_item(clean_cookery_item, cleaning_road, create_missing_items=True)

    # THEN
    assert sue_bud.item_exists(buildings_road)


def test_get_sorted_item_list_ReturnsObj():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_road = sue_bud.make_l1_road("casa")
    cat_road = sue_bud.make_l1_road("cat have dinner")
    week_road = sue_bud.make_l1_road("weekdays")
    sun_road = sue_bud.make_road(week_road, "Sunday")
    mon_road = sue_bud.make_road(week_road, "Monday")
    tue_road = sue_bud.make_road(week_road, "Tuesday")
    wed_road = sue_bud.make_road(week_road, "Wednesday")
    thu_road = sue_bud.make_road(week_road, "Thursday")
    fri_road = sue_bud.make_road(week_road, "Friday")
    sat_road = sue_bud.make_road(week_road, "Saturday")
    states_road = sue_bud.make_l1_road("nation-state")
    usa_road = sue_bud.make_road(states_road, "USA")
    france_road = sue_bud.make_road(states_road, "France")
    brazil_road = sue_bud.make_road(states_road, "Brazil")
    texas_road = sue_bud.make_road(usa_road, "Texas")
    oregon_road = sue_bud.make_road(usa_road, "Oregon")
    sue_bud._set_item_dict()

    # WHEN
    x_sorted_item_list = get_sorted_item_list(list(sue_bud._item_dict.values()))

    # THEN
    assert x_sorted_item_list is not None
    assert len(x_sorted_item_list) == 17
    assert x_sorted_item_list[0] == sue_bud._itemroot
    assert x_sorted_item_list[1] == sue_bud.get_item_obj(casa_road)
    assert x_sorted_item_list[11] == sue_bud.get_item_obj(mon_road)
