from src.a06_believer_logic.believer import (
    BeliefLabel,
    BelieverUnit,
    believerunit_shop,
    planunit_shop,
)
from src.a14_keep_logic.test._util.a14_env import temp_belief_label


def get_1label_believer() -> BelieverUnit:
    x_believer = believerunit_shop("A")
    x_believer.set_belief_label(temp_belief_label())
    x_believer.settle_believer()
    return x_believer


def get_Jlabel2label_believer() -> BelieverUnit:
    x_believer = believerunit_shop("J")
    x_believer.set_belief_label(temp_belief_label())
    x_believer.set_l1_plan(planunit_shop("A"))
    x_believer.settle_believer()
    return x_believer


def get_2label_believer(belief_label: BeliefLabel = None) -> BelieverUnit:
    if belief_label is None:
        belief_label = temp_belief_label()
    a_str = "A"
    b_str = "B"
    x_believer = believerunit_shop(believer_name=a_str)
    x_believer.set_belief_label(belief_label)
    plan_b = planunit_shop(b_str)
    x_believer.set_plan(plan_b, parent_rope=temp_belief_label())
    x_believer.settle_believer()
    return x_believer


def get_3label_believer() -> BelieverUnit:
    a_str = "A"
    x_believer = believerunit_shop(a_str)
    x_believer.set_belief_label(temp_belief_label())
    x_believer.set_l1_plan(planunit_shop("B"))
    x_believer.set_l1_plan(planunit_shop("C"))
    x_believer.settle_believer()
    return x_believer


def get_3label_D_E_F_believer() -> BelieverUnit:
    d_str = "D"
    x_believer = believerunit_shop(d_str)
    x_believer.set_belief_label(temp_belief_label())
    x_believer.set_l1_plan(planunit_shop("E"))
    x_believer.set_l1_plan(planunit_shop("F"))
    x_believer.settle_believer()
    return x_believer


def get_6label_believer() -> BelieverUnit:
    x_believer = believerunit_shop("A")
    x_believer.set_belief_label(temp_belief_label())
    x_believer.set_l1_plan(planunit_shop("B"))
    x_believer.set_l1_plan(planunit_shop("C"))
    c_rope = x_believer.make_l1_rope("C")
    x_believer.set_plan(planunit_shop("D"), c_rope)
    x_believer.set_plan(planunit_shop("E"), c_rope)
    x_believer.set_plan(planunit_shop("F"), c_rope)
    x_believer.settle_believer()
    return x_believer


def get_7labelInsertH_believer() -> BelieverUnit:
    x_believer = believerunit_shop("A")
    x_believer.set_belief_label(temp_belief_label())
    x_believer.set_l1_plan(planunit_shop("B"))
    x_believer.set_l1_plan(planunit_shop("C"))
    c_rope = x_believer.make_l1_rope("C")
    x_believer.set_plan(planunit_shop("H"), c_rope)
    x_believer.set_plan(planunit_shop("D"), c_rope)
    x_believer.set_plan(planunit_shop("E"), c_rope)
    x_believer.set_plan(planunit_shop("F"), x_believer.make_rope(c_rope, "H"))
    x_believer.settle_believer()
    return x_believer


def get_5labelHG_believer() -> BelieverUnit:
    x_believer = believerunit_shop("A")
    x_believer.set_belief_label(temp_belief_label())
    x_believer.set_l1_plan(planunit_shop("B"))
    x_believer.set_l1_plan(planunit_shop("C"))
    c_rope = x_believer.make_l1_rope("C")
    x_believer.set_plan(planunit_shop("H"), c_rope)
    x_believer.set_plan(planunit_shop("G"), c_rope)
    x_believer.settle_believer()
    return x_believer


def get_7labelJRoot_believer() -> BelieverUnit:
    x_believer = believerunit_shop("J")
    x_believer.set_belief_label(temp_belief_label())
    x_believer.set_l1_plan(planunit_shop("A"))

    a_rope = x_believer.make_l1_rope("A")
    x_believer.set_plan(planunit_shop("B"), a_rope)
    x_believer.set_plan(planunit_shop("C"), a_rope)
    c_rope = x_believer.make_l1_rope("C")
    x_believer.set_plan(planunit_shop("D"), c_rope)
    x_believer.set_plan(planunit_shop("E"), c_rope)
    x_believer.set_plan(planunit_shop("F"), c_rope)
    x_believer.settle_believer()
    return x_believer
