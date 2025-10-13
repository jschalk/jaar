from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom.atom_main import beliefatom_shop
from src.ch10_pack.delta import beliefdelta_shop
from src.ch10_pack.legible import create_legible_list
from src.ref.keywords import Ch10Keywords as wx


def test_create_legible_list_ReturnsObj_plan_healerunit_INSERT():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    dimen = wx.belief_plan_healerunit
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    healer_name_value = f"{sue_belief.knot}Swimmers"
    swim_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    swim_beliefatom.set_arg(wx.plan_rope, rope_value)
    swim_beliefatom.set_arg(wx.healer_name, healer_name_value)
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
    dimen = wx.belief_plan_healerunit
    casa_rope = sue_belief.make_l1_rope("casa")
    rope_value = sue_belief.make_rope(casa_rope, "clean fridge")
    healer_name_value = f"{sue_belief.knot}Swimmers"
    swim_beliefatom = beliefatom_shop(dimen, wx.DELETE)
    swim_beliefatom.set_arg(wx.plan_rope, rope_value)
    swim_beliefatom.set_arg(wx.healer_name, healer_name_value)
    # print(f"{swim_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(swim_beliefatom)

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"HealerUnit '{healer_name_value}' deleted for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
