from src.a01_term_logic.rope import create_rope
from src.a04_reason_logic.reason_plan import FactUnit, factunit_shop
from src.a06_believer_logic.believer import BelieverUnit, believerunit_shop


def _example_empty_bob_believerunit() -> BelieverUnit:
    a23_str = "amy23"
    return believerunit_shop("Bob", a23_str)


def get_mop_with_no_reason_believerunit_example() -> BelieverUnit:
    bob_believer = _example_empty_bob_believerunit()
    casa_str = "casa"
    mop_str = "mop"
    casa_rope = bob_believer.make_l1_rope(casa_str)
    mop_rope = bob_believer.make_rope(casa_rope, mop_str)
    bob_believer.add_plan(mop_rope, task=True)
    return bob_believer


def get_bob_mop_with_reason_believerunit_example() -> BelieverUnit:
    bob_believer = _example_empty_bob_believerunit()
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
        mop_rope, reason_r_context=floor_rope, reason_premise=clean_rope
    )
    return bob_believer


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    floor_rope = create_rope(casa_rope, "floor status")
    clean_rope = create_rope(floor_rope, "clean")
    return factunit_shop(floor_rope, clean_rope)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    floor_rope = create_rope(casa_rope, "floor status")
    dirty_rope = create_rope(floor_rope, "dirty")
    return factunit_shop(floor_rope, dirty_rope)
