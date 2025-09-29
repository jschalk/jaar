from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_keywords import (
    Ch09Keywords as wx,
    DELETE_str,
    INSERT_str,
    belief_plan_factunit_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fact_upper_str,
    plan_rope_str,
)
from src.ch10_pack_logic.delta import beliefdelta_shop
from src.ch10_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_factunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_factunit_str()
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_belief.make_l1_rope("casa")
    fact_context_value = sue_belief.make_rope(casa_rope, "fridge status")
    fact_state_value = sue_belief.make_rope(fact_context_value, "dirty")
    swim_beliefatom = beliefatom_shop(dimen, INSERT_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(fact_context_str(), fact_context_value)
    swim_beliefatom.set_arg(fact_state_str(), fact_state_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' created for reason_context '{fact_context_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_factunit_str()
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_belief.make_l1_rope("casa")
    reason_context_value = sue_belief.make_rope(casa_rope, "fridge status")
    fact_state_value = sue_belief.make_rope(reason_context_value, "dirty")
    fact_upper_value = 13
    fact_lower_value = 17
    swim_beliefatom = beliefatom_shop(dimen, INSERT_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(fact_context_str(), reason_context_value)
    swim_beliefatom.set_arg(fact_state_str(), fact_state_value)
    swim_beliefatom.set_arg(fact_upper_str(), fact_upper_value)
    swim_beliefatom.set_arg(fact_lower_str(), fact_lower_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' created for reason_context '{reason_context_value}' for plan '{rope_value}'. fact_lower={fact_lower_value}. fact_upper={fact_upper_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_factunit_str()
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_belief.make_l1_rope("casa")
    reason_context_value = sue_belief.make_rope(casa_rope, "fridge status")
    fact_state_value = sue_belief.make_rope(reason_context_value, "dirty")
    swim_beliefatom = beliefatom_shop(dimen, wx.UPDATE)
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(fact_context_str(), reason_context_value)
    swim_beliefatom.set_arg(fact_state_str(), fact_state_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' updated for reason_context '{reason_context_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_factunit_str()
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_belief.make_l1_rope("casa")
    reason_context_value = sue_belief.make_rope(casa_rope, "fridge status")
    fact_state_value = sue_belief.make_rope(reason_context_value, "dirty")
    fact_upper_value = 13
    fact_lower_value = 17
    swim_beliefatom = beliefatom_shop(dimen, wx.UPDATE)
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(fact_context_str(), reason_context_value)
    swim_beliefatom.set_arg(fact_state_str(), fact_state_value)
    swim_beliefatom.set_arg(fact_upper_str(), fact_upper_value)
    swim_beliefatom.set_arg(fact_lower_str(), fact_lower_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' updated for reason_context '{reason_context_value}' for plan '{rope_value}'. fact_lower={fact_lower_value}. fact_upper={fact_upper_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_DELETE():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_factunit_str()
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_belief.make_l1_rope("casa")
    reason_context_value = sue_belief.make_rope(casa_rope, "fridge status")
    swim_beliefatom = beliefatom_shop(dimen, DELETE_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(fact_context_str(), reason_context_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"FactUnit reason_context '{reason_context_value}' deleted for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
