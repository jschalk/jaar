from src.f02_bud.bud_tool import bud_item_healerlink_str
from src.f04_gift.atom_config import atom_insert, atom_delete, healer_name_str
from src.f04_gift.atom import atomunit_shop
from src.f04_gift.delta import buddelta_shop
from src.f04_gift.legible import create_legible_list
from src.f02_bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_item_healerlink_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_healerlink_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    healer_name_value = f"{sue_bud.bridge}Swimmers"
    swim_atomunit = atomunit_shop(dimen, atom_insert())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(healer_name_str(), healer_name_value)
    # print(f"{swim_atomunit=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"HealerLink '{healer_name_value}' created for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_healerlink_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_healerlink_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    healer_name_value = f"{sue_bud.bridge}Swimmers"
    swim_atomunit = atomunit_shop(dimen, atom_delete())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(healer_name_str(), healer_name_value)
    # print(f"{swim_atomunit=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"HealerLink '{healer_name_value}' deleted for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
