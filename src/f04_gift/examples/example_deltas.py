from src.f02_bud.bud_tool import budunit_str, bud_acctunit_str
from src.f04_gift.atom_config import atom_delete, atom_update, acct_name_str
from src.f04_gift.atom import atomunit_shop
from src.f04_gift.delta import BudDelta, buddelta_shop


def get_buddelta_sue_example() -> BudDelta:
    sue_buddelta = buddelta_shop()

    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_jvalue(pool_attribute, 77)
    sue_buddelta.set_atomunit(pool_atomunit)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    sue_atomunit = atomunit_shop(dimen, atom_delete())
    sue_atomunit.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_atomunit(sue_atomunit)
    return sue_buddelta


def get_buddelta_example1() -> BudDelta:
    sue_buddelta = buddelta_shop()

    tally_name = "tally"
    x_atomunit = atomunit_shop(budunit_str(), atom_update())
    x_atomunit.set_jvalue(tally_name, 55)
    x_attribute = "max_tree_traverse"
    x_atomunit.set_jvalue(x_attribute, 66)
    x_attribute = "credor_respect"
    x_atomunit.set_jvalue(x_attribute, 77)
    x_attribute = "debtor_respect"
    x_atomunit.set_jvalue(x_attribute, 88)
    x_attribute = "deal_time_int"
    x_atomunit.set_jvalue(x_attribute, 990000)
    sue_buddelta.set_atomunit(x_atomunit)

    dimen = bud_acctunit_str()
    zia_str = "Zia"
    x_atomunit = atomunit_shop(dimen, atom_delete())
    x_atomunit.set_jkey(acct_name_str(), zia_str)
    sue_buddelta.set_atomunit(x_atomunit)
    return sue_buddelta
