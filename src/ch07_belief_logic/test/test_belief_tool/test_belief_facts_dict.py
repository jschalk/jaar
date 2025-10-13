from copy import deepcopy as copy_deepcopy
from src.ch02_rope.rope import create_rope
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_tool import (
    clear_factunits_from_belief,
    get_belief_root_facts_dict,
    set_factunits_to_belief,
)


def test_get_belief_root_facts_dict_ReturnsObj_Scenario0_No_factunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    # WHEN / THEN
    assert get_belief_root_facts_dict(sue_belief) == {}
    assert (
        get_belief_root_facts_dict(sue_belief)
        == sue_belief.get_planroot_factunits_dict()
    )


def test_get_belief_root_facts_dict_ReturnsObj_Scenario1_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_l1_rope("clean")
    dirty_rope = sue_belief.make_l1_rope("dirty")
    sue_belief.add_fact(casa_rope, dirty_rope, create_missing_plans=True)

    # WHEN
    sue_fact_dict = get_belief_root_facts_dict(sue_belief)

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


def test_get_belief_root_facts_dict_ReturnsObj_Scenario2_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_l1_rope("clean")
    dirty_rope = sue_belief.make_l1_rope("dirty")
    dirty_reason_lower = 10
    dirty_reason_upper = 13
    sue_belief.add_fact(
        casa_rope, dirty_rope, dirty_reason_lower, dirty_reason_upper, True
    )

    # WHEN
    sue_fact_dict = get_belief_root_facts_dict(sue_belief)

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


def test_set_factunits_to_belief_ReturnsObj_Scenario0_BeliefEmptyNoFacts():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao", "amy23")
    before_yao_belief = copy_deepcopy(yao_belief)
    facts_dict = {}
    assert yao_belief.to_dict() == before_yao_belief.to_dict()

    # WHEN
    set_factunits_to_belief(yao_belief, facts_dict)

    # THEN
    assert yao_belief.to_dict() == before_yao_belief.to_dict()


def test_set_factunits_to_belief_ReturnsObj_Scenario1_Belief1FactsChanged():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob", "amy23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    floor_rope = bob_belief.make_rope(casa_rope, floor_str)
    clean_rope = bob_belief.make_rope(floor_rope, clean_str)
    dirty_rope = bob_belief.make_rope(floor_rope, dirty_str)
    mop_rope = bob_belief.make_rope(casa_rope, mop_str)
    bob_belief.add_plan(floor_rope)
    bob_belief.add_plan(clean_rope)
    bob_belief.add_plan(dirty_rope)
    bob_belief.add_plan(mop_rope, pledge=True)
    bob_belief.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    dirty_facts_dict = {
        floor_rope: {"fact_context": floor_rope, "fact_state": dirty_rope}
    }
    before_bob_belief = copy_deepcopy(bob_belief)
    assert bob_belief.get_planroot_factunits_dict() != dirty_facts_dict
    assert bob_belief.get_planroot_factunits_dict() == {}
    assert bob_belief.to_dict() == before_bob_belief.to_dict()

    # WHEN
    set_factunits_to_belief(bob_belief, dirty_facts_dict)

    # THEN
    assert bob_belief.to_dict() != before_bob_belief.to_dict()
    assert bob_belief.get_planroot_factunits_dict() == dirty_facts_dict


def test_set_factunits_to_belief_ReturnsObj_Scenario2_FactUnit_reason_context_DoesNotExistInBelief():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob", "amy23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    floor_rope = bob_belief.make_rope(casa_rope, floor_str)
    clean_rope = bob_belief.make_rope(floor_rope, clean_str)
    dirty_rope = bob_belief.make_rope(floor_rope, dirty_str)
    mop_rope = bob_belief.make_rope(casa_rope, mop_str)
    bob_belief.add_plan(floor_rope)
    # bob_belief.add_plan(clean_rope)
    bob_belief.add_plan(dirty_rope)
    bob_belief.add_plan(mop_rope, pledge=True)
    bob_belief.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    clean_facts_dict = {
        floor_rope: {"fact_context": floor_rope, "fact_state": clean_rope}
    }
    before_bob_belief = copy_deepcopy(bob_belief)
    assert bob_belief.get_planroot_factunits_dict() != clean_facts_dict
    assert bob_belief.get_planroot_factunits_dict() == {}
    assert bob_belief.to_dict() == before_bob_belief.to_dict()

    # WHEN
    set_factunits_to_belief(bob_belief, clean_facts_dict)

    # THEN
    assert bob_belief.to_dict() != before_bob_belief.to_dict()
    assert bob_belief.get_planroot_factunits_dict() == clean_facts_dict
    assert bob_belief.get_plan_obj(clean_rope)


def test_set_factunits_to_belief_ReturnsObj_Scenario3_FactUnit_reason_context_Withoutreason_contextNotAddedToBelief():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob", "amy23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    floor_rope = bob_belief.make_rope(casa_rope, floor_str)
    clean_rope = bob_belief.make_rope(floor_rope, clean_str)
    dirty_rope = bob_belief.make_rope(floor_rope, dirty_str)
    mop_rope = bob_belief.make_rope(casa_rope, mop_str)
    bob_belief.add_plan(floor_rope)
    # bob_belief.add_plan(clean_rope)
    bob_belief.add_plan(dirty_rope)
    bob_belief.add_plan(mop_rope, pledge=True)
    bob_belief.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )

    weather_str = "weather"
    raining_str = "raining"
    weather_rope = bob_belief.make_l1_rope(weather_str)
    rain_rope = bob_belief.make_rope(weather_rope, raining_str)

    two_facts_dict = {
        floor_rope: {"fact_context": floor_rope, "fact_state": clean_rope},
        weather_rope: {"fact_context": weather_rope, "fact_state": rain_rope},
    }
    before_bob_belief = copy_deepcopy(bob_belief)
    assert bob_belief.get_planroot_factunits_dict() != two_facts_dict
    assert bob_belief.get_planroot_factunits_dict() == {}
    assert bob_belief.to_dict() == before_bob_belief.to_dict()

    # WHEN
    set_factunits_to_belief(bob_belief, two_facts_dict)

    # THEN
    assert floor_rope in set(bob_belief.get_planroot_factunits_dict().keys())
    assert weather_rope not in set(bob_belief.get_planroot_factunits_dict().keys())
    assert bob_belief.to_dict() != before_bob_belief.to_dict()


def test_clear_factunits_from_belief_ReturnsObj_Scenario1_FactUnit_Exist():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob", "amy23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    floor_rope = bob_belief.make_rope(casa_rope, floor_str)
    clean_rope = bob_belief.make_rope(floor_rope, clean_str)
    dirty_rope = bob_belief.make_rope(floor_rope, dirty_str)
    mop_rope = bob_belief.make_rope(casa_rope, mop_str)
    bob_belief.add_plan(floor_rope)
    # bob_belief.add_plan(clean_rope)
    bob_belief.add_plan(dirty_rope)
    bob_belief.add_plan(mop_rope, pledge=True)
    bob_belief.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=dirty_rope
    )
    bob_belief.add_fact(floor_rope, dirty_rope)
    floor_facts_dict = {
        floor_rope: {"fact_context": floor_rope, "fact_state": dirty_rope}
    }
    assert bob_belief.get_planroot_factunits_dict() == floor_facts_dict
    assert bob_belief.get_planroot_factunits_dict() != {}

    # WHEN
    clear_factunits_from_belief(bob_belief)

    # THEN
    assert bob_belief.get_planroot_factunits_dict() != floor_facts_dict
    assert bob_belief.get_planroot_factunits_dict() == {}
