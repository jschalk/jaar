from src.a06_bud_logic._utils.str_a06 import (
    bud_idea_reason_premiseunit_str,
    idea_way_str,
    rcontext_str,
    pbranch_str,
    pnigh_str,
    popen_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import atom_update, atom_insert, atom_delete
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list
from src.a06_bud_logic.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pbranch_value = sue_bud.make_way(rcontext_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pbranch_str(), pbranch_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pbranch_value}' created for reason '{rcontext_value}' for idea '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pbranch_value = sue_bud.make_way(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pbranch_str(), pbranch_value)
    swim_budatom.set_arg("pdivisor", pdivisor_value)
    swim_budatom.set_arg(pnigh_str(), pnigh_value)
    swim_budatom.set_arg(popen_str(), popen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pbranch_value}' created for reason '{rcontext_value}' for idea '{way_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pbranch_value = sue_bud.make_way(rcontext_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pbranch_str(), pbranch_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pbranch_value}' updated for reason '{rcontext_value}' for idea '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pbranch_value = sue_bud.make_way(rcontext_value, "dirty")
    pdivisor_value = 7
    pnigh_value = 13
    popen_value = 17
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pbranch_str(), pbranch_value)
    swim_budatom.set_arg("pdivisor", pdivisor_value)
    swim_budatom.set_arg(pnigh_str(), pnigh_value)
    swim_budatom.set_arg(popen_str(), popen_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pbranch_value}' updated for reason '{rcontext_value}' for idea '{way_value}'. Popen={popen_value}. Pnigh={pnigh_value}. Pdivisor={pdivisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reason_premiseunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reason_premiseunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    casa_way = sue_bud.make_l1_way("casa")
    rcontext_value = sue_bud.make_way(casa_way, "fridge status")
    pbranch_value = sue_bud.make_way(rcontext_value, "dirty")
    swim_budatom = budatom_shop(dimen, atom_delete())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(rcontext_str(), rcontext_value)
    swim_budatom.set_arg(pbranch_str(), pbranch_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"PremiseUnit '{pbranch_value}' deleted from reason '{rcontext_value}' for idea '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
