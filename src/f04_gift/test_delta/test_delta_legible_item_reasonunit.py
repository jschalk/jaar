from src.f02_bud.bud_tool import bud_item_reasonunit_str
from src.f04_gift.atom_config import (
    atom_update,
    atom_insert,
    atom_delete,
    base_item_active_requisite_str,
)
from src.f04_gift.atom import atomunit_shop
from src.f04_gift.delta import deltaunit_shop
from src.f04_gift.legible import create_legible_list
from src.f02_bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_item_reasonunit_INSERT_With_base_item_active_requisite():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reasonunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    base_value = f"{sue_bud._wall}Swimmers"
    base_item_active_requisite_value = True
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    swim_atomunit.set_arg(
        base_item_active_requisite_str(), base_item_active_requisite_value
    )
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit created for item '{road_value}' with base '{base_value}'. base_item_active_requisite={base_item_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reasonunit_INSERT_Without_base_item_active_requisite():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reasonunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    base_value = f"{sue_bud._wall}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit created for item '{road_value}' with base '{base_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reasonunit_UPDATE_base_item_active_requisite_IsTrue():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reasonunit_str()
    base_str = "base"
    base_value = f"{sue_bud._wall}Swimmers"
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_item_active_requisite_value = True
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    swim_atomunit.set_arg(
        base_item_active_requisite_str(), base_item_active_requisite_value
    )
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for item '{road_value}' set with base_item_active_requisite={base_item_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reasonunit_UPDATE_base_item_active_requisite_IsNone():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reasonunit_str()
    base_str = "base"
    base_value = f"{sue_bud._wall}Swimmers"
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for item '{road_value}' and no longer checks base active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reasonunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reasonunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    base_value = f"{sue_bud._wall}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for item '{road_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
