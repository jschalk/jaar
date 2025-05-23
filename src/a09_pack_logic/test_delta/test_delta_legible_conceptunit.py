from src.a06_bud_logic._utils.str_a06 import (
    bud_conceptunit_str,
    concept_way_str,
    pledge_str,
    addin_str,
    begin_str,
    close_str,
    denom_str,
    numor_str,
    morph_str,
    mass_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import atom_update, atom_insert, atom_delete
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list
from src.a06_bud_logic.bud import budunit_shop


def test_create_legible_list_ReturnsObj_conceptunit_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_conceptunit_str()
    _problem_bool_str = "problem_bool"
    clean_label = "clean fridge"
    casa_way = sue_bud.make_l1_way("casa")
    clean_way = sue_bud.make_way(casa_way, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    mass_value = 43
    pledge_value = False
    clean_budatom = budatom_shop(dimen, atom_insert())
    clean_budatom.set_arg(concept_way_str(), clean_way)
    clean_budatom.set_arg(addin_str(), addin_value)
    clean_budatom.set_arg(begin_str(), begin_value)
    clean_budatom.set_arg(close_str(), close_value)
    clean_budatom.set_arg(denom_str(), denom_value)
    clean_budatom.set_arg(numor_str(), numor_value)
    clean_budatom.set_arg(_problem_bool_str, problem_bool_value)
    clean_budatom.set_arg(morph_str(), morph_value)
    clean_budatom.set_arg(mass_str(), mass_value)
    clean_budatom.set_arg(pledge_str(), pledge_value)

    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(clean_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Created Concept '{clean_way}'. addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.mass={mass_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_conceptunit_UPDATE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_conceptunit_str()
    _problem_bool_str = "problem_bool"
    clean_label = "clean fridge"
    casa_way = sue_bud.make_l1_way("casa")
    clean_way = sue_bud.make_way(casa_way, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    mass_value = 43
    pledge_value = False
    clean_budatom = budatom_shop(dimen, atom_update())
    clean_budatom.set_arg(concept_way_str(), clean_way)
    clean_budatom.set_arg(addin_str(), addin_value)
    clean_budatom.set_arg(begin_str(), begin_value)
    clean_budatom.set_arg(close_str(), close_value)
    clean_budatom.set_arg(denom_str(), denom_value)
    clean_budatom.set_arg(numor_str(), numor_value)
    clean_budatom.set_arg(_problem_bool_str, problem_bool_value)
    clean_budatom.set_arg(morph_str(), morph_value)
    clean_budatom.set_arg(mass_str(), mass_value)
    clean_budatom.set_arg(pledge_str(), pledge_value)

    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(clean_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Concept '{clean_way}' set these attributes: addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.mass={mass_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_conceptunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_conceptunit_str()
    clean_label = "clean fridge"
    casa_way = sue_bud.make_l1_way("casa")
    clean_way = sue_bud.make_way(casa_way, clean_label)
    clean_budatom = budatom_shop(dimen, atom_delete())
    clean_budatom.set_arg(concept_way_str(), clean_way)

    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(clean_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Concept '{clean_way}' was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
