from src.a06_bud_logic._utils.str_a06 import (
    bud_idea_reason_premiseunit_str,
    idea_way_str,
    context_str,
    branch_str,
    nigh_str,
    open_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import atom_update, atom_insert, atom_delete
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list
from src.a06_bud_logic.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    context_value = sue_bud.make_way(casa_way, "fridge status")
    branch_value = sue_bud.make_way(context_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    swim_budatom.set_arg(branch_str(), branch_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{branch_value}' created for reason '{context_value}' for idea '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    context_value = sue_bud.make_way(casa_way, "fridge status")
    branch_value = sue_bud.make_way(context_value, "dirty")
    divisor_value = 7
    nigh_value = 13
    open_value = 17
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    swim_budatom.set_arg(branch_str(), branch_value)
    swim_budatom.set_arg("divisor", divisor_value)
    swim_budatom.set_arg(nigh_str(), nigh_value)
    swim_budatom.set_arg(open_str(), open_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{branch_value}' created for reason '{context_value}' for idea '{way_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    context_value = sue_bud.make_way(casa_way, "fridge status")
    branch_value = sue_bud.make_way(context_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    swim_budatom.set_arg(branch_str(), branch_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{branch_value}' updated for reason '{context_value}' for idea '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    context_value = sue_bud.make_way(casa_way, "fridge status")
    branch_value = sue_bud.make_way(context_value, "dirty")
    divisor_value = 7
    nigh_value = 13
    open_value = 17
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    swim_budatom.set_arg(branch_str(), branch_value)
    swim_budatom.set_arg("divisor", divisor_value)
    swim_budatom.set_arg(nigh_str(), nigh_value)
    swim_budatom.set_arg(open_str(), open_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{branch_value}' updated for reason '{context_value}' for idea '{way_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    context_value = sue_bud.make_way(casa_way, "fridge status")
    branch_value = sue_bud.make_way(context_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_delete())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    swim_budatom.set_arg(branch_str(), branch_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{branch_value}' deleted from reason '{context_value}' for idea '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
