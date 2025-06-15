from copy import deepcopy as copy_deepcopy
from src.a01_term_logic.rope import create_rope
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.plan_tool import (
    clear_factunits_from_plan,
    get_plan_root_facts_dict,
    set_factunits_to_plan,
)


def test_get_plan_root_facts_dict_ReturnsObj_Scenario0_No_factunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    # WHEN / THEN
    assert get_plan_root_facts_dict(sue_plan) == {}
    assert get_plan_root_facts_dict(sue_plan) == sue_plan.get_factunits_dict()


def test_get_plan_root_facts_dict_ReturnsObj_Scenario1_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    casa_rope = sue_plan.make_l1_rope("case")
    clean_rope = sue_plan.make_l1_rope("clean")
    dirty_rope = sue_plan.make_l1_rope("dirty")
    sue_plan.add_fact(casa_rope, dirty_rope, create_missing_concepts=True)

    # WHEN
    sue_fact_dict = get_plan_root_facts_dict(sue_plan)

    # THEN
    assert sue_fact_dict.get(casa_rope) != None
    casa_fact_dict = sue_fact_dict.get(casa_rope)
    assert casa_fact_dict.get("fcontext") == casa_rope
    assert casa_fact_dict.get("fstate") == dirty_rope
    expected_sue_fact_dict = {casa_rope: {"fcontext": casa_rope, "fstate": dirty_rope}}
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_get_plan_root_facts_dict_ReturnsObj_Scenario2_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    casa_rope = sue_plan.make_l1_rope("case")
    clean_rope = sue_plan.make_l1_rope("clean")
    dirty_rope = sue_plan.make_l1_rope("dirty")
    dirty_popen = 10
    dirty_pnigh = 13
    sue_plan.add_fact(casa_rope, dirty_rope, dirty_popen, dirty_pnigh, True)

    # WHEN
    sue_fact_dict = get_plan_root_facts_dict(sue_plan)

    # THEN
    assert sue_fact_dict.get(casa_rope) != None
    casa_fact_dict = sue_fact_dict.get(casa_rope)
    assert casa_fact_dict.get("fcontext") == casa_rope
    assert casa_fact_dict.get("fstate") == dirty_rope
    assert casa_fact_dict.get("fopen") == dirty_popen
    assert casa_fact_dict.get("fnigh") == dirty_pnigh
    expected_sue_fact_dict = {
        casa_rope: {
            "fcontext": casa_rope,
            "fstate": dirty_rope,
            "fopen": dirty_popen,
            "fnigh": dirty_pnigh,
        }
    }
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_set_factunits_to_plan_ReturnsObj_Scenario0_PlanEmptyNoFacts():
    # ESTABLISH
    yao_plan = planunit_shop("Yao", "accord23")
    before_yao_plan = copy_deepcopy(yao_plan)
    facts_dict = {}
    assert yao_plan.get_dict() == before_yao_plan.get_dict()

    # WHEN
    set_factunits_to_plan(yao_plan, facts_dict)

    # THEN
    assert yao_plan.get_dict() == before_yao_plan.get_dict()


def test_set_factunits_to_plan_ReturnsObj_Scenario1_Plan1FactsChanged():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_plan.make_l1_rope(casa_str)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, clean_str)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, mop_str)
    bob_plan.add_concept(floor_rope)
    bob_plan.add_concept(clean_rope)
    bob_plan.add_concept(dirty_rope)
    bob_plan.add_concept(mop_rope, task=True)
    bob_plan.edit_concept_attr(
        mop_rope, reason_rcontext=floor_rope, reason_premise=dirty_rope
    )
    dirty_facts_dict = {floor_rope: {"fcontext": floor_rope, "fstate": dirty_rope}}
    before_bob_plan = copy_deepcopy(bob_plan)
    assert bob_plan.get_factunits_dict() != dirty_facts_dict
    assert bob_plan.get_factunits_dict() == {}
    assert bob_plan.get_dict() == before_bob_plan.get_dict()

    # WHEN
    set_factunits_to_plan(bob_plan, dirty_facts_dict)

    # THEN
    assert bob_plan.get_dict() != before_bob_plan.get_dict()
    assert bob_plan.get_factunits_dict() == dirty_facts_dict


