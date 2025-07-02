from src.a06_owner_logic.test._util.a06_str import (
    acct_name_str,
    owner_acctunit_str,
    ownerunit_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import DELETE_str, UPDATE_str
from src.a09_pack_logic.delta import OwnerDelta, ownerdelta_shop


def get_ownerdelta_sue_example() -> OwnerDelta:
    sue_ownerdelta = ownerdelta_shop()

    pool_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_owneratom.set_jvalue(pool_attribute, 77)
    sue_ownerdelta.set_owneratom(pool_owneratom)

    dimen = owner_acctunit_str()
    sue_str = "Sue"
    sue_owneratom = owneratom_shop(dimen, DELETE_str())
    sue_owneratom.set_jkey(acct_name_str(), sue_str)
    sue_ownerdelta.set_owneratom(sue_owneratom)
    return sue_ownerdelta


def get_ownerdelta_example1() -> OwnerDelta:
    sue_ownerdelta = ownerdelta_shop()

    tally_name = "tally"
    x_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    x_owneratom.set_jvalue(tally_name, 55)
    x_attribute = "max_tree_traverse"
    x_owneratom.set_jvalue(x_attribute, 66)
    x_attribute = "credor_respect"
    x_owneratom.set_jvalue(x_attribute, 77)
    x_attribute = "debtor_respect"
    x_owneratom.set_jvalue(x_attribute, 88)
    sue_ownerdelta.set_owneratom(x_owneratom)

    dimen = owner_acctunit_str()
    zia_str = "Zia"
    x_owneratom = owneratom_shop(dimen, DELETE_str())
    x_owneratom.set_jkey(acct_name_str(), zia_str)
    sue_ownerdelta.set_owneratom(x_owneratom)
    return sue_ownerdelta
