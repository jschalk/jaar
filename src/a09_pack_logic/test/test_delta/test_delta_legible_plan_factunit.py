from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_plan_factunit_str,
    f_context_str,
    f_lower_str,
    f_state_str,
    f_upper_str,
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
    f_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    f_state_value = sue_believer.make_rope(f_context_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(f_context_str(), f_context_value)
    swim_believeratom.set_arg(f_state_str(), f_state_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit '{f_state_value}' created for r_context '{f_context_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_factunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    r_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    f_state_value = sue_believer.make_rope(r_context_value, "dirty")
    f_upper_value = 13
    f_lower_value = 17
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(f_context_str(), r_context_value)
    swim_believeratom.set_arg(f_state_str(), f_state_value)
    swim_believeratom.set_arg(f_upper_str(), f_upper_value)
    swim_believeratom.set_arg(f_lower_str(), f_lower_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit '{f_state_value}' created for r_context '{r_context_value}' for plan '{rope_value}'. f_lower={f_lower_value}. f_upper={f_upper_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_factunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    r_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    f_state_value = sue_believer.make_rope(r_context_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(f_context_str(), r_context_value)
    swim_believeratom.set_arg(f_state_str(), f_state_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit '{f_state_value}' updated for r_context '{r_context_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_factunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    r_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    f_state_value = sue_believer.make_rope(r_context_value, "dirty")
    f_upper_value = 13
    f_lower_value = 17
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(f_context_str(), r_context_value)
    swim_believeratom.set_arg(f_state_str(), f_state_value)
    swim_believeratom.set_arg(f_upper_str(), f_upper_value)
    swim_believeratom.set_arg(f_lower_str(), f_lower_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit '{f_state_value}' updated for r_context '{r_context_value}' for plan '{rope_value}'. f_lower={f_lower_value}. f_upper={f_upper_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_factunit_DELETE():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_factunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    r_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    swim_believeratom = believeratom_shop(dimen, DELETE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(f_context_str(), r_context_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"FactUnit r_context '{r_context_value}' deleted for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
