from src.f01_road.road import create_road
from src.f02_bud.bud_tool import budunit_str, bud_item_factunit_str
from src.f04_gift.atom_config import atom_update, atom_insert, fopen_str, fnigh_str
from src.f04_gift.atom import (
    atomunit_shop,
    atom_hx_table_name,
    get_atomunit_from_rowdata,
)
from src.f00_instrument.db_toolbox import get_rowdata, sqlite_connection
from pytest import raises as pytest_raises


def test_AtomUnit_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # WHEN
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)

    # WHEN
    x_category = bud_item_factunit_str()
    update_disc_atomunit = atomunit_shop(x_category, atom_update())
    update_disc_atomunit.set_required_arg("base", knee_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_atomunit.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_category}' with is_valid=False."
    )


def test_AtomUnit_get_insert_sqlstr_ReturnsCorrectObj_BudUnitSimpleAttrs():
    # WHEN
    new2_value = 66
    category = budunit_str()
    opt_arg2 = "max_tree_traverse"
    x_atomunit = atomunit_shop(category, atom_update())
    x_atomunit.set_optional_arg(opt_arg2, new2_value)
    # THEN
    x_table = "atom_hx"
    example_sqlstr = f"""
INSERT INTO {x_table} (
  {category}_{atom_update()}_{opt_arg2}
)
VALUES (
  {new2_value}
)
;"""
    assert x_atomunit.get_insert_sqlstr() == example_sqlstr


def test_AtomUnit_get_insert_sqlstr_ReturnsCorrectObj_item_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    knee_open = 7
    x_category = bud_item_factunit_str()
    road_str = "road"
    base_str = "base"
    update_disc_atomunit = atomunit_shop(x_category, atom_insert())
    update_disc_atomunit.set_required_arg(road_str, ball_road)
    update_disc_atomunit.set_required_arg(base_str, knee_road)
    update_disc_atomunit.set_optional_arg(fopen_str(), knee_open)

    # WHEN
    generated_sqlstr = update_disc_atomunit.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""
INSERT INTO {atom_hx_table_name()} (
  {x_category}_{atom_insert()}_{road_str}
, {x_category}_{atom_insert()}_{base_str}
, {x_category}_{atom_insert()}_{fopen_str()}
)
VALUES (
  '{ball_road}'
, '{knee_road}'
, {knee_open}
)
;"""
    print(f"{generated_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_atomunit_from_rowdata_ReturnsCorrectObj_item_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    knee_fopen = 7
    x_category = bud_item_factunit_str()
    road_str = "road"
    base_str = "base"
    x_sqlstr = f"""SELECT
  '{ball_road}' as {x_category}_{atom_insert()}_{road_str}
, '{knee_road}' as {x_category}_{atom_insert()}_{base_str}
, {knee_fopen} as {x_category}_{atom_insert()}_{fopen_str()}
"""
    with sqlite_connection(":memory:") as x_conn:
        x_rowdata = get_rowdata(atom_hx_table_name(), x_conn, x_sqlstr)

    # WHEN
    x_atomunit = get_atomunit_from_rowdata(x_rowdata)

    # THEN
    update_disc_atomunit = atomunit_shop(x_category, atom_insert())
    update_disc_atomunit.set_required_arg(road_str, ball_road)
    update_disc_atomunit.set_required_arg(base_str, knee_road)
    update_disc_atomunit.set_optional_arg(fopen_str(), knee_fopen)
    assert update_disc_atomunit.category == x_atomunit.category
    assert update_disc_atomunit.crud_str == x_atomunit.crud_str
    assert update_disc_atomunit.required_args == x_atomunit.required_args
    assert update_disc_atomunit.optional_args == x_atomunit.optional_args
