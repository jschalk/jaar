from src.a06_plan_logic._test_util.a06_str import (
    concept_rope_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    plan_concept_factunit_str,
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


def test_create_legible_list_ReturnsObj_concept_factunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_factunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    fcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    fstate_value = sue_plan.make_rope(fcontext_value, "dirty")
    swim_planatom = planatom_shop(dimen, INSERT_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(fcontext_str(), fcontext_value)
    swim_planatom.set_arg(fstate_str(), fstate_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit '{fstate_value}' created for rcontext '{fcontext_value}' for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_factunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    rcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    fstate_value = sue_plan.make_rope(rcontext_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_planatom = planatom_shop(dimen, INSERT_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(fcontext_str(), rcontext_value)
    swim_planatom.set_arg(fstate_str(), fstate_value)
    swim_planatom.set_arg(fnigh_str(), fnigh_value)
    swim_planatom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit '{fstate_value}' created for rcontext '{rcontext_value}' for concept '{rope_value}'. fopen={fopen_value}. fnigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_factunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    rcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    fstate_value = sue_plan.make_rope(rcontext_value, "dirty")
    swim_planatom = planatom_shop(dimen, UPDATE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(fcontext_str(), rcontext_value)
    swim_planatom.set_arg(fstate_str(), fstate_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit '{fstate_value}' updated for rcontext '{rcontext_value}' for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_factunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    rcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    fstate_value = sue_plan.make_rope(rcontext_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_planatom = planatom_shop(dimen, UPDATE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(fcontext_str(), rcontext_value)
    swim_planatom.set_arg(fstate_str(), fstate_value)
    swim_planatom.set_arg(fnigh_str(), fnigh_value)
    swim_planatom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit '{fstate_value}' updated for rcontext '{rcontext_value}' for concept '{rope_value}'. fopen={fopen_value}. fnigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_factunit_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_concept_factunit_str()
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    rcontext_value = sue_plan.make_rope(casa_rope, "fridge status")
    swim_planatom = planatom_shop(dimen, DELETE_str())
    swim_planatom.set_arg(concept_rope_str(), rope_value)
    swim_planatom.set_arg(fcontext_str(), rcontext_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit rcontext '{rcontext_value}' deleted for concept '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
