from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_charunit_INSERT():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _meld_strategy_text = "_meld_strategy"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _weight_text = "_weight"
    pledge_text = "pledge"
    label_value = "clean fridge"
    parent_road_value = sue_world.make_l1_road("casa")
    _addin_value = 7
    _begin_value = 13
    _close_value = 17
    _denom_value = 23
    _meld_strategy_value = "example_text1"
    _numeric_road_value = sue_world.make_l1_road("sports")
    _numor_value = 29
    _problem_bool_value = False
    _range_source_road_value = sue_world.make_l1_road("greenways")
    _reest_value = 37
    _weight_value = 43
    pledge_value = False
    clean_atomunit = atomunit_shop(category, atom_insert())
    clean_atomunit.set_arg(label_text, label_value)
    clean_atomunit.set_arg(parent_road_text, parent_road_value)
    clean_atomunit.set_arg(_addin_text, _addin_value)
    clean_atomunit.set_arg(_begin_text, _begin_value)
    clean_atomunit.set_arg(_close_text, _close_value)
    clean_atomunit.set_arg(_denom_text, _denom_value)
    clean_atomunit.set_arg(_meld_strategy_text, _meld_strategy_value)
    clean_atomunit.set_arg(_numeric_road_text, _numeric_road_value)
    clean_atomunit.set_arg(_numor_text, _numor_value)
    clean_atomunit.set_arg(_problem_bool_text, _problem_bool_value)
    clean_atomunit.set_arg(_range_source_road_text, _range_source_road_value)
    clean_atomunit.set_arg(_reest_text, _reest_value)
    clean_atomunit.set_arg(_weight_text, _weight_value)
    clean_atomunit.set_arg(pledge_text, pledge_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(clean_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Created Idea '{label_value}' with parent_road {parent_road_value}. _addin={_addin_value}._begin={_begin_value}._close={_close_value}._denom={_denom_value}._meld_strategy={_meld_strategy_value}._numeric_road={_numeric_road_value}._numor={_numor_value}._problem_bool={_problem_bool_value}._range_source_road={_range_source_road_value}._reest={_reest_value}._weight={_weight_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_charunit_UPDATE():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _meld_strategy_text = "_meld_strategy"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _weight_text = "_weight"
    pledge_text = "pledge"
    label_value = "clean fridge"
    parent_road_value = sue_world.make_l1_road("casa")
    _addin_value = 7
    _begin_value = 13
    _close_value = 17
    _denom_value = 23
    _meld_strategy_value = "example_text1"
    _numeric_road_value = sue_world.make_l1_road("sports")
    _numor_value = 29
    _problem_bool_value = False
    _range_source_road_value = sue_world.make_l1_road("greenways")
    _reest_value = 37
    _weight_value = 43
    pledge_value = False
    clean_atomunit = atomunit_shop(category, atom_update())
    clean_atomunit.set_arg(label_text, label_value)
    clean_atomunit.set_arg(parent_road_text, parent_road_value)
    clean_atomunit.set_arg(_addin_text, _addin_value)
    clean_atomunit.set_arg(_begin_text, _begin_value)
    clean_atomunit.set_arg(_close_text, _close_value)
    clean_atomunit.set_arg(_denom_text, _denom_value)
    clean_atomunit.set_arg(_meld_strategy_text, _meld_strategy_value)
    clean_atomunit.set_arg(_numeric_road_text, _numeric_road_value)
    clean_atomunit.set_arg(_numor_text, _numor_value)
    clean_atomunit.set_arg(_problem_bool_text, _problem_bool_value)
    clean_atomunit.set_arg(_range_source_road_text, _range_source_road_value)
    clean_atomunit.set_arg(_reest_text, _reest_value)
    clean_atomunit.set_arg(_weight_text, _weight_value)
    clean_atomunit.set_arg(pledge_text, pledge_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(clean_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Idea '{label_value}' with parent_road {parent_road_value} transited these attributes: _addin={_addin_value}._begin={_begin_value}._close={_close_value}._denom={_denom_value}._meld_strategy={_meld_strategy_value}._numeric_road={_numeric_road_value}._numor={_numor_value}._problem_bool={_problem_bool_value}._range_source_road={_range_source_road_value}._reest={_reest_value}._weight={_weight_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_charunit_DELETE():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    label_value = "clean fridge"
    parent_road_value = sue_world.make_l1_road("casa")
    clean_atomunit = atomunit_shop(category, atom_delete())
    clean_atomunit.set_arg(label_text, label_value)
    clean_atomunit.set_arg(parent_road_text, parent_road_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(clean_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Idea '{label_value}' with parent_road {parent_road_value} was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
