from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._test_util.a06_str import (
    bud_concept_healerlink_str,
    healer_name_str,
    concept_way_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import INSERT_str, DELETE_str
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_concept_healerlink_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_healerlink_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    healer_name_value = f"{sue_bud.bridge}Swimmers"
    swim_budatom = budatom_shop(dimen, INSERT_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(healer_name_str(), healer_name_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"HealerLink '{healer_name_value}' created for concept '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_concept_healerlink_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_concept_healerlink_str()
    casa_way = sue_bud.make_l1_way("casa")
    way_value = sue_bud.make_way(casa_way, "clean fridge")
    healer_name_value = f"{sue_bud.bridge}Swimmers"
    swim_budatom = budatom_shop(dimen, DELETE_str())
    swim_budatom.set_arg(concept_way_str(), way_value)
    swim_budatom.set_arg(healer_name_str(), healer_name_value)
    # print(f"{swim_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(swim_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"HealerLink '{healer_name_value}' deleted for concept '{way_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
