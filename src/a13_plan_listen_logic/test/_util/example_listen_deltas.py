from src.a01_term_logic.term import BankLabel
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    concept_label_str,
    parent_rope_str,
    plan_acctunit_str,
    plan_conceptunit_str,
)
from src.a08_plan_atom_logic.atom import PlanAtom, planatom_shop
from src.a08_plan_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import PlanDelta, plandelta_shop


def get_atom_example_conceptunit_sports(bank_label: BankLabel = None) -> PlanAtom:
    if not bank_label:
        bank_label = "accord23"
    sports_str = "sports"
    x_dimen = plan_conceptunit_str()
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_label_str(), sports_str)
    insert_conceptunit_planatom.set_jkey(parent_rope_str(), bank_label)
    return insert_conceptunit_planatom


def get_plandelta_sue_example() -> PlanDelta:
    sue_plandelta = plandelta_shop()

    planunit_str = planunit_str()
    pool_planatom = planatom_shop(planunit_str(), UPDATE_str())
    pool_attribute = "_credor_respect"
    pool_planatom.set_jvalue(pool_attribute, 77)
    sue_plandelta.set_planatom(pool_planatom)

    dimen = plan_acctunit_str()
    sue_str = "Sue"
    sue_planatom = planatom_shop(dimen, DELETE_str())
    sue_planatom.set_jkey(acct_name_str(), sue_str)
    sue_plandelta.set_planatom(sue_planatom)
    return sue_plandelta


def get_plandelta_example1() -> PlanDelta:
    sue_plandelta = plandelta_shop()

    planunit_str = planunit_str()
    mass_name = "mass"
    x_planatom = planatom_shop(planunit_str(), UPDATE_str())
    x_planatom.set_jvalue(mass_name, 55)
    x_attribute = "_max_tree_traverse"
    x_planatom.set_jvalue(x_attribute, 66)
    x_attribute = "_credor_respect"
    x_planatom.set_jvalue(x_attribute, 77)
    x_attribute = "_debtor_respect"
    x_planatom.set_jvalue(x_attribute, 88)
    sue_plandelta.set_planatom(x_planatom)

    dimen = plan_acctunit_str()
    sue_str = "Sue"
    x_planatom = planatom_shop(dimen, DELETE_str())
    x_planatom.set_jkey(acct_name_str(), sue_str)
    sue_plandelta.set_planatom(x_planatom)
    return sue_plandelta


def get_plandelta_example2() -> PlanDelta:
    sue_plandelta = plandelta_shop()

    planunit_str = planunit_str()
    x_planatom = planatom_shop(planunit_str(), UPDATE_str())
    x_attribute = "_credor_respect"
    x_planatom.set_jvalue(x_attribute, 77)

    dimen = plan_acctunit_str()
    sue_str = "Sue"
    x_planatom = planatom_shop(dimen, DELETE_str())
    x_planatom.set_jkey(acct_name_str(), sue_str)
    sue_plandelta.set_planatom(x_planatom)
    return sue_plandelta
