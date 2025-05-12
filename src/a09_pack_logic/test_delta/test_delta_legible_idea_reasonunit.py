from src.a06_bud_logic._utils.str_a06 import (
    bud_idea_reasonunit_str,
    context_idea_active_requisite_str,
    context_str,
    idea_way_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import atom_update, atom_insert, atom_delete
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list
from src.a06_bud_logic.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_With_context_idea_active_requisite():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reasonunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    context_value = f"{sue_bud.bridge}Swimmers"
    context_idea_active_requisite_value = True
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    swim_budatom.set_arg(
        context_idea_active_requisite_str(), context_idea_active_requisite_value
    )
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"ReasonUnit created for idea '{way_value}' with context '{context_value}'. context_idea_active_requisite={context_idea_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_Without_context_idea_active_requisite():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reasonunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    context_value = f"{sue_bud.bridge}Swimmers"
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"ReasonUnit created for idea '{way_value}' with context '{context_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_context_idea_active_requisite_IsTrue():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reasonunit_str()
    context_value = f"{sue_bud.bridge}Swimmers"
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    context_idea_active_requisite_value = True
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    swim_budatom.set_arg(
        context_idea_active_requisite_str(), context_idea_active_requisite_value
    )
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"ReasonUnit context='{context_value}' for idea '{way_value}' set with context_idea_active_requisite={context_idea_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_context_idea_active_requisite_IsNone():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reasonunit_str()
    context_value = f"{sue_bud.bridge}Swimmers"
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"ReasonUnit context='{context_value}' for idea '{way_value}' and no longer checks context active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_reasonunit_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    context_value = f"{sue_bud.bridge}Swimmers"
    swim_budatom = budatom_shop(dimen, atom_delete())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(context_str(), context_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = (
        f"ReasonUnit context='{context_value}' for idea '{way_value}' has been deleted."
    )
    print(f"{x_str=}")
    assert legible_list[0] == x_str
