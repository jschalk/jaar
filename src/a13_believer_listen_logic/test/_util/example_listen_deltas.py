from src.a01_term_logic.term import BeliefLabel
from src.a06_believer_logic.test._util.a06_str import (
    believer_partnerunit_str,
    believer_planunit_str,
    parent_rope_str,
    partner_name_str,
    plan_label_str,
)
from src.a08_believer_atom_logic.atom_main import BelieverAtom, believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import BelieverDelta, believerdelta_shop


def get_atom_example_planunit_sports(belief_label: BeliefLabel = None) -> BelieverAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    x_dimen = believer_planunit_str()
    insert_planunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_planunit_believeratom.set_jkey(plan_label_str(), sports_str)
    insert_planunit_believeratom.set_jkey(parent_rope_str(), belief_label)
    return insert_planunit_believeratom


def get_believerdelta_sue_example() -> BelieverDelta:
    sue_believerdelta = believerdelta_shop()

    believerunit_str = believerunit_str()
    pool_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    pool_attribute = "_credor_respect"
    pool_believeratom.set_jvalue(pool_attribute, 77)
    sue_believerdelta.set_believeratom(pool_believeratom)

    dimen = believer_partnerunit_str()
    sue_str = "Sue"
    sue_believeratom = believeratom_shop(dimen, DELETE_str())
    sue_believeratom.set_jkey(partner_name_str(), sue_str)
    sue_believerdelta.set_believeratom(sue_believeratom)
    return sue_believerdelta


def get_believerdelta_example1() -> BelieverDelta:
    sue_believerdelta = believerdelta_shop()

    believerunit_str = believerunit_str()
    mass_name = "mass"
    x_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    x_believeratom.set_jvalue(mass_name, 55)
    x_attribute = "_max_tree_traverse"
    x_believeratom.set_jvalue(x_attribute, 66)
    x_attribute = "_credor_respect"
    x_believeratom.set_jvalue(x_attribute, 77)
    x_attribute = "_debtor_respect"
    x_believeratom.set_jvalue(x_attribute, 88)
    sue_believerdelta.set_believeratom(x_believeratom)

    dimen = believer_partnerunit_str()
    sue_str = "Sue"
    x_believeratom = believeratom_shop(dimen, DELETE_str())
    x_believeratom.set_jkey(partner_name_str(), sue_str)
    sue_believerdelta.set_believeratom(x_believeratom)
    return sue_believerdelta


def get_believerdelta_example2() -> BelieverDelta:
    sue_believerdelta = believerdelta_shop()

    believerunit_str = believerunit_str()
    x_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    x_attribute = "_credor_respect"
    x_believeratom.set_jvalue(x_attribute, 77)

    dimen = believer_partnerunit_str()
    sue_str = "Sue"
    x_believeratom = believeratom_shop(dimen, DELETE_str())
    x_believeratom.set_jkey(partner_name_str(), sue_str)
    sue_believerdelta.set_believeratom(x_believeratom)
    return sue_believerdelta
