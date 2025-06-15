from pytest import raises as pytest_raises
from src.a00_data_toolbox.db_toolbox import get_rowdata, sqlite_connection
from src.a01_term_logic.rope import create_rope
from src.a06_plan_logic._test_util.a06_str import (
    concept_rope_str,
    fcontext_str,
    fopen_str,
    plan_concept_factunit_str,
    planunit_str,
)
from src.a08_plan_atom_logic._test_util.a08_str import (
    INSERT_str,
    UPDATE_str,
    atom_hx_str,
)
from src.a08_plan_atom_logic.atom import get_planatom_from_rowdata, planatom_shop


def test_PlanAtom_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # WHEN
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)

    # WHEN
    x_dimen = plan_concept_factunit_str()
    update_disc_planatom = planatom_shop(x_dimen, UPDATE_str())
    update_disc_planatom.set_jkey("rcontext", knee_rope)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_planatom.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_dimen}' with is_valid=False."
    )


def test_PlanAtom_get_insert_sqlstr_ReturnsObj_PlanUnitSimpleAttrs():
    # WHEN
    new2_value = 66
    dimen = planunit_str()
    opt_arg2 = "max_tree_traverse"
    x_planatom = planatom_shop(dimen, UPDATE_str())
    x_planatom.set_jvalue(opt_arg2, new2_value)
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
    assert x_planatom.get_insert_sqlstr() == example_sqlstr


def test_PlanAtom_get_insert_sqlstr_ReturnsObj_concept_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_popen = 7
    x_dimen = plan_concept_factunit_str()
    update_disc_planatom = planatom_shop(x_dimen, INSERT_str())
    update_disc_planatom.set_jkey(concept_rope_str(), ball_rope)
    update_disc_planatom.set_jkey(fcontext_str(), knee_rope)
    update_disc_planatom.set_jvalue(fopen_str(), knee_popen)

    # WHEN
    generated_sqlstr = update_disc_planatom.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""
INSERT INTO {atom_hx_str()} (
  {x_dimen}_{INSERT_str()}_{concept_rope_str()}
, {x_dimen}_{INSERT_str()}_{fcontext_str()}
, {x_dimen}_{INSERT_str()}_{fopen_str()}
)
VALUES (
  '{ball_rope}'
, '{knee_rope}'
, {knee_popen}
)
;"""
    print(f"{generated_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_planatom_from_rowdata_ReturnsObj_concept_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_fopen = 7
    x_dimen = plan_concept_factunit_str()
    x_sqlstr = f"""SELECT
  '{ball_rope}' as {x_dimen}_{INSERT_str()}_{concept_rope_str()}
, '{knee_rope}' as {x_dimen}_{INSERT_str()}_{fcontext_str()}
, {knee_fopen} as {x_dimen}_{INSERT_str()}_{fopen_str()}
"""
    with sqlite_connection(":memory:") as x_conn:
        x_rowdata = get_rowdata(atom_hx_str(), x_conn, x_sqlstr)

    # WHEN
    x_planatom = get_planatom_from_rowdata(x_rowdata)

    # THEN
    update_disc_planatom = planatom_shop(x_dimen, INSERT_str())
    update_disc_planatom.set_jkey(concept_rope_str(), ball_rope)
    update_disc_planatom.set_jkey(fcontext_str(), knee_rope)
    update_disc_planatom.set_jvalue(fopen_str(), knee_fopen)
    assert update_disc_planatom.dimen == x_planatom.dimen
    assert update_disc_planatom.crud_str == x_planatom.crud_str
    assert update_disc_planatom.jkeys == x_planatom.jkeys
    assert update_disc_planatom.jvalues == x_planatom.jvalues
