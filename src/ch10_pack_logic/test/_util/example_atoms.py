from src.ch01_rope_logic.rope import create_rope
from src.ch01_rope_logic.term import MomentLabel
from src.ch09_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.ch10_pack_logic._ref.ch10_terms import (
    INSERT_str,
    belief_planunit_str,
    plan_rope_str,
)


def get_atom_example_planunit_sports(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    x_dimen = belief_planunit_str()
    sports_rope = create_rope(moment_label, sports_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), sports_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_ball(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    ball_str = "basketball"
    x_dimen = belief_planunit_str()
    ball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_knee(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = belief_planunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), knee_rope)
    insert_planunit_beliefatom.set_jvalue(begin_str, knee_begin)
    insert_planunit_beliefatom.set_jvalue(close_str, knee_close)
    return insert_planunit_beliefatom
