from src.gift.atom import atomunit_shop, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_range_push_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_idea_range_push"
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    range_push_text = "range_push"
    range_push_value = sue_bud.make_l1_road("fridge metrics")
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(range_push_text, range_push_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"range_push '{range_push_value}' created for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_range_push_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_idea_range_push"
    road_text = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    range_push_text = "range_push"
    range_push_value = sue_bud.make_l1_road("fridge metrics")
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(range_push_text, range_push_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"range_push '{range_push_value}' deleted for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
