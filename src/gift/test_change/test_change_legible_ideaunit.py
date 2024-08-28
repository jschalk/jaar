from src.gift.atom_config import (
    atom_update,
    atom_insert,
    atom_delete,
    bud_ideaunit_text,
    parent_road_str,
    label_str,
)
from src.gift.atom import atomunit_shop
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_ideaunit_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_ideaunit_text()
    _addin_text = "addin"
    _begin_text = "begin"
    _close_text = "close"
    _denom_text = "denom"
    _numor_text = "numor"
    _problem_bool_text = "problem_bool"
    _morph_text = "morph"
    _mass_text = "mass"
    pledge_text = "pledge"
    label_value = "clean fridge"
    parent_road_value = sue_bud.make_l1_road("casa")
    _addin_value = 7
    _begin_value = 13
    _close_value = 17
    _denom_value = 23
    _numor_value = 29
    _problem_bool_value = False
    _morph_value = 37
    _mass_value = 43
    pledge_value = False
    clean_atomunit = atomunit_shop(category, atom_insert())
    clean_atomunit.set_arg(label_str(), label_value)
    clean_atomunit.set_arg(parent_road_str(), parent_road_value)
    clean_atomunit.set_arg(_addin_text, _addin_value)
    clean_atomunit.set_arg(_begin_text, _begin_value)
    clean_atomunit.set_arg(_close_text, _close_value)
    clean_atomunit.set_arg(_denom_text, _denom_value)
    clean_atomunit.set_arg(_numor_text, _numor_value)
    clean_atomunit.set_arg(_problem_bool_text, _problem_bool_value)
    clean_atomunit.set_arg(_morph_text, _morph_value)
    clean_atomunit.set_arg(_mass_text, _mass_value)
    clean_atomunit.set_arg(pledge_text, pledge_value)

    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(clean_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Created Idea '{label_value}' with parent_road {parent_road_value}. addin={_addin_value}.begin={_begin_value}.close={_close_value}.denom={_denom_value}.numor={_numor_value}.problem_bool={_problem_bool_value}.morph={_morph_value}.mass={_mass_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_ideaunit_UPDATE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_ideaunit_text()
    _addin_text = "addin"
    _begin_text = "begin"
    _close_text = "close"
    _denom_text = "denom"
    _numor_text = "numor"
    _problem_bool_text = "problem_bool"
    _morph_text = "morph"
    _mass_text = "mass"
    pledge_text = "pledge"
    label_value = "clean fridge"
    parent_road_value = sue_bud.make_l1_road("casa")
    _addin_value = 7
    _begin_value = 13
    _close_value = 17
    _denom_value = 23
    _numor_value = 29
    _problem_bool_value = False
    _morph_value = 37
    _mass_value = 43
    pledge_value = False
    clean_atomunit = atomunit_shop(category, atom_update())
    clean_atomunit.set_arg(label_str(), label_value)
    clean_atomunit.set_arg(parent_road_str(), parent_road_value)
    clean_atomunit.set_arg(_addin_text, _addin_value)
    clean_atomunit.set_arg(_begin_text, _begin_value)
    clean_atomunit.set_arg(_close_text, _close_value)
    clean_atomunit.set_arg(_denom_text, _denom_value)
    clean_atomunit.set_arg(_numor_text, _numor_value)
    clean_atomunit.set_arg(_problem_bool_text, _problem_bool_value)
    clean_atomunit.set_arg(_morph_text, _morph_value)
    clean_atomunit.set_arg(_mass_text, _mass_value)
    clean_atomunit.set_arg(pledge_text, pledge_value)

    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(clean_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Idea '{label_value}' with parent_road {parent_road_value} transited these attributes: addin={_addin_value}.begin={_begin_value}.close={_close_value}.denom={_denom_value}.numor={_numor_value}.problem_bool={_problem_bool_value}.morph={_morph_value}.mass={_mass_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_ideaunit_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_ideaunit_text()
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
