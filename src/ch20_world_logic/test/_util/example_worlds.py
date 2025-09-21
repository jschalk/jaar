from src.ch01_rope_logic.rope import create_rope
from src.ch04_reason_logic.reason import FactUnit, factunit_shop
from src.ch06_belief_logic.belief_main import BeliefUnit, beliefunit_shop


def _example_empty_bob_beliefunit() -> BeliefUnit:
    a23_str = "amy23"
    return beliefunit_shop("Bob", a23_str)


def get_mop_with_no_reason_beliefunit_example() -> BeliefUnit:
    bob_belief = _example_empty_bob_beliefunit()
    casa_str = "casa"
    mop_str = "mop"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    mop_rope = bob_belief.make_rope(casa_rope, mop_str)
    bob_belief.add_plan(mop_rope, task=True)
    return bob_belief


def get_bob_mop_with_reason_beliefunit_example() -> BeliefUnit:
    bob_belief = _example_empty_bob_beliefunit()
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
    bob_belief.add_plan(mop_rope, task=True)
    bob_belief.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=clean_rope
    )
    return bob_belief


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
