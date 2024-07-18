from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_awardlink_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_idea_awardlink"
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    lobby_id_text = "lobby_id"
    lobby_id_value = f"{sue_bud._road_delimiter}Swimmers"
    give_weight_text = "give_weight"
    take_weight_text = "take_weight"
    give_weight_value = 81
    take_weight_value = 43
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(lobby_id_text, lobby_id_value)
    swim_atomunit.set_arg(give_weight_text, give_weight_value)
    swim_atomunit.set_arg(take_weight_text, take_weight_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Awardlink created for lobby {lobby_id_value} for idea '{road_value}' with give_weight={give_weight_value} and take_weight={take_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_awardlink_UPDATE_give_weight_take_weight():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")

    category = "bud_idea_awardlink"
    lobby_id_text = "lobby_id"
    lobby_id_value = f"{sue_bud._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    give_weight_text = "give_weight"
    take_weight_text = "take_weight"
    give_weight_value = 81
    take_weight_value = 43
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(lobby_id_text, lobby_id_value)
    swim_atomunit.set_arg(give_weight_text, give_weight_value)
    swim_atomunit.set_arg(take_weight_text, take_weight_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Awardlink has been transited for lobby {lobby_id_value} for idea '{road_value}'. Now give_weight={give_weight_value} and take_weight={take_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_awardlink_UPDATE_give_weight():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_idea_awardlink"
    lobby_id_text = "lobby_id"
    lobby_id_value = f"{sue_bud._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    give_weight_text = "give_weight"
    give_weight_value = 81
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(lobby_id_text, lobby_id_value)
    swim_atomunit.set_arg(give_weight_text, give_weight_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Awardlink has been transited for lobby {lobby_id_value} for idea '{road_value}'. Now give_weight={give_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_awardlink_UPDATE_take_weight():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_idea_awardlink"
    lobby_id_text = "lobby_id"
    lobby_id_value = f"{sue_bud._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    take_weight_text = "take_weight"
    take_weight_value = 81
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(lobby_id_text, lobby_id_value)
    swim_atomunit.set_arg(take_weight_text, take_weight_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Awardlink has been transited for lobby {lobby_id_value} for idea '{road_value}'. Now take_weight={take_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_awardlink_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_idea_awardlink"
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    lobby_id_text = "lobby_id"
    lobby_id_value = f"{sue_bud._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(lobby_id_text, lobby_id_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = (
        f"Awardlink for lobby {lobby_id_value}, idea '{road_value}' has been deleted."
    )
    print(f"{x_str=}")
    assert legible_list[0] == x_str
