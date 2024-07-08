from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_idea_fiscallink_INSERT():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_fiscallink"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_world._road_delimiter}Swimmers"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(belief_id_text, belief_id_value)
    swim_atomunit.set_arg(credor_weight_text, credor_weight_value)
    swim_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Fiscallink created for belief {belief_id_value} for idea '{road_value}' with credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_fiscallink_UPDATE_credor_weight_debtor_weight():
    # GIVEN
    sue_world = worldunit_shop("Sue")

    category = "world_idea_fiscallink"
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_world._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(belief_id_text, belief_id_value)
    swim_atomunit.set_arg(credor_weight_text, credor_weight_value)
    swim_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Fiscallink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_fiscallink_UPDATE_credor_weight():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_fiscallink"
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_world._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    credor_weight_text = "credor_weight"
    credor_weight_value = 81
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(belief_id_text, belief_id_value)
    swim_atomunit.set_arg(credor_weight_text, credor_weight_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Fiscallink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_fiscallink_UPDATE_debtor_weight():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_fiscallink"
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_world._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    debtor_weight_text = "debtor_weight"
    debtor_weight_value = 81
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(belief_id_text, belief_id_value)
    swim_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Fiscallink has been transited for belief {belief_id_value} for idea '{road_value}'. Now debtor_weight={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_fiscallink_DELETE():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_fiscallink"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_world._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(belief_id_text, belief_id_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Fiscallink for belief {belief_id_value}, idea '{road_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
