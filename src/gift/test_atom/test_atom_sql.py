from src._road.road import create_road
from src.gift.atom import (
    atom_update,
    atom_insert,
    atomunit_shop,
    atom_hx_table_name,
    get_atomunit_from_rowdata,
)
from src._instrument.db_tool import get_rowdata, sqlite_connection
from pytest import raises as pytest_raises


def test_AtomUnit_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # WHEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)

    # WHEN
    x_category = "world_idea_factunit"
    update_disc_atomunit = atomunit_shop(x_category, atom_update())
    update_disc_atomunit.set_required_arg("base", knee_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_atomunit.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_category}' with is_valid=False."
    )


def test_AtomUnit_get_insert_sqlstr_ReturnsCorrectObj_WorldUnitSimpleAttrs():
    # WHEN
    new2_value = 66
    category = "worldunit"
    opt_arg2 = "_max_tree_traverse"
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


def test_AtomUnit_get_insert_sqlstr_ReturnsCorrectObj_idea_factunit():
    # ESTABLISH
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    knee_open = 7
    x_category = "world_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    update_disc_atomunit = atomunit_shop(x_category, atom_insert())
    update_disc_atomunit.set_required_arg(road_text, ball_road)
    update_disc_atomunit.set_required_arg(base_text, knee_road)
    update_disc_atomunit.set_optional_arg(open_text, knee_open)

    # WHEN
    gen_sqlstr = update_disc_atomunit.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""
INSERT INTO {atom_hx_table_name()} (
  {x_category}_{atom_insert()}_{road_text}
, {x_category}_{atom_insert()}_{base_text}
, {x_category}_{atom_insert()}_{open_text}
)
VALUES (
  '{ball_road}'
, '{knee_road}'
, {knee_open}
)
;"""
    assert gen_sqlstr == example_sqlstr


def test_get_atomunit_from_rowdata_ReturnsCorrectObj_idea_factunit():
    # ESTABLISH
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    knee_open = 7
    x_category = "world_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    x_sqlstr = f"""SELECT
  '{ball_road}' as {x_category}_{atom_insert()}_{road_text}
, '{knee_road}' as {x_category}_{atom_insert()}_{base_text}
, {knee_open} as {x_category}_{atom_insert()}_{open_text}
"""
    with sqlite_connection(":memory:") as x_conn:
        x_rowdata = get_rowdata(atom_hx_table_name(), x_conn, x_sqlstr)

    # WHEN
    x_atomunit = get_atomunit_from_rowdata(x_rowdata)

    # THEN
    update_disc_atomunit = atomunit_shop(x_category, atom_insert())
    update_disc_atomunit.set_required_arg(road_text, ball_road)
    update_disc_atomunit.set_required_arg(base_text, knee_road)
    update_disc_atomunit.set_optional_arg(open_text, knee_open)
    assert update_disc_atomunit.category == x_atomunit.category
    assert update_disc_atomunit.crud_text == x_atomunit.crud_text
    assert update_disc_atomunit.required_args == x_atomunit.required_args
    assert update_disc_atomunit.optional_args == x_atomunit.optional_args
