from src.bud.bud_tool import bud_idea_healerlink_str
from src.change.atom_config import atom_insert, atom_delete, healer_id_str
from src.change.atom import atomunit_shop
from src.change.change import changeunit_shop
from src.change.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_healerlink_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_healerlink_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    healer_id_value = f"{sue_bud._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(healer_id_str(), healer_id_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"HealerLink '{healer_id_value}' created for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_healerlink_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_idea_healerlink_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    healer_id_value = f"{sue_bud._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(healer_id_str(), healer_id_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"HealerLink '{healer_id_value}' deleted for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
