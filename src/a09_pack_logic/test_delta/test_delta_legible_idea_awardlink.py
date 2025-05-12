from src.a06_bud_logic._utils.str_a06 import (
    bud_idea_awardlink_str,
    awardee_label_str,
    give_force_str,
    idea_way_str,
    take_force_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import atom_update, atom_insert, atom_delete
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list
from src.a06_bud_logic.bud import budunit_shop


def test_create_legible_list_ReturnsObj_idea_awardlink_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_awardlink_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    awardee_label_value = f"{sue_bud.bridge}Swimmers"
    give_force_value = 81
    take_force_value = 43
    swim_budatom = budatom_shop(dimen, atom_insert())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(awardee_label_str(), awardee_label_value)
    swim_budatom.set_arg(give_force_str(), give_force_value)
    swim_budatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink created for group {awardee_label_value} for idea '{way_value}' with give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_awardlink_UPDATE_give_force_take_force():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")

    dimen = bud_idea_awardlink_str()
    awardee_label_value = f"{sue_bud.bridge}Swimmers"
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    give_force_value = 81
    take_force_value = 43
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(awardee_label_str(), awardee_label_value)
    swim_budatom.set_arg(give_force_str(), give_force_value)
    swim_budatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_label_value} for idea '{way_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_awardlink_UPDATE_give_force():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_awardlink_str()
    awardee_label_value = f"{sue_bud.bridge}Swimmers"
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    give_force_value = 81
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(awardee_label_str(), awardee_label_value)
    swim_budatom.set_arg(give_force_str(), give_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_label_value} for idea '{way_value}'. Now give_force={give_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_awardlink_UPDATE_take_force():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_awardlink_str()
    awardee_label_value = f"{sue_bud.bridge}Swimmers"
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")

    take_force_value = 81
    swim_budatom = budatom_shop(dimen, atom_update())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(awardee_label_str(), awardee_label_value)
    swim_budatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_label_value} for idea '{way_value}'. Now take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_awardlink_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_idea_awardlink_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    awardee_label_value = f"{sue_bud.bridge}Swimmers"
    swim_budatom = budatom_shop(dimen, atom_delete())
    swim_budatom.set_arg(idea_way_str(), way_value)
    swim_budatom.set_arg(awardee_label_str(), awardee_label_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink for group {awardee_label_value}, idea '{way_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
