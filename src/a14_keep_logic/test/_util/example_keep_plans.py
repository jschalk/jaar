from src.a06_plan_logic.plan import (
    BeliefLabel,
    PlanUnit,
    conceptunit_shop,
    planunit_shop,
)
from src.a14_keep_logic.test._util.a14_env import temp_belief_label


def get_1label_plan() -> PlanUnit:
    x_plan = planunit_shop("A")
    x_plan.set_belief_label(temp_belief_label())
    x_plan.settle_plan()
    return x_plan


def get_Jlabel2label_plan() -> PlanUnit:
    x_plan = planunit_shop("J")
    x_plan.set_belief_label(temp_belief_label())
    x_plan.set_l1_concept(conceptunit_shop("A"))
    x_plan.settle_plan()
    return x_plan


def get_2label_plan(belief_label: BeliefLabel = None) -> PlanUnit:
    if belief_label is None:
        belief_label = temp_belief_label()
    a_str = "A"
    b_str = "B"
    x_plan = planunit_shop(owner_name=a_str)
    x_plan.set_belief_label(belief_label)
    concept_b = conceptunit_shop(b_str)
    x_plan.set_concept(concept_b, parent_rope=temp_belief_label())
    x_plan.settle_plan()
    return x_plan


def get_3label_plan() -> PlanUnit:
    a_str = "A"
    x_plan = planunit_shop(a_str)
    x_plan.set_belief_label(temp_belief_label())
    x_plan.set_l1_concept(conceptunit_shop("B"))
    x_plan.set_l1_concept(conceptunit_shop("C"))
    x_plan.settle_plan()
    return x_plan


def get_3label_D_E_F_plan() -> PlanUnit:
    d_str = "D"
    x_plan = planunit_shop(d_str)
    x_plan.set_belief_label(temp_belief_label())
    x_plan.set_l1_concept(conceptunit_shop("E"))
    x_plan.set_l1_concept(conceptunit_shop("F"))
    x_plan.settle_plan()
    return x_plan


def get_6label_plan() -> PlanUnit:
    x_plan = planunit_shop("A")
    x_plan.set_belief_label(temp_belief_label())
    x_plan.set_l1_concept(conceptunit_shop("B"))
    x_plan.set_l1_concept(conceptunit_shop("C"))
    c_rope = x_plan.make_l1_rope("C")
    x_plan.set_concept(conceptunit_shop("D"), c_rope)
    x_plan.set_concept(conceptunit_shop("E"), c_rope)
    x_plan.set_concept(conceptunit_shop("F"), c_rope)
    x_plan.settle_plan()
    return x_plan


def get_7labelInsertH_plan() -> PlanUnit:
    x_plan = planunit_shop("A")
    x_plan.set_belief_label(temp_belief_label())
    x_plan.set_l1_concept(conceptunit_shop("B"))
    x_plan.set_l1_concept(conceptunit_shop("C"))
    c_rope = x_plan.make_l1_rope("C")
    x_plan.set_concept(conceptunit_shop("H"), c_rope)
    x_plan.set_concept(conceptunit_shop("D"), c_rope)
    x_plan.set_concept(conceptunit_shop("E"), c_rope)
    x_plan.set_concept(conceptunit_shop("F"), x_plan.make_rope(c_rope, "H"))
    x_plan.settle_plan()
    return x_plan


def get_5labelHG_plan() -> PlanUnit:
    x_plan = planunit_shop("A")
    x_plan.set_belief_label(temp_belief_label())
    x_plan.set_l1_concept(conceptunit_shop("B"))
    x_plan.set_l1_concept(conceptunit_shop("C"))
    c_rope = x_plan.make_l1_rope("C")
    x_plan.set_concept(conceptunit_shop("H"), c_rope)
    x_plan.set_concept(conceptunit_shop("G"), c_rope)
    x_plan.settle_plan()
    return x_plan


def get_7labelJRoot_plan() -> PlanUnit:
    x_plan = planunit_shop("J")
    x_plan.set_belief_label(temp_belief_label())
    x_plan.set_l1_concept(conceptunit_shop("A"))

    a_rope = x_plan.make_l1_rope("A")
    x_plan.set_concept(conceptunit_shop("B"), a_rope)
    x_plan.set_concept(conceptunit_shop("C"), a_rope)
    c_rope = x_plan.make_l1_rope("C")
    x_plan.set_concept(conceptunit_shop("D"), c_rope)
    x_plan.set_concept(conceptunit_shop("E"), c_rope)
    x_plan.set_concept(conceptunit_shop("F"), c_rope)
    x_plan.settle_plan()
    return x_plan
