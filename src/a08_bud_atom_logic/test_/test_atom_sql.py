from pytest import raises as pytest_raises
from src.a00_data_toolbox.db_toolbox import get_rowdata, sqlite_connection
from src.a01_term_logic.way import create_way
from src.a06_bud_logic._test_util.a06_str import (
    bud_concept_factunit_str,
    budunit_str,
    concept_way_str,
    fcontext_str,
    fopen_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import (
    INSERT_str,
    UPDATE_str,
    atom_hx_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop, get_budatom_from_rowdata


def test_BudAtom_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # WHEN
    sports_str = "sports"
    sports_way = create_way("a", sports_str)
    ball_str = "basketball"
    ball_way = create_way(sports_way, ball_str)
    knee_str = "knee"
    knee_way = create_way("a", knee_str)

    # WHEN
    x_dimen = bud_concept_factunit_str()
    update_disc_budatom = budatom_shop(x_dimen, UPDATE_str())
    update_disc_budatom.set_jkey("rcontext", knee_way)

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
    x_budatom = budatom_shop(dimen, UPDATE_str())
    x_budatom.set_jvalue(opt_arg2, new2_value)
    # THEN
    x_table = "atom_hx"
    example_sqlstr = f"""
INSERT INTO {x_table} (
  {dimen}_{UPDATE_str()}_{opt_arg2}
)
VALUES (
  {new2_value}
)
;"""
    assert x_budatom.get_insert_sqlstr() == example_sqlstr


def test_BudAtom_get_insert_sqlstr_ReturnsObj_concept_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_way = create_way("a", sports_str)
    ball_str = "basketball"
    ball_way = create_way(sports_way, ball_str)
    knee_str = "knee"
    knee_way = create_way("a", knee_str)
    knee_popen = 7
    x_dimen = bud_concept_factunit_str()
    update_disc_budatom = budatom_shop(x_dimen, INSERT_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(fcontext_str(), knee_way)
    update_disc_budatom.set_jvalue(fopen_str(), knee_popen)

    # WHEN
    generated_sqlstr = update_disc_budatom.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""
INSERT INTO {atom_hx_str()} (
  {x_dimen}_{INSERT_str()}_{concept_way_str()}
, {x_dimen}_{INSERT_str()}_{fcontext_str()}
, {x_dimen}_{INSERT_str()}_{fopen_str()}
)
VALUES (
  '{ball_way}'
, '{knee_way}'
, {knee_popen}
)
;"""
    print(f"{generated_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_budatom_from_rowdata_ReturnsObj_concept_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_way = create_way("a", sports_str)
    ball_str = "basketball"
    ball_way = create_way(sports_way, ball_str)
    knee_str = "knee"
    knee_way = create_way("a", knee_str)
    knee_fopen = 7
    x_dimen = bud_concept_factunit_str()
    x_sqlstr = f"""SELECT
  '{ball_way}' as {x_dimen}_{INSERT_str()}_{concept_way_str()}
, '{knee_way}' as {x_dimen}_{INSERT_str()}_{fcontext_str()}
, {knee_fopen} as {x_dimen}_{INSERT_str()}_{fopen_str()}
"""
    with sqlite_connection(":memory:") as x_conn:
        x_rowdata = get_rowdata(atom_hx_str(), x_conn, x_sqlstr)

    # WHEN
    x_budatom = get_budatom_from_rowdata(x_rowdata)

    # THEN
    update_disc_budatom = budatom_shop(x_dimen, INSERT_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(fcontext_str(), knee_way)
    update_disc_budatom.set_jvalue(fopen_str(), knee_fopen)
    assert update_disc_budatom.dimen == x_budatom.dimen
    assert update_disc_budatom.crud_str == x_budatom.crud_str
    assert update_disc_budatom.jkeys == x_budatom.jkeys
    assert update_disc_budatom.jvalues == x_budatom.jvalues
