from src.bud.bud_tool import bud_idea_factunit_text
from src.gift.atom_config import (
    atom_update,
    atom_insert,
    atom_delete,
    fnigh_str,
    fopen_str,
)
from src.gift.atom import atomunit_shop
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_factunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_factunit_text()
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    pick_text = "pick"
    pick_value = sue_bud.make_road(base_value, "dirty")
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(pick_text, pick_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"FactUnit '{pick_value}' created for base '{base_value}' for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_factunit_text()
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    pick_text = "pick"
    pick_value = sue_bud.make_road(base_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(pick_text, pick_value)
    swim_atomunit.set_arg(fnigh_str(), fnigh_value)
    swim_atomunit.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"FactUnit '{pick_value}' created for base '{base_value}' for idea '{road_value}'. fOpen={fopen_value}. fNigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_factunit_text()
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    pick_text = "pick"
    pick_value = sue_bud.make_road(base_value, "dirty")
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(pick_text, pick_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"FactUnit '{pick_value}' updated for base '{base_value}' for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_factunit_text()
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    pick_text = "pick"
    pick_value = sue_bud.make_road(base_value, "dirty")
    fnigh_value = 13
    fopen_value = 17
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(pick_text, pick_value)
    swim_atomunit.set_arg(fnigh_str(), fnigh_value)
    swim_atomunit.set_arg(fopen_str(), fopen_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"FactUnit '{pick_value}' updated for base '{base_value}' for idea '{road_value}'. fOpen={fopen_value}. fNigh={fnigh_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_factunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_factunit_text()
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    pick_text = "pick"
    pick_value = sue_bud.make_road(base_value, "dirty")
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(pick_text, pick_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"FactUnit '{pick_value}' deleted from base '{base_value}' for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
