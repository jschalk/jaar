from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_plan_factunit_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    plan_rope_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_factunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_factunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    fcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    fstate_value = sue_believer.make_rope(fcontext_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(fcontext_str(), fcontext_value)
    swim_believeratom.set_arg(fstate_str(), fstate_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit '{fstate_value}' created for rcontext '{fcontext_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_factunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    rcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    fstate_value = sue_believer.make_rope(rcontext_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(fcontext_str(), rcontext_value)
    swim_believeratom.set_arg(fstate_str(), fstate_value)
    swim_believeratom.set_arg(fnigh_str(), fnigh_value)
    swim_believeratom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit '{fstate_value}' created for rcontext '{rcontext_value}' for plan '{rope_value}'. fopen={fopen_value}. fnigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_factunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    rcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    fstate_value = sue_believer.make_rope(rcontext_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(fcontext_str(), rcontext_value)
    swim_believeratom.set_arg(fstate_str(), fstate_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit '{fstate_value}' updated for rcontext '{rcontext_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_factunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    rcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    fstate_value = sue_believer.make_rope(rcontext_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(fcontext_str(), rcontext_value)
    swim_believeratom.set_arg(fstate_str(), fstate_value)
    swim_believeratom.set_arg(fnigh_str(), fnigh_value)
    swim_believeratom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit '{fstate_value}' updated for rcontext '{rcontext_value}' for plan '{rope_value}'. fopen={fopen_value}. fnigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_DELETE():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_factunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    rcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    swim_believeratom = believeratom_shop(dimen, DELETE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(fcontext_str(), rcontext_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit rcontext '{rcontext_value}' deleted for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
