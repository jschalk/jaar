from src.a06_bud_logic._utils.str_a06 import (
    bud_item_factunit_str,
    fnigh_str,
    fopen_str,
    way_str,
    fbase_str,
    fneed_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import atom_update, atom_insert, atom_delete
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list
from src.a06_bud_logic.bud import budunit_shop


def test_create_legible_list_ReturnsObj_item_factunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    fbase_value = sue_bud.make_way(casa_way, "fridge status")
    fneed_value = sue_bud.make_way(fbase_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(way_str(), way_value)
    swim_budatom.set_arg(fbase_str(), fbase_value)
    swim_budatom.set_arg(fneed_str(), fneed_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{fneed_value}' created for base '{fbase_value}' for item '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    base_value = sue_bud.make_way(casa_way, "fridge status")
    fneed_value = sue_bud.make_way(base_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(way_str(), way_value)
    swim_budatom.set_arg(fbase_str(), base_value)
    swim_budatom.set_arg(fneed_str(), fneed_value)
    swim_budatom.set_arg(fnigh_str(), fnigh_value)
    swim_budatom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{fneed_value}' created for base '{base_value}' for item '{way_value}'. fopen={fopen_value}. fnigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    base_value = sue_bud.make_way(casa_way, "fridge status")
    fneed_value = sue_bud.make_way(base_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(way_str(), way_value)
    swim_budatom.set_arg(fbase_str(), base_value)
    swim_budatom.set_arg(fneed_str(), fneed_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{fneed_value}' updated for base '{base_value}' for item '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    base_value = sue_bud.make_way(casa_way, "fridge status")
    fneed_value = sue_bud.make_way(base_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(way_str(), way_value)
    swim_budatom.set_arg(fbase_str(), base_value)
    swim_budatom.set_arg(fneed_str(), fneed_value)
    swim_budatom.set_arg(fnigh_str(), fnigh_value)
    swim_budatom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{fneed_value}' updated for base '{base_value}' for item '{way_value}'. fopen={fopen_value}. fnigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_factunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    base_value = sue_bud.make_way(casa_way, "fridge status")
    swim_budatom = budatom_shop(dimen, atom_delete())
    swim_budatom.set_arg(way_str(), way_value)
    swim_budatom.set_arg(fbase_str(), base_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit base '{base_value}' deleted for item '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
