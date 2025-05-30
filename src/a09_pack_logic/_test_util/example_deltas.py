from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    bud_acctunit_str,
    budunit_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import DELETE_str, UPDATE_str
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import BudDelta, buddelta_shop


def get_buddelta_sue_example() -> BudDelta:
    sue_buddelta = buddelta_shop()

    pool_budatom = budatom_shop(budunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
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

    tally_name = "tally"
    x_budatom = budatom_shop(budunit_str(), UPDATE_str())
    x_budatom.set_jvalue(tally_name, 55)
    x_attribute = "max_tree_traverse"
    x_budatom.set_jvalue(x_attribute, 66)
    x_attribute = "credor_respect"
    x_budatom.set_jvalue(x_attribute, 77)
    x_attribute = "debtor_respect"
    x_budatom.set_jvalue(x_attribute, 88)
    sue_buddelta.set_budatom(x_budatom)

    dimen = bud_acctunit_str()
    zia_str = "Zia"
    x_budatom = budatom_shop(dimen, DELETE_str())
    x_budatom.set_jkey(acct_name_str(), zia_str)
    sue_buddelta.set_budatom(x_budatom)
    return sue_buddelta
