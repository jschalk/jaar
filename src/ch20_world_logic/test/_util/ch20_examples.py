from src.ch07_belief_logic.belief_main import BeliefUnit
from src.ch15_moment.test._util.ch15_examples import _example_empty_bob_beliefunit


def get_mop_with_no_reason_beliefunit_example() -> BeliefUnit:
    bob_belief = _example_empty_bob_beliefunit()
    casa_str = "casa"
    mop_str = "mop"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    mop_rope = bob_belief.make_rope(casa_rope, mop_str)
    bob_belief.add_plan(mop_rope, pledge=True)
    return bob_belief


def get_bob_mop_reason_beliefunit_example() -> BeliefUnit:
    bob_belief = _example_empty_bob_beliefunit()
    casa_str = "casa"
    floor_str = "floor situation"
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
        mop_rope, reason_context=floor_rope, reason_case=clean_rope
    )
    return bob_belief
