from src.a01_term_logic.way import create_way
from src.a04_reason_logic.reason_concept import FactUnit, factunit_shop
from src.a06_plan_logic.plan import PlanUnit, planunit_shop


def _example_empty_bob_planunit() -> PlanUnit:
    a23_str = "accord23"
    return planunit_shop("Bob", a23_str)


def get_mop_with_no_reason_planunit_example() -> PlanUnit:
    bob_plan = _example_empty_bob_planunit()
    casa_str = "casa"
    mop_str = "mop"
    casa_way = bob_plan.make_l1_way(casa_str)
    mop_way = bob_plan.make_way(casa_way, mop_str)
    bob_plan.add_concept(mop_way, task=True)
    return bob_plan


def get_bob_mop_with_reason_planunit_example() -> PlanUnit:
    bob_plan = _example_empty_bob_planunit()
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
        mop_way, reason_rcontext=floor_way, reason_premise=clean_way
    )
    return bob_plan


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    floor_way = create_way(casa_way, "floor status")
    clean_way = create_way(floor_way, "clean")
    return factunit_shop(floor_way, clean_way)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "accord23"
    casa_way = create_way(a23_str, "casa")
    floor_way = create_way(casa_way, "floor status")
    dirty_way = create_way(floor_way, "dirty")
    return factunit_shop(floor_way, dirty_way)
