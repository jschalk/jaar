from src.a01_rope_logic.rope import RopePointer, create_rope_from_labels
from src.a06_belief_logic.belief_main import (
    BeliefUnit,
    MomentLabel,
    beliefunit_shop,
    planunit_shop,
)
from src.a14_keep_logic.test._util.a14_env import temp_moment_label


def temp_belief_name():
    return "ex_belief04"


def get_1label_belief() -> BeliefUnit:
    x_belief = beliefunit_shop("A")
    x_belief.set_moment_label(temp_moment_label())
    x_belief.cashout()
    return x_belief


def get_Jlabel2label_belief() -> BeliefUnit:
    x_belief = beliefunit_shop("J")
    x_belief.set_moment_label(temp_moment_label())
    x_belief.set_l1_plan(planunit_shop("A"))
    x_belief.cashout()
    return x_belief


def get_2label_belief(moment_label: MomentLabel = None) -> BeliefUnit:
    if moment_label is None:
        moment_label = temp_moment_label()
    a_str = "A"
    b_str = "B"
    x_belief = beliefunit_shop(belief_name=a_str)
    x_belief.set_moment_label(moment_label)
    plan_b = planunit_shop(b_str)
    x_belief.set_plan(plan_b, parent_rope=temp_moment_label())
    x_belief.cashout()
    return x_belief


def get_3label_belief() -> BeliefUnit:
    a_str = "A"
    x_belief = beliefunit_shop(a_str)
    x_belief.set_moment_label(temp_moment_label())
    x_belief.set_l1_plan(planunit_shop("B"))
    x_belief.set_l1_plan(planunit_shop("C"))
    x_belief.cashout()
    return x_belief


def get_3label_D_E_F_belief() -> BeliefUnit:
    d_str = "D"
    x_belief = beliefunit_shop(d_str)
    x_belief.set_moment_label(temp_moment_label())
    x_belief.set_l1_plan(planunit_shop("E"))
    x_belief.set_l1_plan(planunit_shop("F"))
    x_belief.cashout()
    return x_belief


def get_6label_belief() -> BeliefUnit:
    x_belief = beliefunit_shop("A")
    x_belief.set_moment_label(temp_moment_label())
    x_belief.set_l1_plan(planunit_shop("B"))
    x_belief.set_l1_plan(planunit_shop("C"))
    c_rope = x_belief.make_l1_rope("C")
    x_belief.set_plan(planunit_shop("D"), c_rope)
    x_belief.set_plan(planunit_shop("E"), c_rope)
    x_belief.set_plan(planunit_shop("F"), c_rope)
    x_belief.cashout()
    return x_belief


def get_7labelInsertH_belief() -> BeliefUnit:
    x_belief = beliefunit_shop("A")
    x_belief.set_moment_label(temp_moment_label())
    x_belief.set_l1_plan(planunit_shop("B"))
    x_belief.set_l1_plan(planunit_shop("C"))
    c_rope = x_belief.make_l1_rope("C")
    x_belief.set_plan(planunit_shop("H"), c_rope)
    x_belief.set_plan(planunit_shop("D"), c_rope)
    x_belief.set_plan(planunit_shop("E"), c_rope)
    x_belief.set_plan(planunit_shop("F"), x_belief.make_rope(c_rope, "H"))
    x_belief.cashout()
    return x_belief


def get_5labelHG_belief() -> BeliefUnit:
    x_belief = beliefunit_shop("A")
    x_belief.set_moment_label(temp_moment_label())
    x_belief.set_l1_plan(planunit_shop("B"))
    x_belief.set_l1_plan(planunit_shop("C"))
    c_rope = x_belief.make_l1_rope("C")
    x_belief.set_plan(planunit_shop("H"), c_rope)
    x_belief.set_plan(planunit_shop("G"), c_rope)
    x_belief.cashout()
    return x_belief


def get_7labelJRoot_belief() -> BeliefUnit:
    x_belief = beliefunit_shop("J")
    x_belief.set_moment_label(temp_moment_label())
    x_belief.set_l1_plan(planunit_shop("A"))

    a_rope = x_belief.make_l1_rope("A")
    x_belief.set_plan(planunit_shop("B"), a_rope)
    x_belief.set_plan(planunit_shop("C"), a_rope)
    c_rope = x_belief.make_l1_rope("C")
    x_belief.set_plan(planunit_shop("D"), c_rope)
    x_belief.set_plan(planunit_shop("E"), c_rope)
    x_belief.set_plan(planunit_shop("F"), c_rope)
    x_belief.cashout()
    return x_belief


def get_texas_rope() -> RopePointer:
    naton_str = "nation"
    usa_str = "usa"
    texas_str = "texas"
    return create_rope_from_labels([naton_str, usa_str, texas_str])
