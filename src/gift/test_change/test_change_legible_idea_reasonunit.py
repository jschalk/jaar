from src.bud.bud_tool import bud_idea_reasonunit_str
from src.gift.atom_config import (
    atom_update,
    atom_insert,
    atom_delete,
    base_idea_active_requisite_str,
)
from src.gift.atom import atomunit_shop
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_With_base_idea_active_requisite():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_reasonunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    base_value = f"{sue_bud._road_delimiter}Swimmers"
    base_idea_active_requisite_value = True
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    swim_atomunit.set_arg(
        base_idea_active_requisite_str(), base_idea_active_requisite_value
    )
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit created for idea '{road_value}' with base '{base_value}'. base_idea_active_requisite={base_idea_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_Without_base_idea_active_requisite():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_reasonunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    base_value = f"{sue_bud._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit created for idea '{road_value}' with base '{base_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_base_idea_active_requisite_IsTrue():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_reasonunit_str()
    base_str = "base"
    base_value = f"{sue_bud._road_delimiter}Swimmers"
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_idea_active_requisite_value = True
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    swim_atomunit.set_arg(
        base_idea_active_requisite_str(), base_idea_active_requisite_value
    )
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' transited with base_idea_active_requisite={base_idea_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_base_idea_active_requisite_IsNone():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_reasonunit_str()
    base_str = "base"
    base_value = f"{sue_bud._road_delimiter}Swimmers"
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' and no longer checks base active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_reasonunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    base_value = f"{sue_bud._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
