from pytest import raises as pytest_raises
from src.ch02_rope_logic.rope import create_rope, default_knot_if_None, to_rope
from src.ch04_group_logic.group import awardunit_shop
from src.ch04_group_logic.labor import laborunit_shop
from src.ch05_reason_logic.reason import caseunit_shop, factunit_shop, reasonunit_shop
from src.ch06_plan_logic.healer import healerunit_shop
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_tool import set_case_attr
from src.ch07_belief_logic.test._util.example_beliefs import (
    get_beliefunit_with_4_levels,
)


def test_set_case_attr_SetNestedPlanUnitAttr_reason_context():
    # ESTABLISH
    slash_str = "/"
    bob_belief = beliefunit_shop("Bob", knot=slash_str)
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wed"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    wk_rope = bob_belief.make_l1_rope(wk_str)
    wed_rope = bob_belief.make_rope(wk_rope, wed_str)
    bob_belief.set_l1_plan(planunit_shop(casa_str))
    bob_belief.set_l1_plan(planunit_shop(wk_str))
    bob_belief.set_plan(planunit_shop(wed_str), wk_rope)
    casa_plan = bob_belief.get_plan_obj(casa_rope)
    assert not casa_plan.reasonunits.get(wk_rope)

    # WHEN
    set_case_attr(bob_belief, casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    assert casa_plan.reasonunits.get(wk_rope)
