from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    owner_plan_reason_premiseunit_str,
    plan_rope_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rcontext_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import ownerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reason_premiseunit_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_owner.make_l1_rope("casa")
    rcontext_value = sue_owner.make_rope(casa_rope, "fridge status")
    pstate_value = sue_owner.make_rope(rcontext_value, "dirty")
    swim_owneratom = owneratom_shop(dimen, INSERT_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    swim_owneratom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' created for reason '{rcontext_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reason_premiseunit_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_owner.make_l1_rope("casa")
    rcontext_value = sue_owner.make_rope(casa_rope, "fridge status")
    pstate_value = sue_owner.make_rope(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_owneratom = owneratom_shop(dimen, INSERT_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    swim_owneratom.set_arg(pstate_str(), pstate_value)
    swim_owneratom.set_arg("pdivisor", pdivisor_value)
    swim_owneratom.set_arg(pnigh_str(), pnigh_value)
    swim_owneratom.set_arg(popen_str(), popen_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' created for reason '{rcontext_value}' for plan '{rope_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reason_premiseunit_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_owner.make_l1_rope("casa")
    rcontext_value = sue_owner.make_rope(casa_rope, "fridge status")
    pstate_value = sue_owner.make_rope(rcontext_value, "dirty")
    swim_owneratom = owneratom_shop(dimen, UPDATE_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    swim_owneratom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' updated for reason '{rcontext_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reason_premiseunit_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_owner.make_l1_rope("casa")
    rcontext_value = sue_owner.make_rope(casa_rope, "fridge status")
    pstate_value = sue_owner.make_rope(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_owneratom = owneratom_shop(dimen, UPDATE_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    swim_owneratom.set_arg(pstate_str(), pstate_value)
    swim_owneratom.set_arg("pdivisor", pdivisor_value)
    swim_owneratom.set_arg(pnigh_str(), pnigh_value)
    swim_owneratom.set_arg(popen_str(), popen_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' updated for reason '{rcontext_value}' for plan '{rope_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_premiseunit_DELETE():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_plan_reason_premiseunit_str()
    casa_rope = sue_owner.make_l1_rope("casa")
    rope_value = sue_owner.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_owner.make_l1_rope("casa")
    rcontext_value = sue_owner.make_rope(casa_rope, "fridge status")
    pstate_value = sue_owner.make_rope(rcontext_value, "dirty")
    swim_owneratom = owneratom_shop(dimen, DELETE_str())
    swim_owneratom.set_arg(plan_rope_str(), rope_value)
    swim_owneratom.set_arg(rcontext_str(), rcontext_value)
    swim_owneratom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(swim_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' deleted from reason '{rcontext_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
