from copy import deepcopy as copy_deepcopy
from src.a01_term_logic.rope import create_rope
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.believer_tool import (
    clear_factunits_from_believer,
    get_believer_root_facts_dict,
    set_factunits_to_believer,
)


def test_get_believer_root_facts_dict_ReturnsObj_Scenario0_No_factunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str)
    # WHEN / THEN
    assert get_believer_root_facts_dict(sue_believer) == {}
    assert (
        get_believer_root_facts_dict(sue_believer) == sue_believer.get_factunits_dict()
    )


def test_get_believer_root_facts_dict_ReturnsObj_Scenario1_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str)
    casa_rope = sue_believer.make_l1_rope("casa")
    clean_rope = sue_believer.make_l1_rope("clean")
    dirty_rope = sue_believer.make_l1_rope("dirty")
    sue_believer.add_fact(casa_rope, dirty_rope, create_missing_plans=True)

    # WHEN
    sue_fact_dict = get_believer_root_facts_dict(sue_believer)

    # THEN
    assert sue_fact_dict.get(casa_rope) != None
    casa_fact_dict = sue_fact_dict.get(casa_rope)
    assert casa_fact_dict.get("fact_context") == casa_rope
    assert casa_fact_dict.get("fact_state") == dirty_rope
    expected_sue_fact_dict = {
        casa_rope: {"fact_context": casa_rope, "fact_state": dirty_rope}
    }
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_get_believer_root_facts_dict_ReturnsObj_Scenario2_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str)
    casa_rope = sue_believer.make_l1_rope("casa")
    clean_rope = sue_believer.make_l1_rope("clean")
    dirty_rope = sue_believer.make_l1_rope("dirty")
    dirty_reason_lower = 10
    dirty_reason_upper = 13
    sue_believer.add_fact(
        casa_rope, dirty_rope, dirty_reason_lower, dirty_reason_upper, True
    )

    # WHEN
    sue_fact_dict = get_believer_root_facts_dict(sue_believer)

    # THEN
    assert sue_fact_dict.get(casa_rope) != None
    casa_fact_dict = sue_fact_dict.get(casa_rope)
    assert casa_fact_dict.get("fact_context") == casa_rope
    assert casa_fact_dict.get("fact_state") == dirty_rope
    assert casa_fact_dict.get("fact_lower") == dirty_reason_lower
    assert casa_fact_dict.get("fact_upper") == dirty_reason_upper
    expected_sue_fact_dict = {
        casa_rope: {
            "fact_context": casa_rope,
            "fact_state": dirty_rope,
            "fact_lower": dirty_reason_lower,
            "fact_upper": dirty_reason_upper,
        }
    }
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_set_factunits_to_believer_ReturnsObj_Scenario0_BelieverEmptyNoFacts():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao", "amy23")
    before_yao_believer = copy_deepcopy(yao_believer)
    facts_dict = {}
    assert yao_believer.get_dict() == before_yao_believer.get_dict()

    # WHEN
    set_factunits_to_believer(yao_believer, facts_dict)

    # THEN
    assert yao_believer.get_dict() == before_yao_believer.get_dict()


