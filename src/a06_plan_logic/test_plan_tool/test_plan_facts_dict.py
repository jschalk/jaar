from copy import deepcopy as copy_deepcopy
from src.a01_term_logic.way import create_way
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
    casa_way = sue_plan.make_l1_way("case")
    clean_way = sue_plan.make_l1_way("clean")
    dirty_way = sue_plan.make_l1_way("dirty")
    sue_plan.add_fact(casa_way, dirty_way, create_missing_concepts=True)

    # WHEN
    sue_fact_dict = get_plan_root_facts_dict(sue_plan)

    # THEN
    assert sue_fact_dict.get(casa_way) != None
    casa_fact_dict = sue_fact_dict.get(casa_way)
    assert casa_fact_dict.get("fcontext") == casa_way
    assert casa_fact_dict.get("fstate") == dirty_way
    expected_sue_fact_dict = {casa_way: {"fcontext": casa_way, "fstate": dirty_way}}
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_get_plan_root_facts_dict_ReturnsObj_Scenario2_factunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    casa_way = sue_plan.make_l1_way("case")
    clean_way = sue_plan.make_l1_way("clean")
    dirty_way = sue_plan.make_l1_way("dirty")
    dirty_popen = 10
    dirty_pnigh = 13
    sue_plan.add_fact(casa_way, dirty_way, dirty_popen, dirty_pnigh, True)

    # WHEN
    sue_fact_dict = get_plan_root_facts_dict(sue_plan)

    # THEN
    assert sue_fact_dict.get(casa_way) != None
    casa_fact_dict = sue_fact_dict.get(casa_way)
    assert casa_fact_dict.get("fcontext") == casa_way
    assert casa_fact_dict.get("fstate") == dirty_way
    assert casa_fact_dict.get("fopen") == dirty_popen
    assert casa_fact_dict.get("fnigh") == dirty_pnigh
    expected_sue_fact_dict = {
        casa_way: {
            "fcontext": casa_way,
            "fstate": dirty_way,
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
    casa_way = bob_plan.make_l1_way(casa_str)
    floor_way = bob_plan.make_way(casa_way, floor_str)
    clean_way = bob_plan.make_way(floor_way, clean_str)
    dirty_way = bob_plan.make_way(floor_way, dirty_str)
    mop_way = bob_plan.make_way(casa_way, mop_str)
    bob_plan.add_concept(floor_way)
    bob_plan.add_concept(clean_way)
    bob_plan.add_concept(dirty_way)
    bob_plan.add_concept(mop_way, task=True)
    bob_plan.edit_concept_attr(
        mop_way, reason_rcontext=floor_way, reason_premise=dirty_way
    )
    dirty_facts_dict = {floor_way: {"fcontext": floor_way, "fstate": dirty_way}}
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
    casa_way = bob_plan.make_l1_way(casa_str)
    floor_way = bob_plan.make_way(casa_way, floor_str)
    clean_way = bob_plan.make_way(floor_way, clean_str)
    dirty_way = bob_plan.make_way(floor_way, dirty_str)
    mop_way = bob_plan.make_way(casa_way, mop_str)
    bob_plan.add_concept(floor_way)
    # bob_plan.add_concept(clean_way)
    bob_plan.add_concept(dirty_way)
    bob_plan.add_concept(mop_way, task=True)
    bob_plan.edit_concept_attr(
        mop_way, reason_rcontext=floor_way, reason_premise=dirty_way
    )
    clean_facts_dict = {floor_way: {"fcontext": floor_way, "fstate": clean_way}}
    before_bob_plan = copy_deepcopy(bob_plan)
    assert bob_plan.get_factunits_dict() != clean_facts_dict
    assert bob_plan.get_factunits_dict() == {}
    assert bob_plan.get_dict() == before_bob_plan.get_dict()

    # WHEN
    set_factunits_to_plan(bob_plan, clean_facts_dict)

    # THEN
    assert bob_plan.get_dict() != before_bob_plan.get_dict()
    assert bob_plan.get_factunits_dict() == clean_facts_dict
    assert bob_plan.get_concept_obj(clean_way)


def test_set_factunits_to_plan_ReturnsObj_Scenario3_FactUnit_rcontext_WithoutRcontextNotAddedToPlan():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_way = bob_plan.make_l1_way(casa_str)
    floor_way = bob_plan.make_way(casa_way, floor_str)
    clean_way = bob_plan.make_way(floor_way, clean_str)
    dirty_way = bob_plan.make_way(floor_way, dirty_str)
    mop_way = bob_plan.make_way(casa_way, mop_str)
    bob_plan.add_concept(floor_way)
    # bob_plan.add_concept(clean_way)
    bob_plan.add_concept(dirty_way)
    bob_plan.add_concept(mop_way, task=True)
    bob_plan.edit_concept_attr(
        mop_way, reason_rcontext=floor_way, reason_premise=dirty_way
    )

    weather_str = "weather"
    raining_str = "raining"
    weather_way = bob_plan.make_l1_way(weather_str)
    rain_way = bob_plan.make_way(weather_way, raining_str)

    two_facts_dict = {
        floor_way: {"fcontext": floor_way, "fstate": clean_way},
        weather_way: {"fcontext": weather_way, "fstate": rain_way},
    }
    before_bob_plan = copy_deepcopy(bob_plan)
    assert bob_plan.get_factunits_dict() != two_facts_dict
    assert bob_plan.get_factunits_dict() == {}
    assert bob_plan.get_dict() == before_bob_plan.get_dict()

    # WHEN
    set_factunits_to_plan(bob_plan, two_facts_dict)

    # THEN
    assert floor_way in set(bob_plan.get_factunits_dict().keys())
    assert weather_way not in set(bob_plan.get_factunits_dict().keys())
    assert bob_plan.get_dict() != before_bob_plan.get_dict()


def test_clear_factunits_from_plan_ReturnsObj_Scenario1_FactUnit_Exist():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", "accord23")
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_way = bob_plan.make_l1_way(casa_str)
    floor_way = bob_plan.make_way(casa_way, floor_str)
    clean_way = bob_plan.make_way(floor_way, clean_str)
    dirty_way = bob_plan.make_way(floor_way, dirty_str)
    mop_way = bob_plan.make_way(casa_way, mop_str)
    bob_plan.add_concept(floor_way)
    # bob_plan.add_concept(clean_way)
    bob_plan.add_concept(dirty_way)
    bob_plan.add_concept(mop_way, task=True)
    bob_plan.edit_concept_attr(
        mop_way, reason_rcontext=floor_way, reason_premise=dirty_way
    )
    bob_plan.add_fact(floor_way, dirty_way)
    floor_facts_dict = {floor_way: {"fcontext": floor_way, "fstate": dirty_way}}
    assert bob_plan.get_factunits_dict() == floor_facts_dict
    assert bob_plan.get_factunits_dict() != {}

    # WHEN
    clear_factunits_from_plan(bob_plan)

    # THEN
    assert bob_plan.get_factunits_dict() != floor_facts_dict
    assert bob_plan.get_factunits_dict() == {}
