from src.a06_bud_logic.bud_tool import bud_item_factunit_str
from src.a08_bud_atom_logic.atom_config import (
    atom_update,
    atom_insert,
    atom_delete,
    fnigh_str,
    fopen_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop
from src.f04_pack.delta import buddelta_shop
from src.f04_pack.legible import create_legible_list
from src.a06_bud_logic.bud import budunit_shop


def test_create_legible_list_ReturnsObj_item_factunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    pick_str = "pick"
    pick_value = sue_bud.make_road(base_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    swim_budatom.set_arg(pick_str, pick_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{pick_value}' created for base '{base_value}' for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    pick_str = "pick"
    pick_value = sue_bud.make_road(base_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    swim_budatom.set_arg(pick_str, pick_value)
    swim_budatom.set_arg(fnigh_str(), fnigh_value)
    swim_budatom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{pick_value}' created for base '{base_value}' for item '{road_value}'. fOpen={fopen_value}. fNigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    pick_str = "pick"
    pick_value = sue_bud.make_road(base_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    swim_budatom.set_arg(pick_str, pick_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{pick_value}' updated for base '{base_value}' for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    pick_str = "pick"
    pick_value = sue_bud.make_road(base_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    swim_budatom.set_arg(pick_str, pick_value)
    swim_budatom.set_arg(fnigh_str(), fnigh_value)
    swim_budatom.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit '{pick_value}' updated for base '{base_value}' for item '{road_value}'. fOpen={fopen_value}. fNigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_factunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_factunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    swim_budatom = budatom_shop(dimen, atom_delete())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"FactUnit base '{base_value}' deleted for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
