from src.ch02_rope_logic.rope import RopeTerm, create_rope, create_rope_from_labels
from src.ch09_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.ch10_pack_logic.pack import PackUnit, packunit_shop
from src.ch10_pack_logic.test._util.ch10_examples import (
    get_atom_example_planunit_ball,
    get_atom_example_planunit_knee,
    get_atom_example_planunit_sports,
)
from src.ch11_bud_logic.bud import BudUnit, budunit_shop
from src.ch12_pack_file._ref.ch12_semantic_types import LabelTerm
from src.ref.ch12_keywords import Ch12Keywords as wx


def get_ch12_example_moment_label() -> str:
    return "FizzBuzz2"


def get_atom_example_factunit_knee(first_label: LabelTerm = None) -> BeliefAtom:
    if not first_label:
        first_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(first_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(first_label, knee_str)
    knee_fact_lower = 7
    knee_fact_upper = 23
    x_dimen = wx.belief_plan_factunit
    insert_factunit_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
    insert_factunit_beliefatom.set_jkey(wx.plan_rope, ball_rope)
    insert_factunit_beliefatom.set_jkey(wx.fact_context, knee_rope)
    insert_factunit_beliefatom.set_jvalue(wx.fact_lower, knee_fact_lower)
    insert_factunit_beliefatom.set_jvalue(wx.fact_upper, knee_fact_upper)
    return insert_factunit_beliefatom


def get_texas_rope() -> RopeTerm:
    moment_label = get_ch12_example_moment_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_rope_from_labels([moment_label, nation_str, usa_str, texas_str])


def get_sue_packunit() -> PackUnit:
    return packunit_shop(belief_name="Sue", _pack_id=37, face_name="Yao")


def sue_1beliefatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(belief_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    return x_packunit


def sue_2beliefatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(belief_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    return x_packunit


def sue_3beliefatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(belief_name="Sue", _pack_id=37, face_name="Yao")
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_factunit_knee())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_ball())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    return x_packunit


def sue_4beliefatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(belief_name="Sue", _pack_id=47, face_name="Yao")
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_factunit_knee())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_ball())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    return x_packunit


def get_budunit_55_example() -> BudUnit:
    x_bud_time = 55
    return budunit_shop(x_bud_time)


def get_budunit_66_example() -> BudUnit:
    t66_bud_time = 66
    t66_budunit = budunit_shop(t66_bud_time)
    t66_budunit.set_bud_voice_net("Sue", -5)
    t66_budunit.set_bud_voice_net("Bob", 5)
    return t66_budunit


def get_budunit_88_example() -> BudUnit:
    t88_bud_time = 88
    t88_budunit = budunit_shop(t88_bud_time)
    t88_budunit.quota = 800
    return t88_budunit


def get_budunit_invalid_example() -> BudUnit:
    t55_bud_time = 55
    t55_budunit = budunit_shop(t55_bud_time)
    t55_budunit.set_bud_voice_net("Sue", -5)
    t55_budunit.set_bud_voice_net("Bob", 3)
    return t55_budunit
