from src.a06_bud_logic._test_util.a06_str import (
    awardee_title_str,
    bud_concept_awardlink_str,
    concept_way_str,
    give_force_str,
    take_force_str,
)
from src.a06_bud_logic.bud import budunit_shop
from src.a08_bud_atom_logic._test_util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_awardlink_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_awardlink_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    give_force_value = 81
    take_force_value = 43
    swim_budatom = budatom_shop(dimen, INSERT_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_budatom.set_arg(give_force_str(), give_force_value)
    swim_budatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink created for group {awardee_title_value} for concept '{way_value}' with give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_UPDATE_give_force_take_force():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")

    dimen = bud_concept_awardlink_str()
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    give_force_value = 81
    take_force_value = 43
    swim_budatom = budatom_shop(dimen, UPDATE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_budatom.set_arg(give_force_str(), give_force_value)
    swim_budatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{way_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_UPDATE_give_force():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_awardlink_str()
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    give_force_value = 81
    swim_budatom = budatom_shop(dimen, UPDATE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_budatom.set_arg(give_force_str(), give_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{way_value}'. Now give_force={give_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_UPDATE_take_force():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_awardlink_str()
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")

    take_force_value = 81
    swim_budatom = budatom_shop(dimen, UPDATE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    swim_budatom.set_arg(take_force_str(), take_force_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink has been set for group {awardee_title_value} for concept '{way_value}'. Now take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_awardlink_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_awardlink_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    awardee_title_value = f"{sue_bud.bridge}Swimmers"
    swim_budatom = budatom_shop(dimen, DELETE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(awardee_title_str(), awardee_title_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Awardlink for group {awardee_title_value}, concept '{way_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
