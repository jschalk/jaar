from src.f1_road.jaar_config import get_fiscal_id_if_None
from src.f1_road.road import FiscalID
from src.f2_bud.bud_tool import bud_acctunit_str, bud_itemunit_str
from src.f4_gift.atom_config import acct_id_str, parent_road_str, label_str
from src.f4_gift.atom import (
    AtomUnit,
    atom_delete,
    atom_update,
    atom_insert,
    atomunit_shop,
)
from src.f4_gift.delta import DeltaUnit, deltaunit_shop


def get_atom_example_itemunit_sports(fiscal_id: FiscalID = None) -> AtomUnit:
    fiscal_id = get_fiscal_id_if_None(fiscal_id)
    sports_str = "sports"
    x_category = bud_itemunit_str()
    insert_itemunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_itemunit_atomunit.set_required_arg(label_str(), sports_str)
    insert_itemunit_atomunit.set_required_arg(parent_road_str(), fiscal_id)
    return insert_itemunit_atomunit


def get_deltaunit_sue_example() -> DeltaUnit:
    sue_deltaunit = deltaunit_shop()

    budunit_str = budunit_str()
    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "_credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 77)
    sue_deltaunit.set_atomunit(pool_atomunit)

    category = bud_acctunit_str()
    sue_str = "Sue"
    sue_atomunit = atomunit_shop(category, atom_delete())
    sue_atomunit.set_required_arg(acct_id_str(), sue_str)
    sue_deltaunit.set_atomunit(sue_atomunit)
    return sue_deltaunit


def get_deltaunit_example1() -> DeltaUnit:
    sue_deltaunit = deltaunit_shop()

    budunit_str = budunit_str()
    mass_name = "mass"
    x_atomunit = atomunit_shop(budunit_str(), atom_update())
    x_atomunit.set_optional_arg(mass_name, 55)
    x_attribute = "_max_tree_traverse"
    x_atomunit.set_optional_arg(x_attribute, 66)
    x_attribute = "_credor_respect"
    x_atomunit.set_optional_arg(x_attribute, 77)
    x_attribute = "_debtor_respect"
    x_atomunit.set_optional_arg(x_attribute, 88)
    sue_deltaunit.set_atomunit(x_atomunit)

    category = bud_acctunit_str()
    sue_str = "Sue"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg(acct_id_str(), sue_str)
    sue_deltaunit.set_atomunit(x_atomunit)
    return sue_deltaunit


def get_deltaunit_example2() -> DeltaUnit:
    sue_deltaunit = deltaunit_shop()

    budunit_str = budunit_str()
    x_atomunit = atomunit_shop(budunit_str(), atom_update())
    x_attribute = "_credor_respect"
    x_atomunit.set_optional_arg(x_attribute, 77)

    category = bud_acctunit_str()
    sue_str = "Sue"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg(acct_id_str(), sue_str)
    sue_deltaunit.set_atomunit(x_atomunit)
    return sue_deltaunit
