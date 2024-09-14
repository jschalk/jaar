from src.s2_bud.bud_tool import bud_idea_teamlink_str
from src.s4_gift.atom_config import atom_insert, atom_delete, group_id_str
from src.s4_gift.atom import atomunit_shop
from src.s4_gift.delta import deltaunit_shop
from src.s4_gift.legible import create_legible_list
from src.s2_bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_teamlink_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_teamlink_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    group_id_value = f"{sue_bud._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(group_id_str(), group_id_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"teamlink '{group_id_value}' created for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_teamlink_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_teamlink_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    group_id_value = f"{sue_bud._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(group_id_str(), group_id_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"teamlink '{group_id_value}' deleted for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
