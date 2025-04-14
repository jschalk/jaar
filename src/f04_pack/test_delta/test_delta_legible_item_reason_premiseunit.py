from src.f02_bud.bud_tool import bud_item_reason_premiseunit_str
from src.f04_pack.atom_config import atom_update, atom_insert, atom_delete
from src.f04_pack.atom import budatom_shop
from src.f04_pack.delta import buddelta_shop
from src.f04_pack.legible import create_legible_list
from src.f02_bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_reason_premiseunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    need_str = "need"
    need_value = sue_bud.make_road(base_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    swim_budatom.set_arg(need_str, need_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_reason_premiseunit_str()
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
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    swim_budatom.set_arg(need_str, need_value)
    swim_budatom.set_arg(divisor_str, divisor_value)
    swim_budatom.set_arg(nigh_str, nigh_value)
    swim_budatom.set_arg(open_str, open_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for item '{road_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_reason_premiseunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    need_str = "need"
    need_value = sue_bud.make_road(base_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    swim_budatom.set_arg(need_str, need_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_reason_premiseunit_str()
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
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    swim_budatom.set_arg(need_str, need_value)
    swim_budatom.set_arg(divisor_str, divisor_value)
    swim_budatom.set_arg(nigh_str, nigh_value)
    swim_budatom.set_arg(open_str, open_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for item '{road_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_item_reason_premiseunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_item_reason_premiseunit_str()
    road_str = "road"
    casa_road = sue_bud.make_l1_road("casa")
    road_value = sue_bud.make_road(casa_road, "clean fridge")
    base_str = "base"
    casa_road = sue_bud.make_l1_road("casa")
    base_value = sue_bud.make_road(casa_road, "fridge status")
    need_str = "need"
    need_value = sue_bud.make_road(base_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_delete())
    swim_budatom.set_arg(road_str, road_value)
    swim_budatom.set_arg(base_str, base_value)
    swim_budatom.set_arg(need_str, need_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{need_value}' deleted from reason '{base_value}' for item '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
