from src.a01_term_logic.rope import create_rope
from src.a01_term_logic.term import BeliefLabel
from src.a06_believer_logic.test._util.a06_str import (
    believer_planunit_str,
    plan_rope_str,
)
from src.a08_believer_atom_logic.atom_main import BelieverAtom, believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import INSERT_str


def get_atom_example_planunit_sports(belief_label: BeliefLabel = None) -> BelieverAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    x_dimen = believer_planunit_str()
    sports_rope = create_rope(belief_label, sports_str)
    insert_planunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_planunit_believeratom.set_jkey(plan_rope_str(), sports_rope)
    return insert_planunit_believeratom


def get_atom_example_planunit_ball(belief_label: BeliefLabel = None) -> BelieverAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(belief_label, sports_str)
    ball_str = "basketball"
    x_dimen = believer_planunit_str()
    ball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_planunit_believeratom.set_jkey(plan_rope_str(), ball_rope)
    return insert_planunit_believeratom


def get_atom_example_planunit_knee(belief_label: BeliefLabel = None) -> BelieverAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(belief_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = believer_planunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_planunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_planunit_believeratom.set_jkey(plan_rope_str(), knee_rope)
    insert_planunit_believeratom.set_jvalue(begin_str, knee_begin)
    insert_planunit_believeratom.set_jvalue(close_str, knee_close)
    return insert_planunit_believeratom
