from src.a01_way_logic.way import create_way
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_tool import (
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
    casa_way = sue_bud.make_l1_way("case")
    clean_way = sue_bud.make_l1_way("clean")
    dirty_way = sue_bud.make_l1_way("dirty")
    sue_bud.add_fact(casa_way, dirty_way, create_missing_ideas=True)

    # WHEN
    sue_fact_dict = get_bud_root_facts_dict(sue_bud)

    # THEN
    assert sue_fact_dict.get(casa_way) != None
    casa_fact_dict = sue_fact_dict.get(casa_way)
    assert casa_fact_dict.get("fcontext") == casa_way
    assert casa_fact_dict.get("fbranch") == dirty_way
    expected_sue_fact_dict = {casa_way: {"fcontext": casa_way, "fbranch": dirty_way}}
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_get_bud_root_facts_dict_ReturnsObj_Scenario2_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    casa_way = sue_bud.make_l1_way("case")
    clean_way = sue_bud.make_l1_way("clean")
    dirty_way = sue_bud.make_l1_way("dirty")
    dirty_open = 10
    dirty_nigh = 13
    sue_bud.add_fact(casa_way, dirty_way, dirty_open, dirty_nigh, True)

    # WHEN
    sue_fact_dict = get_bud_root_facts_dict(sue_bud)

    # THEN
    assert sue_fact_dict.get(casa_way) != None
    casa_fact_dict = sue_fact_dict.get(casa_way)
    assert casa_fact_dict.get("fcontext") == casa_way
    assert casa_fact_dict.get("fbranch") == dirty_way
    assert casa_fact_dict.get("fopen") == dirty_open
    assert casa_fact_dict.get("fnigh") == dirty_nigh
    expected_sue_fact_dict = {
        casa_way: {
            "fcontext": casa_way,
            "fbranch": dirty_way,
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
    casa_way = bob_bud.make_l1_way(casa_str)
    floor_way = bob_bud.make_way(casa_way, floor_str)
    clean_way = bob_bud.make_way(floor_way, clean_str)
    dirty_way = bob_bud.make_way(floor_way, dirty_str)
    mop_way = bob_bud.make_way(casa_way, mop_str)
    bob_bud.add_idea(floor_way)
    bob_bud.add_idea(clean_way)
    bob_bud.add_idea(dirty_way)
    bob_bud.add_idea(mop_way, pledge=True)
    bob_bud.edit_idea_attr(mop_way, reason_context=floor_way, reason_premise=dirty_way)
    dirty_facts_dict = {floor_way: {"fcontext": floor_way, "fbranch": dirty_way}}
    before_bob_bud = copy_deepcopy(bob_bud)
    assert bob_bud.get_factunits_dict() != dirty_facts_dict
    assert bob_bud.get_factunits_dict() == {}
    assert bob_bud.get_dict() == before_bob_bud.get_dict()

    # WHEN
    set_factunits_to_bud(bob_bud, dirty_facts_dict)

    # THEN
    assert bob_bud.get_dict() != before_bob_bud.get_dict()
    assert bob_bud.get_factunits_dict() == dirty_facts_dict


def test_set_factunits_to_bud_ReturnsObj_Scenario2_FactUnit_context_DoesNotExistInBud():
    # ESTABLISH
    bob_bud = budunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_way = bob_bud.make_l1_way(casa_str)
    floor_way = bob_bud.make_way(casa_way, floor_str)
    clean_way = bob_bud.make_way(floor_way, clean_str)
    dirty_way = bob_bud.make_way(floor_way, dirty_str)
    mop_way = bob_bud.make_way(casa_way, mop_str)
    bob_bud.add_idea(floor_way)
    # bob_bud.add_idea(clean_way)
    bob_bud.add_idea(dirty_way)
    bob_bud.add_idea(mop_way, pledge=True)
    bob_bud.edit_idea_attr(mop_way, reason_context=floor_way, reason_premise=dirty_way)
    clean_facts_dict = {floor_way: {"fcontext": floor_way, "fbranch": clean_way}}
    before_bob_bud = copy_deepcopy(bob_bud)
    assert bob_bud.get_factunits_dict() != clean_facts_dict
    assert bob_bud.get_factunits_dict() == {}
    assert bob_bud.get_dict() == before_bob_bud.get_dict()

    # WHEN
    set_factunits_to_bud(bob_bud, clean_facts_dict)

    # THEN
    assert bob_bud.get_dict() != before_bob_bud.get_dict()
    assert bob_bud.get_factunits_dict() == clean_facts_dict
    assert bob_bud.get_idea_obj(clean_way)


def test_set_factunits_to_bud_ReturnsObj_Scenario3_FactUnit_context_WithoutContextNotAddedToBud():
    # ESTABLISH
    bob_bud = budunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_way = bob_bud.make_l1_way(casa_str)
    floor_way = bob_bud.make_way(casa_way, floor_str)
    clean_way = bob_bud.make_way(floor_way, clean_str)
    dirty_way = bob_bud.make_way(floor_way, dirty_str)
    mop_way = bob_bud.make_way(casa_way, mop_str)
    bob_bud.add_idea(floor_way)
    # bob_bud.add_idea(clean_way)
    bob_bud.add_idea(dirty_way)
    bob_bud.add_idea(mop_way, pledge=True)
    bob_bud.edit_idea_attr(mop_way, reason_context=floor_way, reason_premise=dirty_way)

    weather_str = "weather"
    raining_str = "raining"
    weather_way = bob_bud.make_l1_way(weather_str)
    rain_way = bob_bud.make_way(weather_way, raining_str)

    two_facts_dict = {
        floor_way: {"fcontext": floor_way, "fbranch": clean_way},
        weather_way: {"fcontext": weather_way, "fbranch": rain_way},
    }
    before_bob_bud = copy_deepcopy(bob_bud)
    assert bob_bud.get_factunits_dict() != two_facts_dict
    assert bob_bud.get_factunits_dict() == {}
    assert bob_bud.get_dict() == before_bob_bud.get_dict()

    # WHEN
    set_factunits_to_bud(bob_bud, two_facts_dict)

    # THEN
    assert floor_way in set(bob_bud.get_factunits_dict().keys())
    assert weather_way not in set(bob_bud.get_factunits_dict().keys())
    assert bob_bud.get_dict() != before_bob_bud.get_dict()


def test_clear_factunits_from_bud_ReturnsObj_Scenario1_FactUnit_Exist():
    # ESTABLISH
    bob_bud = budunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_way = bob_bud.make_l1_way(casa_str)
    floor_way = bob_bud.make_way(casa_way, floor_str)
    clean_way = bob_bud.make_way(floor_way, clean_str)
    dirty_way = bob_bud.make_way(floor_way, dirty_str)
    mop_way = bob_bud.make_way(casa_way, mop_str)
    bob_bud.add_idea(floor_way)
    # bob_bud.add_idea(clean_way)
    bob_bud.add_idea(dirty_way)
    bob_bud.add_idea(mop_way, pledge=True)
    bob_bud.edit_idea_attr(mop_way, reason_context=floor_way, reason_premise=dirty_way)
    bob_bud.add_fact(floor_way, dirty_way)
    floor_facts_dict = {floor_way: {"fcontext": floor_way, "fbranch": dirty_way}}
    assert bob_bud.get_factunits_dict() == floor_facts_dict
    assert bob_bud.get_factunits_dict() != {}

    # WHEN
    clear_factunits_from_bud(bob_bud)

    # THEN
    assert bob_bud.get_factunits_dict() != floor_facts_dict
    assert bob_bud.get_factunits_dict() == {}
