from src.a01_term_logic.term import BeliefLabel
from src.a06_owner_logic.test._util.a06_str import (
    acct_name_str,
    concept_label_str,
    owner_acctunit_str,
    owner_conceptunit_str,
    parent_rope_str,
)
from src.a08_owner_atom_logic.atom import OwnerAtom, owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import OwnerDelta, ownerdelta_shop


def get_atom_example_conceptunit_sports(belief_label: BeliefLabel = None) -> OwnerAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    x_dimen = owner_conceptunit_str()
    insert_conceptunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_conceptunit_owneratom.set_jkey(concept_label_str(), sports_str)
    insert_conceptunit_owneratom.set_jkey(parent_rope_str(), belief_label)
    return insert_conceptunit_owneratom


def get_ownerdelta_sue_example() -> OwnerDelta:
    sue_ownerdelta = ownerdelta_shop()

    ownerunit_str = ownerunit_str()
    pool_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    pool_attribute = "_credor_respect"
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

    ownerunit_str = ownerunit_str()
    mass_name = "mass"
    x_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    x_owneratom.set_jvalue(mass_name, 55)
    x_attribute = "_max_tree_traverse"
    x_owneratom.set_jvalue(x_attribute, 66)
    x_attribute = "_credor_respect"
    x_owneratom.set_jvalue(x_attribute, 77)
    x_attribute = "_debtor_respect"
    x_owneratom.set_jvalue(x_attribute, 88)
    sue_ownerdelta.set_owneratom(x_owneratom)

    dimen = owner_acctunit_str()
    sue_str = "Sue"
    x_owneratom = owneratom_shop(dimen, DELETE_str())
    x_owneratom.set_jkey(acct_name_str(), sue_str)
    sue_ownerdelta.set_owneratom(x_owneratom)
    return sue_ownerdelta


def get_ownerdelta_example2() -> OwnerDelta:
    sue_ownerdelta = ownerdelta_shop()

    ownerunit_str = ownerunit_str()
    x_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    x_attribute = "_credor_respect"
    x_owneratom.set_jvalue(x_attribute, 77)

    dimen = owner_acctunit_str()
    sue_str = "Sue"
    x_owneratom = owneratom_shop(dimen, DELETE_str())
    x_owneratom.set_jkey(acct_name_str(), sue_str)
    sue_ownerdelta.set_owneratom(x_owneratom)
    return sue_ownerdelta
