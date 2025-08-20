from src.a01_term_logic.rope import create_rope
from src.a01_term_logic.term import CoinLabel
from src.a06_belief_logic.test._util.a06_str import belief_planunit_str, plan_rope_str
from src.a08_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.a08_belief_atom_logic.test._util.a08_str import INSERT_str


def get_atom_example_planunit_sports(coin_label: CoinLabel = None) -> BeliefAtom:
    if not coin_label:
        coin_label = "amy23"
    sports_str = "sports"
    x_dimen = belief_planunit_str()
    sports_rope = create_rope(coin_label, sports_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), sports_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_ball(coin_label: CoinLabel = None) -> BeliefAtom:
    if not coin_label:
        coin_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(coin_label, sports_str)
    ball_str = "basketball"
    x_dimen = belief_planunit_str()
    ball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_knee(coin_label: CoinLabel = None) -> BeliefAtom:
    if not coin_label:
        coin_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(coin_label, sports_str)
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
