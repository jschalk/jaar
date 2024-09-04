from src.gift.atom_config import (
    atom_insert,
    atom_delete,
    bud_idea_teamlink_text,
    group_id_str,
)
from src.gift.atom import atomunit_shop
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_teamlink_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_teamlink_text()
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    group_id_value = f"{sue_bud._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(group_id_str(), group_id_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"teamlink '{group_id_value}' created for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_teamlink_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_teamlink_text()
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    group_id_value = f"{sue_bud._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(group_id_str(), group_id_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"teamlink '{group_id_value}' deleted for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
