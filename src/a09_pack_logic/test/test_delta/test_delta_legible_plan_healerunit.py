from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_plan_healerunit_str,
    healer_name_str,
    plan_rope_str,
)
from src.a08_believer_atom_logic.atom_main import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import DELETE_str, INSERT_str
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_healerunit_INSERT():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_healerunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    healer_name_value = f"{sue_believer.knot}Swimmers"
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(healer_name_str(), healer_name_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"HealerUnit '{healer_name_value}' created for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_healerunit_DELETE():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_healerunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    healer_name_value = f"{sue_believer.knot}Swimmers"
    swim_believeratom = believeratom_shop(dimen, DELETE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(healer_name_str(), healer_name_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"HealerUnit '{healer_name_value}' deleted for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
