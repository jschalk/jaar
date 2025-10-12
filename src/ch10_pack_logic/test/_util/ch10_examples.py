from src.ch02_rope_logic.rope import create_rope
from src.ch09_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.ch10_pack_logic._ref.ch10_semantic_types import MomentLabel
from src.ch10_pack_logic.delta import BeliefDelta, beliefdelta_shop
from src.ref.ch10_keywords import Ch10Keywords as wx


def get_atom_example_planunit_sports(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    insert_planunit_beliefatom = beliefatom_shop(wx.belief_planunit, wx.INSERT)
    insert_planunit_beliefatom.set_jkey(wx.plan_rope, sports_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_ball(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_beliefatom = beliefatom_shop(wx.belief_planunit, wx.INSERT)
    insert_planunit_beliefatom.set_jkey(wx.plan_rope, ball_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_knee(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_planunit_beliefatom = beliefatom_shop(wx.belief_planunit, crud_str=wx.INSERT)
    insert_planunit_beliefatom.set_jkey(wx.plan_rope, knee_rope)
    insert_planunit_beliefatom.set_jvalue(begin_str, knee_begin)
    insert_planunit_beliefatom.set_jvalue(close_str, knee_close)
    return insert_planunit_beliefatom


def get_beliefdelta_sue_example() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    pool_beliefatom = beliefatom_shop(wx.beliefunit, wx.UPDATE)
    pool_attribute = wx.credor_respect
    pool_beliefatom.set_jvalue(pool_attribute, 77)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)

    dimen = wx.belief_voiceunit
    sue_str = "Sue"
    sue_beliefatom = beliefatom_shop(dimen, wx.DELETE)
    sue_beliefatom.set_jkey(wx.voice_name, sue_str)
    sue_beliefdelta.set_beliefatom(sue_beliefatom)
    return sue_beliefdelta


def get_beliefdelta_example1() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    x_beliefatom = beliefatom_shop(wx.beliefunit, wx.UPDATE)
    x_beliefatom.set_jvalue(wx.tally, 55)
    x_beliefatom.set_jvalue(wx.max_tree_traverse, 66)
    x_beliefatom.set_jvalue(wx.credor_respect, 77)
    x_beliefatom.set_jvalue(wx.debtor_respect, 88)
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    zia_str = "Zia"
    x_beliefatom = beliefatom_shop(dimen=wx.belief_voiceunit, crud_str=wx.DELETE)
    x_beliefatom.set_jkey(wx.voice_name, zia_str)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    return sue_beliefdelta
