from src.a06_plan_logic._test_util.a06_str import (
    concept_rope_str,
    plan_concept_reason_premiseunit_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rcontext_str,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a08_plan_atom_logic._test_util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a09_pack_logic.delta import plandelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reason_premiseunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    rcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    pstate_value = sue_plan.make_rope(rcontext_value, "dirty")
    swim_planatom = planatom_shop(dimen, INSERT_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    swim_planatom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' created for reason '{rcontext_value}' for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reason_premiseunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    rcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    pstate_value = sue_plan.make_rope(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_planatom = planatom_shop(dimen, INSERT_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    swim_planatom.set_arg(pstate_str(), pstate_value)
    swim_planatom.set_arg("pdivisor", pdivisor_value)
    swim_planatom.set_arg(pnigh_str(), pnigh_value)
    swim_planatom.set_arg(popen_str(), popen_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' created for reason '{rcontext_value}' for concept '{rope_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reason_premiseunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    rcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    pstate_value = sue_plan.make_rope(rcontext_value, "dirty")
    swim_planatom = planatom_shop(dimen, UPDATE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    swim_planatom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' updated for reason '{rcontext_value}' for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reason_premiseunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    rcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    pstate_value = sue_plan.make_rope(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_planatom = planatom_shop(dimen, UPDATE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    swim_planatom.set_arg(pstate_str(), pstate_value)
    swim_planatom.set_arg("pdivisor", pdivisor_value)
    swim_planatom.set_arg(pnigh_str(), pnigh_value)
    swim_planatom.set_arg(popen_str(), popen_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' updated for reason '{rcontext_value}' for concept '{rope_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_reason_premiseunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    rcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    pstate_value = sue_plan.make_rope(rcontext_value, "dirty")
    swim_planatom = planatom_shop(dimen, DELETE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(rcontext_str(), rcontext_value)
    swim_planatom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' deleted from reason '{rcontext_value}' for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