def test_set_factunits_to_plan_ReturnsObj_Scenario2_FactUnit_rcontext_DoesNotExistInPlan():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_plan.make_l1_rope(casa_str)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, clean_str)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, mop_str)
    bob_plan.add_concept(floor_rope)
    # bob_plan.add_concept(clean_rope)
    bob_plan.add_concept(dirty_rope)
    bob_plan.add_concept(mop_rope, task=True)
    bob_plan.edit_concept_attr(
        mop_rope, reason_rcontext=floor_rope, reason_premise=dirty_rope
    )
    clean_facts_dict = {floor_rope: {"fcontext": floor_rope, "fstate": clean_rope}}
    before_bob_plan = copy_deepcopy(bob_plan)
    assert bob_plan.get_factunits_dict() != clean_facts_dict
    assert bob_plan.get_factunits_dict() == {}
    assert bob_plan.get_dict() == before_bob_plan.get_dict()

    # WHEN
    set_factunits_to_plan(bob_plan, clean_facts_dict)

    # THEN
    assert bob_plan.get_dict() != before_bob_plan.get_dict()
    assert bob_plan.get_factunits_dict() == clean_facts_dict
    assert bob_plan.get_concept_obj(clean_rope)


def test_set_factunits_to_plan_ReturnsObj_Scenario3_FactUnit_rcontext_WithoutRcontextNotAddedToPlan():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_plan.make_l1_rope(casa_str)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, clean_str)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, mop_str)
    bob_plan.add_concept(floor_rope)
    # bob_plan.add_concept(clean_rope)
    bob_plan.add_concept(dirty_rope)
    bob_plan.add_concept(mop_rope, task=True)
    bob_plan.edit_concept_attr(
        mop_rope, reason_rcontext=floor_rope, reason_premise=dirty_rope
    )

    weather_str = "weather"
    raining_str = "raining"
    weather_rope = bob_plan.make_l1_rope(weather_str)
    rain_rope = bob_plan.make_rope(weather_rope, raining_str)

    two_facts_dict = {
        floor_rope: {"fcontext": floor_rope, "fstate": clean_rope},
        weather_rope: {"fcontext": weather_rope, "fstate": rain_rope},
    }
    before_bob_plan = copy_deepcopy(bob_plan)
    assert bob_plan.get_factunits_dict() != two_facts_dict
    assert bob_plan.get_factunits_dict() == {}
    assert bob_plan.get_dict() == before_bob_plan.get_dict()

    # WHEN
    set_factunits_to_plan(bob_plan, two_facts_dict)

    # THEN
    assert floor_rope in set(bob_plan.get_factunits_dict().keys())
    assert weather_rope not in set(bob_plan.get_factunits_dict().keys())
    assert bob_plan.get_dict() != before_bob_plan.get_dict()


def test_clear_factunits_from_plan_ReturnsObj_Scenario1_FactUnit_Exist():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = bob_plan.make_l1_rope(casa_str)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, clean_str)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, mop_str)
    bob_plan.add_concept(floor_rope)
    # bob_plan.add_concept(clean_rope)
    bob_plan.add_concept(dirty_rope)
    bob_plan.add_concept(mop_rope, task=True)
    bob_plan.edit_concept_attr(
        mop_rope, reason_rcontext=floor_rope, reason_premise=dirty_rope
    )
    bob_plan.add_fact(floor_rope, dirty_rope)
    floor_facts_dict = {floor_rope: {"fcontext": floor_rope, "fstate": dirty_rope}}
    assert bob_plan.get_factunits_dict() == floor_facts_dict
    assert bob_plan.get_factunits_dict() != {}

    # WHEN
    clear_factunits_from_plan(bob_plan)

    # THEN
    assert bob_plan.get_factunits_dict() != floor_facts_dict
    assert bob_plan.get_factunits_dict() == {}
