from src.a01_rope_logic.rope import create_rope
from src.a01_rope_logic.term import MomentLabel
from src.a08_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.a09_pack_logic.delta import BeliefDelta, beliefdelta_shop
from src.a13_belief_listen_logic._ref.a13_terms import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    belief_plan_factunit_str,
    belief_planunit_str,
    belief_voiceunit_str,
    beliefunit_str,
    fact_context_str,
    fact_lower_str,
    fact_upper_str,
    plan_rope_str,
    voice_name_str,
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
    bball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), bball_rope)
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


def get_atom_example_factunit_knee(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(moment_label, knee_str)
    knee_fact_lower = 7
    knee_fact_upper = 23
    x_dimen = belief_plan_factunit_str()
    insert_factunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_factunit_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    insert_factunit_beliefatom.set_jkey(fact_context_str(), knee_rope)
    insert_factunit_beliefatom.set_jvalue(fact_lower_str(), knee_fact_lower)
    insert_factunit_beliefatom.set_jvalue(fact_upper_str(), knee_fact_upper)
    return insert_factunit_beliefatom


def get_beliefdelta_sue_example() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    pool_beliefatom = beliefatom_shop(beliefunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_beliefatom.set_jvalue(pool_attribute, 77)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)

    dimen = belief_voiceunit_str()
    sue_str = "Sue"
    sue_beliefatom = beliefatom_shop(dimen, DELETE_str())
    sue_beliefatom.set_jkey(voice_name_str(), sue_str)
    sue_beliefdelta.set_beliefatom(sue_beliefatom)
    return sue_beliefdelta
