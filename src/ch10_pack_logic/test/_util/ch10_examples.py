from src.ch02_rope_logic.rope import create_rope
from src.ch07_belief_logic._ref.ch07_semantic_types import MomentLabel
from src.ch09_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.ch10_pack_logic._ref.ch10_keywords import (
    Ch01Keywords as wx,
    Ch04Keywords as wx,
    Ch09Keywords as wx,
    belief_planunit_str,
    belief_voiceunit_str,
    beliefunit_str,
    plan_rope_str,
)
from src.ch10_pack_logic.delta import BeliefDelta, beliefdelta_shop


def get_atom_example_planunit_sports(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    x_dimen = belief_planunit_str()
    sports_rope = create_rope(moment_label, sports_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
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
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
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
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), knee_rope)
    insert_planunit_beliefatom.set_jvalue(begin_str, knee_begin)
    insert_planunit_beliefatom.set_jvalue(close_str, knee_close)
    return insert_planunit_beliefatom


def get_beliefdelta_sue_example() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    pool_beliefatom = beliefatom_shop(beliefunit_str(), wx.UPDATE)
    pool_attribute = "credor_respect"
    pool_beliefatom.set_jvalue(pool_attribute, 77)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)

    dimen = belief_voiceunit_str()
    sue_str = "Sue"
    sue_beliefatom = beliefatom_shop(dimen, wx.DELETE)
    sue_beliefatom.set_jkey(wx.voice_name, sue_str)
    sue_beliefdelta.set_beliefatom(sue_beliefatom)
    return sue_beliefdelta


def get_beliefdelta_example1() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    tally_name = "tally"
    x_beliefatom = beliefatom_shop(beliefunit_str(), wx.UPDATE)
    x_beliefatom.set_jvalue(tally_name, 55)
    x_attribute = "max_tree_traverse"
    x_beliefatom.set_jvalue(x_attribute, 66)
    x_attribute = "credor_respect"
    x_beliefatom.set_jvalue(x_attribute, 77)
    x_attribute = "debtor_respect"
    x_beliefatom.set_jvalue(x_attribute, 88)
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    dimen = belief_voiceunit_str()
    zia_str = "Zia"
    x_beliefatom = beliefatom_shop(dimen, wx.DELETE)
    x_beliefatom.set_jkey(wx.voice_name, zia_str)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    return sue_beliefdelta
