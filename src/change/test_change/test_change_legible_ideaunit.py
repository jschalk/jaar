from src.bud.bud_tool import bud_ideaunit_str
from src.change.atom_config import (
    atom_update,
    atom_insert,
    atom_delete,
    parent_road_str,
    label_str,
    pledge_str,
    addin_str,
    begin_str,
    close_str,
    denom_str,
    numor_str,
    morph_str,
    mass_str,
)
from src.change.atom import atomunit_shop
from src.change.change import changeunit_shop
from src.change.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_ideaunit_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_ideaunit_str()
    _problem_bool_str = "problem_bool"
    label_value = "clean fridge"
    parent_road_value = sue_bud.make_l1_road("casa")
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    mass_value = 43
    pledge_value = False
    clean_atomunit = atomunit_shop(category, atom_insert())
    clean_atomunit.set_arg(label_str(), label_value)
    clean_atomunit.set_arg(parent_road_str(), parent_road_value)
    clean_atomunit.set_arg(addin_str(), addin_value)
    clean_atomunit.set_arg(begin_str(), begin_value)
    clean_atomunit.set_arg(close_str(), close_value)
    clean_atomunit.set_arg(denom_str(), denom_value)
    clean_atomunit.set_arg(numor_str(), numor_value)
    clean_atomunit.set_arg(_problem_bool_str, problem_bool_value)
    clean_atomunit.set_arg(morph_str(), morph_value)
    clean_atomunit.set_arg(mass_str(), mass_value)
    clean_atomunit.set_arg(pledge_str(), pledge_value)

    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(clean_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Created Idea '{label_value}' with parent_road {parent_road_value}. addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.mass={mass_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_ideaunit_UPDATE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_ideaunit_str()
    _problem_bool_str = "problem_bool"
    label_value = "clean fridge"
    parent_road_value = sue_bud.make_l1_road("casa")
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    mass_value = 43
    pledge_value = False
    clean_atomunit = atomunit_shop(category, atom_update())
    clean_atomunit.set_arg(label_str(), label_value)
    clean_atomunit.set_arg(parent_road_str(), parent_road_value)
    clean_atomunit.set_arg(addin_str(), addin_value)
    clean_atomunit.set_arg(begin_str(), begin_value)
    clean_atomunit.set_arg(close_str(), close_value)
    clean_atomunit.set_arg(denom_str(), denom_value)
    clean_atomunit.set_arg(numor_str(), numor_value)
    clean_atomunit.set_arg(_problem_bool_str, problem_bool_value)
    clean_atomunit.set_arg(morph_str(), morph_value)
    clean_atomunit.set_arg(mass_str(), mass_value)
    clean_atomunit.set_arg(pledge_str(), pledge_value)

    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(clean_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Idea '{label_value}' with parent_road {parent_road_value} transited these attributes: addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.mass={mass_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_ideaunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_ideaunit_str()
    label_value = "clean fridge"
    parent_road_value = sue_bud.make_l1_road("casa")
    clean_atomunit = atomunit_shop(category, atom_delete())
    clean_atomunit.set_arg(label_str(), label_value)
    clean_atomunit.set_arg(parent_road_str(), parent_road_value)

    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(clean_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Idea '{label_value}' with parent_road {parent_road_value} was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
