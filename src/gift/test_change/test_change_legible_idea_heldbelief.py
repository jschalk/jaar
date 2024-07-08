from src.gift.atom import atomunit_shop, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_idea_heldbelief_INSERT():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_heldbelief"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_world._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(belief_id_text, belief_id_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"heldbelief '{belief_id_value}' created for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_heldbelief_DELETE():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_heldbelief"
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
    x_str = f"heldbelief '{belief_id_value}' deleted for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
