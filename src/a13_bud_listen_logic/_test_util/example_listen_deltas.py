from src.a01_term_logic.way import FiscLabel
from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    bud_acctunit_str,
    bud_conceptunit_str,
    concept_label_str,
    parent_way_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import DELETE_str, INSERT_str, UPDATE_str
from src.a08_bud_atom_logic.atom import BudAtom, budatom_shop
from src.a09_pack_logic.delta import BudDelta, buddelta_shop


def get_atom_example_conceptunit_sports(fisc_label: FiscLabel = None) -> BudAtom:
    if not fisc_label:
        fisc_label = "accord23"
    sports_str = "sports"
    x_dimen = bud_conceptunit_str()
    insert_conceptunit_budatom = budatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_budatom.set_jkey(concept_label_str(), sports_str)
    insert_conceptunit_budatom.set_jkey(parent_way_str(), fisc_label)
    return insert_conceptunit_budatom


def get_buddelta_sue_example() -> BudDelta:
    sue_buddelta = buddelta_shop()

    budunit_str = budunit_str()
    pool_budatom = budatom_shop(budunit_str(), UPDATE_str())
    pool_attribute = "_credor_respect"
    pool_budatom.set_jvalue(pool_attribute, 77)
    sue_buddelta.set_budatom(pool_budatom)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    sue_budatom = budatom_shop(dimen, DELETE_str())
    sue_budatom.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_budatom(sue_budatom)
    return sue_buddelta


def get_buddelta_example1() -> BudDelta:
    sue_buddelta = buddelta_shop()

    budunit_str = budunit_str()
    mass_name = "mass"
    x_budatom = budatom_shop(budunit_str(), UPDATE_str())
    x_budatom.set_jvalue(mass_name, 55)
    x_attribute = "_max_tree_traverse"
    x_budatom.set_jvalue(x_attribute, 66)
    x_attribute = "_credor_respect"
    x_budatom.set_jvalue(x_attribute, 77)
    x_attribute = "_debtor_respect"
    x_budatom.set_jvalue(x_attribute, 88)
    sue_buddelta.set_budatom(x_budatom)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    x_budatom = budatom_shop(dimen, DELETE_str())
    x_budatom.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_budatom(x_budatom)
    return sue_buddelta


def get_buddelta_example2() -> BudDelta:
    sue_buddelta = buddelta_shop()

    budunit_str = budunit_str()
    x_budatom = budatom_shop(budunit_str(), UPDATE_str())
    x_attribute = "_credor_respect"
    x_budatom.set_jvalue(x_attribute, 77)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    x_budatom = budatom_shop(dimen, DELETE_str())
    x_budatom.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_budatom(x_budatom)
    return sue_buddelta
