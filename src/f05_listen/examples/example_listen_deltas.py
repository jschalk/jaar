from src.f01_road.jaar_config import get_fiscal_title_if_None
from src.f01_road.road import FiscalTitle
from src.f02_bud.bud_tool import bud_acctunit_str, bud_itemunit_str
from src.f04_gift.atom_config import acct_name_str, parent_road_str, item_title_str
from src.f04_gift.atom import (
    AtomUnit,
    atom_delete,
    atom_update,
    atom_insert,
    atomunit_shop,
)
from src.f04_gift.delta import DeltaUnit, deltaunit_shop


def get_atom_example_itemunit_sports(fiscal_title: FiscalTitle = None) -> AtomUnit:
    fiscal_title = get_fiscal_title_if_None(fiscal_title)
    sports_str = "sports"
    x_dimen = bud_itemunit_str()
    insert_itemunit_atomunit = atomunit_shop(x_dimen, atom_insert())
    insert_itemunit_atomunit.set_jkey(item_title_str(), sports_str)
    insert_itemunit_atomunit.set_jkey(parent_road_str(), fiscal_title)
    return insert_itemunit_atomunit


def get_deltaunit_sue_example() -> DeltaUnit:
    sue_deltaunit = deltaunit_shop()

    budunit_str = budunit_str()
    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "_credor_respect"
    pool_atomunit.set_jvalue(pool_attribute, 77)
    sue_deltaunit.set_atomunit(pool_atomunit)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    sue_atomunit = atomunit_shop(dimen, atom_delete())
    sue_atomunit.set_jkey(acct_name_str(), sue_str)
    sue_deltaunit.set_atomunit(sue_atomunit)
    return sue_deltaunit


def get_deltaunit_example1() -> DeltaUnit:
    sue_deltaunit = deltaunit_shop()

    budunit_str = budunit_str()
    mass_name = "mass"
    x_atomunit = atomunit_shop(budunit_str(), atom_update())
    x_atomunit.set_jvalue(mass_name, 55)
    x_attribute = "_max_tree_traverse"
    x_atomunit.set_jvalue(x_attribute, 66)
    x_attribute = "_credor_respect"
    x_atomunit.set_jvalue(x_attribute, 77)
    x_attribute = "_debtor_respect"
    x_atomunit.set_jvalue(x_attribute, 88)
    sue_deltaunit.set_atomunit(x_atomunit)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    x_atomunit = atomunit_shop(dimen, atom_delete())
    x_atomunit.set_jkey(acct_name_str(), sue_str)
    sue_deltaunit.set_atomunit(x_atomunit)
    return sue_deltaunit


def get_deltaunit_example2() -> DeltaUnit:
    sue_deltaunit = deltaunit_shop()

    budunit_str = budunit_str()
    x_atomunit = atomunit_shop(budunit_str(), atom_update())
    x_attribute = "_credor_respect"
    x_atomunit.set_jvalue(x_attribute, 77)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    x_atomunit = atomunit_shop(dimen, atom_delete())
    x_atomunit.set_jkey(acct_name_str(), sue_str)
    sue_deltaunit.set_atomunit(x_atomunit)
    return sue_deltaunit
