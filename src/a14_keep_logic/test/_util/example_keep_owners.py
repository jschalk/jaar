from src.a06_owner_logic.owner import (
    BeliefLabel,
    OwnerUnit,
    ownerunit_shop,
    planunit_shop,
)
from src.a14_keep_logic.test._util.a14_env import temp_belief_label


def get_1label_owner() -> OwnerUnit:
    x_owner = ownerunit_shop("A")
    x_owner.set_belief_label(temp_belief_label())
    x_owner.settle_owner()
    return x_owner


def get_Jlabel2label_owner() -> OwnerUnit:
    x_owner = ownerunit_shop("J")
    x_owner.set_belief_label(temp_belief_label())
    x_owner.set_l1_plan(planunit_shop("A"))
    x_owner.settle_owner()
    return x_owner


def get_2label_owner(belief_label: BeliefLabel = None) -> OwnerUnit:
    if belief_label is None:
        belief_label = temp_belief_label()
    a_str = "A"
    b_str = "B"
    x_owner = ownerunit_shop(owner_name=a_str)
    x_owner.set_belief_label(belief_label)
    plan_b = planunit_shop(b_str)
    x_owner.set_plan(plan_b, parent_rope=temp_belief_label())
    x_owner.settle_owner()
    return x_owner


def get_3label_owner() -> OwnerUnit:
    a_str = "A"
    x_owner = ownerunit_shop(a_str)
    x_owner.set_belief_label(temp_belief_label())
    x_owner.set_l1_plan(planunit_shop("B"))
    x_owner.set_l1_plan(planunit_shop("C"))
    x_owner.settle_owner()
    return x_owner


def get_3label_D_E_F_owner() -> OwnerUnit:
    d_str = "D"
    x_owner = ownerunit_shop(d_str)
    x_owner.set_belief_label(temp_belief_label())
    x_owner.set_l1_plan(planunit_shop("E"))
    x_owner.set_l1_plan(planunit_shop("F"))
    x_owner.settle_owner()
    return x_owner


def get_6label_owner() -> OwnerUnit:
    x_owner = ownerunit_shop("A")
    x_owner.set_belief_label(temp_belief_label())
    x_owner.set_l1_plan(planunit_shop("B"))
    x_owner.set_l1_plan(planunit_shop("C"))
    c_rope = x_owner.make_l1_rope("C")
    x_owner.set_plan(planunit_shop("D"), c_rope)
    x_owner.set_plan(planunit_shop("E"), c_rope)
    x_owner.set_plan(planunit_shop("F"), c_rope)
    x_owner.settle_owner()
    return x_owner


def get_7labelInsertH_owner() -> OwnerUnit:
    x_owner = ownerunit_shop("A")
    x_owner.set_belief_label(temp_belief_label())
    x_owner.set_l1_plan(planunit_shop("B"))
    x_owner.set_l1_plan(planunit_shop("C"))
    c_rope = x_owner.make_l1_rope("C")
    x_owner.set_plan(planunit_shop("H"), c_rope)
    x_owner.set_plan(planunit_shop("D"), c_rope)
    x_owner.set_plan(planunit_shop("E"), c_rope)
    x_owner.set_plan(planunit_shop("F"), x_owner.make_rope(c_rope, "H"))
    x_owner.settle_owner()
    return x_owner


def get_5labelHG_owner() -> OwnerUnit:
    x_owner = ownerunit_shop("A")
    x_owner.set_belief_label(temp_belief_label())
    x_owner.set_l1_plan(planunit_shop("B"))
    x_owner.set_l1_plan(planunit_shop("C"))
    c_rope = x_owner.make_l1_rope("C")
    x_owner.set_plan(planunit_shop("H"), c_rope)
    x_owner.set_plan(planunit_shop("G"), c_rope)
    x_owner.settle_owner()
    return x_owner


def get_7labelJRoot_owner() -> OwnerUnit:
    x_owner = ownerunit_shop("J")
    x_owner.set_belief_label(temp_belief_label())
    x_owner.set_l1_plan(planunit_shop("A"))

    a_rope = x_owner.make_l1_rope("A")
    x_owner.set_plan(planunit_shop("B"), a_rope)
    x_owner.set_plan(planunit_shop("C"), a_rope)
    c_rope = x_owner.make_l1_rope("C")
    x_owner.set_plan(planunit_shop("D"), c_rope)
    x_owner.set_plan(planunit_shop("E"), c_rope)
    x_owner.set_plan(planunit_shop("F"), c_rope)
    x_owner.settle_owner()
    return x_owner
