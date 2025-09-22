from src.ch06_belief_logic.belief_main import beliefunit_shop
from src.ch08_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_terms import (
    DELETE_str,
    INSERT_str,
    belief_plan_healerunit_str,
    healer_name_str,
    plan_rope_str,
)
from src.ch10_pack_logic.delta import beliefdelta_shop
from src.ch10_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_healerunit_INSERT():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_healerunit_str()
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    healer_name_value = f"{sue_belief.knot}Swimmers"
    swim_beliefatom = beliefatom_shop(dimen, INSERT_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(healer_name_str(), healer_name_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"HealerUnit '{healer_name_value}' created for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_healerunit_DELETE():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = belief_plan_healerunit_str()
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    healer_name_value = f"{sue_belief.knot}Swimmers"
    swim_beliefatom = beliefatom_shop(dimen, DELETE_str())
    swim_beliefatom.set_arg(plan_rope_str(), rope_value)
    swim_beliefatom.set_arg(healer_name_str(), healer_name_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"HealerUnit '{healer_name_value}' deleted for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
