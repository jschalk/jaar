from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._test_util.a06_str import (
    bud_concept_reason_premiseunit_str,
    concept_way_str,
    rcontext_str,
    pstate_str,
    pnigh_str,
    popen_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import (
    UPDATE_str,
    INSERT_str,
    DELETE_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pstate_value = sue_bud.make_way(rcontext_value, "dirty")
    swim_budatom = budatom_shop(dimen, INSERT_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' created for reason '{rcontext_value}' for concept '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pstate_value = sue_bud.make_way(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_budatom = budatom_shop(dimen, INSERT_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pstate_str(), pstate_value)
    swim_budatom.set_arg("pdivisor", pdivisor_value)
    swim_budatom.set_arg(pnigh_str(), pnigh_value)
    swim_budatom.set_arg(popen_str(), popen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' created for reason '{rcontext_value}' for concept '{way_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pstate_value = sue_bud.make_way(rcontext_value, "dirty")
    swim_budatom = budatom_shop(dimen, UPDATE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' updated for reason '{rcontext_value}' for concept '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pstate_value = sue_bud.make_way(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_budatom = budatom_shop(dimen, UPDATE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pstate_str(), pstate_value)
    swim_budatom.set_arg("pdivisor", pdivisor_value)
    swim_budatom.set_arg(pnigh_str(), pnigh_value)
    swim_budatom.set_arg(popen_str(), popen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' updated for reason '{rcontext_value}' for concept '{way_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_reason_premiseunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pstate_value = sue_bud.make_way(rcontext_value, "dirty")
    swim_budatom = budatom_shop(dimen, DELETE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pstate_str(), pstate_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pstate_value}' deleted from reason '{rcontext_value}' for concept '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
