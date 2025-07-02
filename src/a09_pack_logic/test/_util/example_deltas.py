from src.a06_believer_logic.test._util.a06_str import (
    acct_name_str,
    believer_acctunit_str,
    believerunit_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import DELETE_str, UPDATE_str
from src.a09_pack_logic.delta import BelieverDelta, believerdelta_shop


def get_believerdelta_sue_example() -> BelieverDelta:
    sue_believerdelta = believerdelta_shop()

    pool_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_believeratom.set_jvalue(pool_attribute, 77)
    sue_believerdelta.set_believeratom(pool_believeratom)

    dimen = believer_acctunit_str()
    sue_str = "Sue"
    sue_believeratom = believeratom_shop(dimen, DELETE_str())
    sue_believeratom.set_jkey(acct_name_str(), sue_str)
    sue_believerdelta.set_believeratom(sue_believeratom)
    return sue_believerdelta


def get_believerdelta_example1() -> BelieverDelta:
    sue_believerdelta = believerdelta_shop()

    tally_name = "tally"
    x_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    x_believeratom.set_jvalue(tally_name, 55)
    x_attribute = "max_tree_traverse"
    x_believeratom.set_jvalue(x_attribute, 66)
    x_attribute = "credor_respect"
    x_believeratom.set_jvalue(x_attribute, 77)
    x_attribute = "debtor_respect"
    x_believeratom.set_jvalue(x_attribute, 88)
    sue_believerdelta.set_believeratom(x_believeratom)

    dimen = believer_acctunit_str()
    zia_str = "Zia"
    x_believeratom = believeratom_shop(dimen, DELETE_str())
    x_believeratom.set_jkey(acct_name_str(), zia_str)
    sue_believerdelta.set_believeratom(x_believeratom)
    return sue_believerdelta