def test_set_factunits_to_believer_ReturnsObj_Scenario1_Believer1FactsChanged():
    # ESTABLISH
    bob_believer = believerunit_shop("Bob", "amy23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_believer.make_l1_rope(casa_str)
    floor_rope = bob_believer.make_rope(casa_rope, floor_str)
    clean_rope = bob_believer.make_rope(floor_rope, clean_str)
    dirty_rope = bob_believer.make_rope(floor_rope, dirty_str)
    mop_rope = bob_believer.make_rope(casa_rope, mop_str)
    bob_believer.add_plan(floor_rope)
    bob_believer.add_plan(clean_rope)
    bob_believer.add_plan(dirty_rope)
    bob_believer.add_plan(mop_rope, task=True)
    bob_believer.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    dirty_facts_dict = {
        floor_rope: {"fact_context": floor_rope, "fact_state": dirty_rope}
    }
    before_bob_believer = copy_deepcopy(bob_believer)
    assert bob_believer.get_factunits_dict() != dirty_facts_dict
    assert bob_believer.get_factunits_dict() == {}
    assert bob_believer.get_dict() == before_bob_believer.get_dict()

    # WHEN
    set_factunits_to_believer(bob_believer, dirty_facts_dict)

    # THEN
    assert bob_believer.get_dict() != before_bob_believer.get_dict()
    assert bob_believer.get_factunits_dict() == dirty_facts_dict


def test_set_factunits_to_believer_ReturnsObj_Scenario2_FactUnit_reason_context_DoesNotExistInBeliever():
    # ESTABLISH
    bob_believer = believerunit_shop("Bob", "amy23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_believer.make_l1_rope(casa_str)
    floor_rope = bob_believer.make_rope(casa_rope, floor_str)
    clean_rope = bob_believer.make_rope(floor_rope, clean_str)
    dirty_rope = bob_believer.make_rope(floor_rope, dirty_str)
    mop_rope = bob_believer.make_rope(casa_rope, mop_str)
    bob_believer.add_plan(floor_rope)
    # bob_believer.add_plan(clean_rope)
    bob_believer.add_plan(dirty_rope)
    bob_believer.add_plan(mop_rope, task=True)
    bob_believer.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    clean_facts_dict = {
        floor_rope: {"fact_context": floor_rope, "fact_state": clean_rope}
    }
    before_bob_believer = copy_deepcopy(bob_believer)
    assert bob_believer.get_factunits_dict() != clean_facts_dict
    assert bob_believer.get_factunits_dict() == {}
    assert bob_believer.get_dict() == before_bob_believer.get_dict()

    # WHEN
    set_factunits_to_believer(bob_believer, clean_facts_dict)

    # THEN
    assert bob_believer.get_dict() != before_bob_believer.get_dict()
    assert bob_believer.get_factunits_dict() == clean_facts_dict
    assert bob_believer.get_plan_obj(clean_rope)


def test_set_factunits_to_believer_ReturnsObj_Scenario3_FactUnit_reason_context_Withoutreason_contextNotAddedToBeliever():
    # ESTABLISH
    bob_believer = believerunit_shop("Bob", "amy23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_believer.make_l1_rope(casa_str)
    floor_rope = bob_believer.make_rope(casa_rope, floor_str)
    clean_rope = bob_believer.make_rope(floor_rope, clean_str)
    dirty_rope = bob_believer.make_rope(floor_rope, dirty_str)
    mop_rope = bob_believer.make_rope(casa_rope, mop_str)
    bob_believer.add_plan(floor_rope)
    # bob_believer.add_plan(clean_rope)
    bob_believer.add_plan(dirty_rope)
    bob_believer.add_plan(mop_rope, task=True)
    bob_believer.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )

    weather_str = "weather"
    raining_str = "raining"
    weather_rope = bob_believer.make_l1_rope(weather_str)
    rain_rope = bob_believer.make_rope(weather_rope, raining_str)

    two_facts_dict = {
        floor_rope: {"fact_context": floor_rope, "fact_state": clean_rope},
        weather_rope: {"fact_context": weather_rope, "fact_state": rain_rope},
    }
    before_bob_believer = copy_deepcopy(bob_believer)
    assert bob_believer.get_factunits_dict() != two_facts_dict
    assert bob_believer.get_factunits_dict() == {}
    assert bob_believer.get_dict() == before_bob_believer.get_dict()

    # WHEN
    set_factunits_to_believer(bob_believer, two_facts_dict)

    # THEN
    assert floor_rope in set(bob_believer.get_factunits_dict().keys())
    assert weather_rope not in set(bob_believer.get_factunits_dict().keys())
    assert bob_believer.get_dict() != before_bob_believer.get_dict()


def test_clear_factunits_from_believer_ReturnsObj_Scenario1_FactUnit_Exist():
    # ESTABLISH
    bob_believer = believerunit_shop("Bob", "amy23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_believer.make_l1_rope(casa_str)
    floor_rope = bob_believer.make_rope(casa_rope, floor_str)
    clean_rope = bob_believer.make_rope(floor_rope, clean_str)
    dirty_rope = bob_believer.make_rope(floor_rope, dirty_str)
    mop_rope = bob_believer.make_rope(casa_rope, mop_str)
    bob_believer.add_plan(floor_rope)
    # bob_believer.add_plan(clean_rope)
    bob_believer.add_plan(dirty_rope)
    bob_believer.add_plan(mop_rope, task=True)
    bob_believer.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    bob_believer.add_fact(floor_rope, dirty_rope)
    floor_facts_dict = {
        floor_rope: {"fact_context": floor_rope, "fact_state": dirty_rope}
    }
    assert bob_believer.get_factunits_dict() == floor_facts_dict
    assert bob_believer.get_factunits_dict() != {}

    # WHEN
    clear_factunits_from_believer(bob_believer)

    # THEN
    assert bob_believer.get_factunits_dict() != floor_facts_dict
    assert bob_believer.get_factunits_dict() == {}
