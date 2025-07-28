from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_plan_reason_caseunit_str,
    plan_rope_str,
    reason_context_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
)
from src.a08_believer_atom_logic.atom_main import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_plan_reason_caseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_caseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    reason_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    reason_state_value = sue_believer.make_rope(reason_context_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(reason_context_str(), reason_context_value)
    swim_believeratom.set_arg(reason_state_str(), reason_state_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' created for reason '{reason_context_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_caseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_caseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    reason_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    reason_state_value = sue_believer.make_rope(reason_context_value, "dirty")
    reason_divisor_value = 7
    reason_upper_value = 13
    reason_lower_value = 17
    swim_believeratom = believeratom_shop(dimen, INSERT_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(reason_context_str(), reason_context_value)
    swim_believeratom.set_arg(reason_state_str(), reason_state_value)
    swim_believeratom.set_arg("reason_divisor", reason_divisor_value)
    swim_believeratom.set_arg(reason_upper_str(), reason_upper_value)
    swim_believeratom.set_arg(reason_lower_str(), reason_lower_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' created for reason '{reason_context_value}' for plan '{rope_value}'. reason_lower={reason_lower_value}. reason_upper={reason_upper_value}. reason_divisor={reason_divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_caseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_caseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    reason_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    reason_state_value = sue_believer.make_rope(reason_context_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(reason_context_str(), reason_context_value)
    swim_believeratom.set_arg(reason_state_str(), reason_state_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' updated for reason '{reason_context_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_caseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_caseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    reason_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    reason_state_value = sue_believer.make_rope(reason_context_value, "dirty")
    reason_divisor_value = 7
    reason_upper_value = 13
    reason_lower_value = 17
    swim_believeratom = believeratom_shop(dimen, UPDATE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(reason_context_str(), reason_context_value)
    swim_believeratom.set_arg(reason_state_str(), reason_state_value)
    swim_believeratom.set_arg("reason_divisor", reason_divisor_value)
    swim_believeratom.set_arg(reason_upper_str(), reason_upper_value)
    swim_believeratom.set_arg(reason_lower_str(), reason_lower_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' updated for reason '{reason_context_value}' for plan '{rope_value}'. reason_lower={reason_lower_value}. reason_upper={reason_upper_value}. reason_divisor={reason_divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_reason_caseunit_DELETE():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    dimen = believer_plan_reason_caseunit_str()
    casa_rope = sue_believer.make_l1_rope("casa")
    rope_value = sue_believer.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_believer.make_l1_rope("casa")
    reason_context_value = sue_believer.make_rope(casa_rope, "fridge status")
    reason_state_value = sue_believer.make_rope(reason_context_value, "dirty")
    swim_believeratom = believeratom_shop(dimen, DELETE_str())
    swim_believeratom.set_arg(plan_rope_str(), rope_value)
    swim_believeratom.set_arg(reason_context_str(), reason_context_value)
    swim_believeratom.set_arg(reason_state_str(), reason_state_value)
    # print(f"{swim_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(swim_believeratom)

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' deleted from reason '{reason_context_value}' for plan '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
