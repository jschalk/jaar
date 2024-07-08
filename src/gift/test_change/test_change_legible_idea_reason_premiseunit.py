from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_INSERT_WithOutNumericArgs():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reason_premiseunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_world.make_l1_road("casa")
    base_value = sue_world.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_world.make_road(base_value, "dirty")
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(need_text, need_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_INSERT_WithNumericArgs():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reason_premiseunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_world.make_l1_road("casa")
    base_value = sue_world.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_world.make_road(base_value, "dirty")
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    divisor_value = 7
    nigh_value = 13
    open_value = 17
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(need_text, need_value)
    swim_atomunit.set_arg(divisor_text, divisor_value)
    swim_atomunit.set_arg(nigh_text, nigh_value)
    swim_atomunit.set_arg(open_text, open_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for idea '{road_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_UPDATE_WithOutNumericArgs():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reason_premiseunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_world.make_l1_road("casa")
    base_value = sue_world.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_world.make_road(base_value, "dirty")
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(need_text, need_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_UPDATE_WithNumericArgs():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reason_premiseunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_world.make_l1_road("casa")
    base_value = sue_world.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_world.make_road(base_value, "dirty")
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    divisor_value = 7
    nigh_value = 13
    open_value = 17
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(need_text, need_value)
    swim_atomunit.set_arg(divisor_text, divisor_value)
    swim_atomunit.set_arg(nigh_text, nigh_value)
    swim_atomunit.set_arg(open_text, open_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for idea '{road_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_DELETE():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reason_premiseunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_world.make_l1_road("casa")
    base_value = sue_world.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_world.make_road(base_value, "dirty")
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(need_text, need_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"PremiseUnit '{need_value}' deleted from reason '{base_value}' for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
