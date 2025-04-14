from src.f01_road.road import create_road
from src.f02_bud.bud_tool import budunit_str, bud_item_factunit_str
from src.f04_pack.atom_config import atom_update, atom_insert, fopen_str, fnigh_str
from src.f04_pack.atom import (
    budatom_shop,
    atom_hx_table_name,
    get_budatom_from_rowdata,
)
from src.f00_data_toolboxs.db_toolbox import get_rowdata, sqlite_connection
from pytest import raises as pytest_raises


def test_BudAtom_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # WHEN
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)

    # WHEN
    x_dimen = bud_item_factunit_str()
    update_disc_budatom = budatom_shop(x_dimen, atom_update())
    update_disc_budatom.set_jkey("base", knee_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_budatom.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_dimen}' with is_valid=False."
    )


def test_BudAtom_get_insert_sqlstr_ReturnsObj_BudUnitSimpleAttrs():
    # WHEN
    new2_value = 66
    dimen = budunit_str()
    opt_arg2 = "max_tree_traverse"
    x_budatom = budatom_shop(dimen, atom_update())
    x_budatom.set_jvalue(opt_arg2, new2_value)
    # THEN
    x_table = "atom_hx"
    example_sqlstr = f"""
INSERT INTO {x_table} (
  {dimen}_{atom_update()}_{opt_arg2}
)
VALUES (
  {new2_value}
)
;"""
    assert x_budatom.get_insert_sqlstr() == example_sqlstr


def test_BudAtom_get_insert_sqlstr_ReturnsObj_item_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    knee_open = 7
    x_dimen = bud_item_factunit_str()
    road_str = "road"
    base_str = "base"
    update_disc_budatom = budatom_shop(x_dimen, atom_insert())
    update_disc_budatom.set_jkey(road_str, ball_road)
    update_disc_budatom.set_jkey(base_str, knee_road)
    update_disc_budatom.set_jvalue(fopen_str(), knee_open)

    # WHEN
    generated_sqlstr = update_disc_budatom.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""
INSERT INTO {atom_hx_table_name()} (
  {x_dimen}_{atom_insert()}_{road_str}
, {x_dimen}_{atom_insert()}_{base_str}
, {x_dimen}_{atom_insert()}_{fopen_str()}
)
VALUES (
  '{ball_road}'
, '{knee_road}'
, {knee_open}
)
;"""
    print(f"{generated_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_budatom_from_rowdata_ReturnsObj_item_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    knee_fopen = 7
    x_dimen = bud_item_factunit_str()
    road_str = "road"
    base_str = "base"
    x_sqlstr = f"""SELECT
  '{ball_road}' as {x_dimen}_{atom_insert()}_{road_str}
, '{knee_road}' as {x_dimen}_{atom_insert()}_{base_str}
, {knee_fopen} as {x_dimen}_{atom_insert()}_{fopen_str()}
"""
    with sqlite_connection(":memory:") as x_conn:
        x_rowdata = get_rowdata(atom_hx_table_name(), x_conn, x_sqlstr)

    # WHEN
    x_budatom = get_budatom_from_rowdata(x_rowdata)

    # THEN
    update_disc_budatom = budatom_shop(x_dimen, atom_insert())
    update_disc_budatom.set_jkey(road_str, ball_road)
    update_disc_budatom.set_jkey(base_str, knee_road)
    update_disc_budatom.set_jvalue(fopen_str(), knee_fopen)
    assert update_disc_budatom.dimen == x_budatom.dimen
    assert update_disc_budatom.crud_str == x_budatom.crud_str
    assert update_disc_budatom.jkeys == x_budatom.jkeys
    assert update_disc_budatom.jvalues == x_budatom.jvalues
