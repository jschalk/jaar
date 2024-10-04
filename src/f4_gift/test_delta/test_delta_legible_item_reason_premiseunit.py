from src.f2_bud.bud_tool import bud_item_reason_premiseunit_str
from src.f4_gift.atom_config import atom_update, atom_insert, atom_delete
from src.f4_gift.atom import atomunit_shop
from src.f4_gift.delta import deltaunit_shop
from src.f4_gift.legible import create_legible_list
from src.f2_bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reason_premiseunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    need_str = "need"
    need_value = sue_bud.make_road(base_value, "dirty")
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    swim_atomunit.set_arg(need_str, need_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reason_premiseunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    need_str = "need"
    need_value = sue_bud.make_road(base_value, "dirty")
    divisor_str = "divisor"
    nigh_str = "nigh"
    open_str = "open"
    divisor_value = 7
    nigh_value = 13
    open_value = 17
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    swim_atomunit.set_arg(need_str, need_value)
    swim_atomunit.set_arg(divisor_str, divisor_value)
    swim_atomunit.set_arg(nigh_str, nigh_value)
    swim_atomunit.set_arg(open_str, open_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for item '{road_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reason_premiseunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    need_str = "need"
    need_value = sue_bud.make_road(base_value, "dirty")
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    swim_atomunit.set_arg(need_str, need_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reason_premiseunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    need_str = "need"
    need_value = sue_bud.make_road(base_value, "dirty")
    divisor_str = "divisor"
    nigh_str = "nigh"
    open_str = "open"
    divisor_value = 7
    nigh_value = 13
    open_value = 17
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    swim_atomunit.set_arg(need_str, need_value)
    swim_atomunit.set_arg(divisor_str, divisor_value)
    swim_atomunit.set_arg(nigh_str, nigh_value)
    swim_atomunit.set_arg(open_str, open_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for item '{road_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_item_reason_premiseunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    need_str = "need"
    need_value = sue_bud.make_road(base_value, "dirty")
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_str, road_value)
    swim_atomunit.set_arg(base_str, base_value)
    swim_atomunit.set_arg(need_str, need_value)
    # print(f"{swim_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' deleted from reason '{base_value}' for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str