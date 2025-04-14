from src.a01_word_logic.road import create_road
from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import (
    get_bud_root_facts_dict,
    set_factunits_to_bud,
    clear_factunits_from_bud,
)
from copy import deepcopy as copy_deepcopy


def test_get_bud_root_facts_dict_ReturnsObj_Scenario0_No_factunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    # WHEN / THEN
    assert get_bud_root_facts_dict(sue_bud) == {}
    assert get_bud_root_facts_dict(sue_bud) == sue_bud.get_factunits_dict()


def test_get_bud_root_facts_dict_ReturnsObj_Scenario1_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    casa_road = sue_bud.make_l1_road("case")
    clean_road = sue_bud.make_l1_road("clean")
    dirty_road = sue_bud.make_l1_road("dirty")
    sue_bud.add_fact(casa_road, dirty_road, create_missing_items=True)

    # WHEN
    sue_fact_dict = get_bud_root_facts_dict(sue_bud)

    # THEN
    assert sue_fact_dict.get(casa_road) != None
    casa_fact_dict = sue_fact_dict.get(casa_road)
    assert casa_fact_dict.get("base") == casa_road
    assert casa_fact_dict.get("pick") == dirty_road
    expected_sue_fact_dict = {casa_road: {"base": casa_road, "pick": dirty_road}}
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_get_bud_root_facts_dict_ReturnsObj_Scenario2_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    casa_road = sue_bud.make_l1_road("case")
    clean_road = sue_bud.make_l1_road("clean")
    dirty_road = sue_bud.make_l1_road("dirty")
    dirty_open = 10
    dirty_nigh = 13
    sue_bud.add_fact(casa_road, dirty_road, dirty_open, dirty_nigh, True)

    # WHEN
    sue_fact_dict = get_bud_root_facts_dict(sue_bud)

    # THEN
    assert sue_fact_dict.get(casa_road) != None
    casa_fact_dict = sue_fact_dict.get(casa_road)
    assert casa_fact_dict.get("base") == casa_road
    assert casa_fact_dict.get("pick") == dirty_road
    assert casa_fact_dict.get("fopen") == dirty_open
    assert casa_fact_dict.get("fnigh") == dirty_nigh
    expected_sue_fact_dict = {
        casa_road: {
            "base": casa_road,
            "pick": dirty_road,
            "fopen": dirty_open,
            "fnigh": dirty_nigh,
        }
    }
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_set_factunits_to_bud_ReturnsObj_Scenario0_BudEmptyNoFacts():
    # ESTABLISH
    yao_bud = budunit_shop("Yao", "accord23")
    before_yao_bud = copy_deepcopy(yao_bud)
    facts_dict = {}
    assert yao_bud.get_dict() == before_yao_bud.get_dict()

    # WHEN
    set_factunits_to_bud(yao_bud, facts_dict)

    # THEN
    assert yao_bud.get_dict() == before_yao_bud.get_dict()


