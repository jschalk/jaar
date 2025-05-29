from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._test_util.a06_str import (
    bud_concept_factunit_str,
    fnigh_str,
    fopen_str,
    concept_way_str,
    fcontext_str,
    fstate_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import (
    UPDATE_str,
    INSERT_str,
    DELETE_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_factunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    fcontext_value = sue_bud.make_way(casa_way, "fridge status")
    fstate_value = sue_bud.make_way(fcontext_value, "dirty")
    swim_budatom = budatom_shop(dimen, INSERT_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(fcontext_str(), fcontext_value)
    swim_budatom.set_arg(fstate_str(), fstate_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{fstate_value}' created for rcontext '{fcontext_value}' for concept '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    fstate_value = sue_bud.make_way(rcontext_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_budatom = budatom_shop(dimen, INSERT_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(fcontext_str(), rcontext_value)
    swim_budatom.set_arg(fstate_str(), fstate_value)
    swim_budatom.set_arg(fnigh_str(), fnigh_value)
    swim_budatom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{fstate_value}' created for rcontext '{rcontext_value}' for concept '{way_value}'. fopen={fopen_value}. fnigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    fstate_value = sue_bud.make_way(rcontext_value, "dirty")
    swim_budatom = budatom_shop(dimen, UPDATE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(fcontext_str(), rcontext_value)
    swim_budatom.set_arg(fstate_str(), fstate_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{fstate_value}' updated for rcontext '{rcontext_value}' for concept '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    fstate_value = sue_bud.make_way(rcontext_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_budatom = budatom_shop(dimen, UPDATE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(fcontext_str(), rcontext_value)
    swim_budatom.set_arg(fstate_str(), fstate_value)
    swim_budatom.set_arg(fnigh_str(), fnigh_value)
    swim_budatom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{fstate_value}' updated for rcontext '{rcontext_value}' for concept '{way_value}'. fopen={fopen_value}. fnigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_factunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    swim_budatom = budatom_shop(dimen, DELETE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(fcontext_str(), rcontext_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit rcontext '{rcontext_value}' deleted for concept '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
