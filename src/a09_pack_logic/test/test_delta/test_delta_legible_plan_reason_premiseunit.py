from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_plan_reason_premiseunit_str,
    plan_rope_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rcontext_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_premiseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    rcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    pstate_value = sue_believer.make_rope(rcontext_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(rcontext_str(), rcontext_value)
    swim_believeratom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' created for reason '{rcontext_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_premiseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    rcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    pstate_value = sue_believer.make_rope(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(rcontext_str(), rcontext_value)
    swim_believeratom.set_arg(pstate_str(), pstate_value)
    swim_believeratom.set_arg("pdivisor", pdivisor_value)
    swim_believeratom.set_arg(pnigh_str(), pnigh_value)
    swim_believeratom.set_arg(popen_str(), popen_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' created for reason '{rcontext_value}' for plan '{rope_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_premiseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    rcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    pstate_value = sue_believer.make_rope(rcontext_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(rcontext_str(), rcontext_value)
    swim_believeratom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' updated for reason '{rcontext_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_premiseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    rcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    pstate_value = sue_believer.make_rope(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(rcontext_str(), rcontext_value)
    swim_believeratom.set_arg(pstate_str(), pstate_value)
    swim_believeratom.set_arg("pdivisor", pdivisor_value)
    swim_believeratom.set_arg(pnigh_str(), pnigh_value)
    swim_believeratom.set_arg(popen_str(), popen_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' updated for reason '{rcontext_value}' for plan '{rope_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_DELETE():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_premiseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    rcontext_value = sue_believer.make_rope(casa_rope, "fridge status")
    pstate_value = sue_believer.make_rope(rcontext_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, DELETE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(rcontext_str(), rcontext_value)
    swim_believeratom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' deleted from reason '{rcontext_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