def test_set_factunits_to_bud_ReturnsObj_Scenario1_Bud1FactsChanged():
    # ESTABLISH
    bob_bud = budunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_road = bob_bud.make_l1_road(casa_str)
    floor_road = bob_bud.make_road(casa_road, floor_str)
    clean_road = bob_bud.make_road(floor_road, clean_str)
    dirty_road = bob_bud.make_road(floor_road, dirty_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.add_item(floor_road)
    bob_bud.add_item(clean_road)
    bob_bud.add_item(dirty_road)
    bob_bud.add_item(mop_road, pledge=True)
    bob_bud.edit_item_attr(mop_road, reason_base=floor_road, reason_premise=dirty_road)
    dirty_facts_dict = {floor_road: {"base": floor_road, "pick": dirty_road}}
    before_bob_bud = copy_deepcopy(bob_bud)
    assert bob_bud.get_factunits_dict() != dirty_facts_dict
    assert bob_bud.get_factunits_dict() == {}
    assert bob_bud.get_dict() == before_bob_bud.get_dict()

    # WHEN
    set_factunits_to_bud(bob_bud, dirty_facts_dict)

    # THEN
    assert bob_bud.get_dict() != before_bob_bud.get_dict()
    assert bob_bud.get_factunits_dict() == dirty_facts_dict


def test_set_factunits_to_bud_ReturnsObj_Scenario2_FactUnit_base_DoesNotExistInBud():
    # ESTABLISH
    bob_bud = budunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_road = bob_bud.make_l1_road(casa_str)
    floor_road = bob_bud.make_road(casa_road, floor_str)
    clean_road = bob_bud.make_road(floor_road, clean_str)
    dirty_road = bob_bud.make_road(floor_road, dirty_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.add_item(floor_road)
    # bob_bud.add_item(clean_road)
    bob_bud.add_item(dirty_road)
    bob_bud.add_item(mop_road, pledge=True)
    bob_bud.edit_item_attr(mop_road, reason_base=floor_road, reason_premise=dirty_road)
    clean_facts_dict = {floor_road: {"base": floor_road, "pick": clean_road}}
    before_bob_bud = copy_deepcopy(bob_bud)
    assert bob_bud.get_factunits_dict() != clean_facts_dict
    assert bob_bud.get_factunits_dict() == {}
    assert bob_bud.get_dict() == before_bob_bud.get_dict()

    # WHEN
    set_factunits_to_bud(bob_bud, clean_facts_dict)

    # THEN
    assert bob_bud.get_dict() != before_bob_bud.get_dict()
    assert bob_bud.get_factunits_dict() == clean_facts_dict
    assert bob_bud.get_item_obj(clean_road)


def test_set_factunits_to_bud_ReturnsObj_Scenario3_FactUnit_base_WithoutBaseNotAddedToBud():
    # ESTABLISH
    bob_bud = budunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_road = bob_bud.make_l1_road(casa_str)
    floor_road = bob_bud.make_road(casa_road, floor_str)
    clean_road = bob_bud.make_road(floor_road, clean_str)
    dirty_road = bob_bud.make_road(floor_road, dirty_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.add_item(floor_road)
    # bob_bud.add_item(clean_road)
    bob_bud.add_item(dirty_road)
    bob_bud.add_item(mop_road, pledge=True)
    bob_bud.edit_item_attr(mop_road, reason_base=floor_road, reason_premise=dirty_road)

    weather_str = "weather"
    raining_str = "raining"
    weather_road = bob_bud.make_l1_road(weather_str)
    rain_road = bob_bud.make_road(weather_road, raining_str)

    two_facts_dict = {
        floor_road: {"base": floor_road, "pick": clean_road},
        weather_road: {"base": weather_road, "pick": rain_road},
    }
    before_bob_bud = copy_deepcopy(bob_bud)
    assert bob_bud.get_factunits_dict() != two_facts_dict
    assert bob_bud.get_factunits_dict() == {}
    assert bob_bud.get_dict() == before_bob_bud.get_dict()

    # WHEN
    set_factunits_to_bud(bob_bud, two_facts_dict)

    # THEN
    assert floor_road in set(bob_bud.get_factunits_dict().keys())
    assert weather_road not in set(bob_bud.get_factunits_dict().keys())
    assert bob_bud.get_dict() != before_bob_bud.get_dict()


def test_clear_factunits_from_bud_ReturnsObj_Scenario1_FactUnit_Exist():
    # ESTABLISH
    bob_bud = budunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_road = bob_bud.make_l1_road(casa_str)
    floor_road = bob_bud.make_road(casa_road, floor_str)
    clean_road = bob_bud.make_road(floor_road, clean_str)
    dirty_road = bob_bud.make_road(floor_road, dirty_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.add_item(floor_road)
    # bob_bud.add_item(clean_road)
    bob_bud.add_item(dirty_road)
    bob_bud.add_item(mop_road, pledge=True)
    bob_bud.edit_item_attr(mop_road, reason_base=floor_road, reason_premise=dirty_road)
    bob_bud.add_fact(floor_road, dirty_road)
    floor_facts_dict = {floor_road: {"base": floor_road, "pick": dirty_road}}
    assert bob_bud.get_factunits_dict() == floor_facts_dict
    assert bob_bud.get_factunits_dict() != {}

    # WHEN
    clear_factunits_from_bud(bob_bud)

    # THEN
    assert bob_bud.get_factunits_dict() != floor_facts_dict
    assert bob_bud.get_factunits_dict() == {}
