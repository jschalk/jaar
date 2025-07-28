from pytest import raises as pytest_raises
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_rowdata
from src.a01_term_logic.rope import create_rope
from src.a06_believer_logic.test._util.a06_str import (
    believer_plan_factunit_str,
    believerunit_str,
    f_context_str,
    f_lower_str,
    plan_rope_str,
)
from src.a08_believer_atom_logic.atom_main import (
    believeratom_shop,
    get_believeratom_from_rowdata,
)
from src.a08_believer_atom_logic.test._util.a08_str import (
    INSERT_str,
    UPDATE_str,
    atom_hx_str,
)


def test_BelieverAtom_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # WHEN
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)

    # WHEN
    x_dimen = believer_plan_factunit_str()
    update_disc_believeratom = believeratom_shop(x_dimen, UPDATE_str())
    update_disc_believeratom.set_jkey("reason_context", knee_rope)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_believeratom.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_dimen}' with is_valid=False."
    )


def test_BelieverAtom_get_insert_sqlstr_ReturnsObj_BelieverUnitSimpleAttrs():
    # WHEN
    new2_value = 66
    dimen = believerunit_str()
    opt_arg2 = "max_tree_traverse"
    x_believeratom = believeratom_shop(dimen, UPDATE_str())
    x_believeratom.set_jvalue(opt_arg2, new2_value)
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
    assert x_believeratom.get_insert_sqlstr() == example_sqlstr


def test_BelieverAtom_get_insert_sqlstr_ReturnsObj_plan_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_reason_lower = 7
    x_dimen = believer_plan_factunit_str()
    update_disc_believeratom = believeratom_shop(x_dimen, INSERT_str())
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey(f_context_str(), knee_rope)
    update_disc_believeratom.set_jvalue(f_lower_str(), knee_reason_lower)

    # WHEN
    generated_sqlstr = update_disc_believeratom.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""
INSERT INTO {atom_hx_str()} (
  {x_dimen}_{INSERT_str()}_{plan_rope_str()}
, {x_dimen}_{INSERT_str()}_{f_context_str()}
, {x_dimen}_{INSERT_str()}_{f_lower_str()}
)
VALUES (
  '{ball_rope}'
, '{knee_rope}'
, {knee_reason_lower}
)
;"""
    print(f"{generated_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_believeratom_from_rowdata_ReturnsObj_plan_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_f_lower = 7
    x_dimen = believer_plan_factunit_str()
    x_sqlstr = f"""SELECT
  '{ball_rope}' as {x_dimen}_{INSERT_str()}_{plan_rope_str()}
, '{knee_rope}' as {x_dimen}_{INSERT_str()}_{f_context_str()}
, {knee_f_lower} as {x_dimen}_{INSERT_str()}_{f_lower_str()}
"""
    with sqlite3_connect(":memory:") as x_conn:
        x_rowdata = get_rowdata(atom_hx_str(), x_conn, x_sqlstr)

    # WHEN
    x_believeratom = get_believeratom_from_rowdata(x_rowdata)

    # THEN
    update_disc_believeratom = believeratom_shop(x_dimen, INSERT_str())
    update_disc_believeratom.set_jkey(plan_rope_str(), ball_rope)
    update_disc_believeratom.set_jkey(f_context_str(), knee_rope)
    update_disc_believeratom.set_jvalue(f_lower_str(), knee_f_lower)
    assert update_disc_believeratom.dimen == x_believeratom.dimen
    assert update_disc_believeratom.crud_str == x_believeratom.crud_str
    assert update_disc_believeratom.jkeys == x_believeratom.jkeys
    assert update_disc_believeratom.jvalues == x_believeratom.jvalues
