from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_tool import get_belief_unique_short_ropes
from src.ref.keywords import Ch07Keywords as kw


def test_get_belief_unique_short_ropes_ReturnsObj_Scenario0_RootOnly():
    # ESTABLISH
    a23_str = "Amy23"
    sue_belief = beliefunit_shop("Sue", a23_str)

    # WHEN
    unique_short_ropes = get_belief_unique_short_ropes(sue_belief)

    # THEN
    assert unique_short_ropes == {sue_belief.planroot.get_plan_rope(): a23_str}


def test_get_belief_unique_short_ropess_ReturnsObj_Scenario1_PlansWithUniqueLabels():
    # ESTABLISH
    a23_str = "Amy23"
    sue_belief = beliefunit_shop("Sue", a23_str)
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    mop_str = "mop"
    mop_rope = sue_belief.make_rope(casa_rope, mop_str)
    sue_belief.add_plan(mop_rope)

    # WHEN
    unique_short_ropes = get_belief_unique_short_ropes(sue_belief)

    # THEN
    root_rope = sue_belief.planroot.get_plan_rope()
    assert unique_short_ropes == {
        root_rope: a23_str,
        casa_rope: casa_str,
        mop_rope: mop_str,
    }


def test_get_belief_unique_short_ropess_ReturnsObj_Scenario2_PlansWithCommonLabels():
    # ESTABLISH
    a23_str = "Amy23"
    sue_belief = beliefunit_shop("Sue", a23_str)
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    mop_str = "mop"
    casa_mop_rope = sue_belief.make_rope(casa_rope, mop_str)
    sports_str = "sports"
    sports_rope = sue_belief.make_l1_rope(sports_str)
    sports_mop_rope = sue_belief.make_rope(sports_rope, mop_str)
    sue_belief.add_plan(casa_mop_rope)
    sue_belief.add_plan(sports_mop_rope)

    # WHEN
    unique_short_ropes = get_belief_unique_short_ropes(sue_belief)

    # THEN
    root_rope = sue_belief.planroot.get_plan_rope()
    knot = sue_belief.knot
    expected_short_casa_mop = f"{casa_str}{knot}{mop_str}"
    assert unique_short_ropes.get(casa_mop_rope) == expected_short_casa_mop
    assert unique_short_ropes == {
        root_rope: a23_str,
        casa_rope: casa_str,
        casa_mop_rope: expected_short_casa_mop,
        sports_rope: sports_str,
        sports_mop_rope: f"{sports_str}{knot}{mop_str}",
    }
