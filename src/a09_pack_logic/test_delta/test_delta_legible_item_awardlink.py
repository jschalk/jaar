from src.a06_bud_logic._utils.str_a06 import (
    bud_item_awardlink_str,
    awardee_title_str,
    give_force_str,
    take_force_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import atom_update, atom_insert, atom_delete
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list
from src.a06_bud_logic.bud import budunit_shop


def test_create_legible_list_ReturnsObj_item_awardlink_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_awardlink_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    give_force_value = 81
    take_force_value = 43
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_budatom.set_arg(give_force_str(), give_force_value)
    swim_budatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink created for group {awardee_title_value} for item '{road_value}' with give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_awardlink_UPDATE_give_force_take_force():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")

    dimen = bud_item_awardlink_str()
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    give_force_value = 81
    take_force_value = 43
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_budatom.set_arg(give_force_str(), give_force_value)
    swim_budatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for item '{road_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_awardlink_UPDATE_give_force():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_awardlink_str()
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    give_force_value = 81
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_budatom.set_arg(give_force_str(), give_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for item '{road_value}'. Now give_force={give_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_awardlink_UPDATE_take_force():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_awardlink_str()
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")

    take_force_value = 81
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_budatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for item '{road_value}'. Now take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_awardlink_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_awardlink_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    swim_budatom = budatom_shop(dimen, atom_delete())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink for group {awardee_title_value}, item '{road_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
