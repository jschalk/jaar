from pytest import raises as pytest_raises
from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import get_rowdata
from src.ch02_rope_logic.rope import create_rope
from src.ch09_belief_atom_logic._ref.ch09_keywords import (
    Ch01Keywords as wx,
    Ch06Keywords as wx,
    Ch07Keywords as wx,
    Ch09Keywords as wx,
    fact_context_str,
    fact_lower_str,
)
from src.ch09_belief_atom_logic.atom_main import (
    beliefatom_shop,
    get_beliefatom_from_rowdata,
)


def test_BeliefAtom_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = wx.belief_plan_factunit
    update_disc_beliefatom = beliefatom_shop(x_dimen, wx.UPDATE)
    update_disc_beliefatom.set_jkey("reason_context", knee_rope)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_beliefatom.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_dimen}' with is_valid=False."
    )


def test_BeliefAtom_get_insert_sqlstr_ReturnsObj_BeliefUnitSimpleAttrs():
    # ESTABLISH
    new2_value = 66
    dimen = wx.beliefunit
    opt_arg2 = "max_tree_traverse"
    x_beliefatom = beliefatom_shop(dimen, wx.UPDATE)
    x_beliefatom.set_jvalue(opt_arg2, new2_value)
    x_table = "atom_hx"
    example_sqlstr = f"""
INSERT INTO {x_table} (
  {dimen}_{wx.UPDATE}_{opt_arg2}
)
VALUES (
  {new2_value}
)
;"""

    # WHEN / THEN
    assert x_beliefatom.get_insert_sqlstr() == example_sqlstr


def test_BeliefAtom_get_insert_sqlstr_ReturnsObj_plan_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_reason_lower = 7
    x_dimen = wx.belief_plan_factunit
    update_disc_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
    update_disc_beliefatom.set_jkey(wx.plan_rope, ball_rope)
    update_disc_beliefatom.set_jkey(fact_context_str(), knee_rope)
    update_disc_beliefatom.set_jvalue(fact_lower_str(), knee_reason_lower)

    # WHEN
    generated_sqlstr = update_disc_beliefatom.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""
INSERT INTO {wx.atom_hx} (
  {x_dimen}_{wx.INSERT}_{wx.plan_rope}
, {x_dimen}_{wx.INSERT}_{fact_context_str()}
, {x_dimen}_{wx.INSERT}_{fact_lower_str()}
)
VALUES (
  '{ball_rope}'
, '{knee_rope}'
, {knee_reason_lower}
)
;"""
    print(f"{generated_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_beliefatom_from_rowdata_ReturnsObj_plan_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_fact_lower = 7
    x_dimen = wx.belief_plan_factunit
    x_sqlstr = f"""SELECT
  '{ball_rope}' as {x_dimen}_{wx.INSERT}_{wx.plan_rope}
, '{knee_rope}' as {x_dimen}_{wx.INSERT}_{fact_context_str()}
, {knee_fact_lower} as {x_dimen}_{wx.INSERT}_{fact_lower_str()}
"""
    with sqlite3_connect(":memory:") as x_conn:
        x_rowdata = get_rowdata(wx.atom_hx, x_conn, x_sqlstr)

    # WHEN
    x_beliefatom = get_beliefatom_from_rowdata(x_rowdata)

    # THEN
    update_disc_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
    update_disc_beliefatom.set_jkey(wx.plan_rope, ball_rope)
    update_disc_beliefatom.set_jkey(fact_context_str(), knee_rope)
    update_disc_beliefatom.set_jvalue(fact_lower_str(), knee_fact_lower)
    assert update_disc_beliefatom.dimen == x_beliefatom.dimen
    assert update_disc_beliefatom.crud_str == x_beliefatom.crud_str
    assert update_disc_beliefatom.jkeys == x_beliefatom.jkeys
    assert update_disc_beliefatom.jvalues == x_beliefatom.jvalues
