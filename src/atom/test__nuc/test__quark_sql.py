from src._road.road import create_road
from src.atom.quark import (
    quark_update,
    quark_insert,
    quarkunit_shop,
    quark_hx_table_name,
    get_quarkunit_from_rowdata,
)
from src._instrument.sqlite import get_rowdata
from pytest import raises as pytest_raises
from sqlite3 import connect as sqlite3_connect


def test_QuarkUnit_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # WHEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)

    # WHEN
    x_category = "agenda_idea_beliefunit"
    update_disc_quarkunit = quarkunit_shop(x_category, quark_update())
    # update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_quarkunit.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_category}' with is_valid=False."
    )


def test_QuarkUnit_get_insert_sqlstr_ReturnsCorrectObj_AgendaUnitSimpleAttrs():
    # WHEN
    new2_value = 66
    category = "agendaunit"
    opt_arg2 = "_max_tree_traverse"
    x_quarkunit = quarkunit_shop(category, quark_update())
    x_quarkunit.set_optional_arg(opt_arg2, new2_value)
    # THEN
    x_table = "quark_hx"
    example_sqlstr = f"""INSERT INTO {x_table} (
  {category}_{quark_update()}_{opt_arg2}
)
VALUES (
  {new2_value}
)
;"""
    assert x_quarkunit.get_insert_sqlstr() == example_sqlstr


def test_QuarkUnit_get_insert_sqlstr_ReturnsCorrectObj_idea_beliefunit():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    knee_open = 7
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    update_disc_quarkunit = quarkunit_shop(x_category, quark_insert())
    update_disc_quarkunit.set_required_arg(road_text, ball_road)
    update_disc_quarkunit.set_required_arg(base_text, knee_road)
    update_disc_quarkunit.set_optional_arg(open_text, knee_open)

    # WHEN
    gen_sqlstr = update_disc_quarkunit.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""INSERT INTO {quark_hx_table_name()} (
  {x_category}_{quark_insert()}_{road_text}
, {x_category}_{quark_insert()}_{base_text}
, {x_category}_{quark_insert()}_{open_text}
)
VALUES (
  '{ball_road}'
, '{knee_road}'
, {knee_open}
)
;"""
    assert gen_sqlstr == example_sqlstr


def test_get_quarkunit_from_rowdata_ReturnsCorrectObj_idea_beliefunit():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    knee_open = 7
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    x_sqlstr = f"""SELECT
  '{ball_road}' as {x_category}_{quark_insert()}_{road_text}
, '{knee_road}' as {x_category}_{quark_insert()}_{base_text}
, {knee_open} as {x_category}_{quark_insert()}_{open_text}
"""
    x_conn = sqlite3_connect(":memory:")
    x_rowdata = get_rowdata(quark_hx_table_name(), x_conn, x_sqlstr)

    # WHEN
    x_quarkunit = get_quarkunit_from_rowdata(x_rowdata)

    # THEN
    update_disc_quarkunit = quarkunit_shop(x_category, quark_insert())
    update_disc_quarkunit.set_required_arg(road_text, ball_road)
    update_disc_quarkunit.set_required_arg(base_text, knee_road)
    update_disc_quarkunit.set_optional_arg(open_text, knee_open)
    assert update_disc_quarkunit.category == x_quarkunit.category
    assert update_disc_quarkunit.crud_text == x_quarkunit.crud_text
    assert update_disc_quarkunit.required_args == x_quarkunit.required_args
    assert update_disc_quarkunit.optional_args == x_quarkunit.optional_args