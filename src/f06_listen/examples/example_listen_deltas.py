from src.f01_word_logic.road import FiscTitle
from src.f02_bud.bud_tool import bud_acctunit_str, bud_itemunit_str
from src.f04_pack.atom_config import acct_name_str, parent_road_str, item_title_str
from src.f04_pack.atom import (
    BudAtom,
    atom_delete,
    atom_update,
    atom_insert,
    budatom_shop,
)
from src.f04_pack.delta import BudDelta, buddelta_shop


def get_atom_example_itemunit_sports(fisc_title: FiscTitle = None) -> BudAtom:
    if not fisc_title:
        fisc_title = "accord23"
    sports_str = "sports"
    x_dimen = bud_itemunit_str()
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_title_str(), sports_str)
    insert_itemunit_budatom.set_jkey(parent_road_str(), fisc_title)
    return insert_itemunit_budatom


def get_buddelta_sue_example() -> BudDelta:
    sue_buddelta = buddelta_shop()

    budunit_str = budunit_str()
    pool_budatom = budatom_shop(budunit_str(), atom_update())
    pool_attribute = "_credor_respect"
    pool_budatom.set_jvalue(pool_attribute, 77)
    sue_buddelta.set_budatom(pool_budatom)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    sue_budatom = budatom_shop(dimen, atom_delete())
    sue_budatom.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_budatom(sue_budatom)
    return sue_buddelta


def get_buddelta_example1() -> BudDelta:
    sue_buddelta = buddelta_shop()

    budunit_str = budunit_str()
    mass_name = "mass"
    x_budatom = budatom_shop(budunit_str(), atom_update())
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
    x_budatom = budatom_shop(dimen, atom_delete())
    x_budatom.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_budatom(x_budatom)
    return sue_buddelta


def get_buddelta_example2() -> BudDelta:
    sue_buddelta = buddelta_shop()

    budunit_str = budunit_str()
    x_budatom = budatom_shop(budunit_str(), atom_update())
    x_attribute = "_credor_respect"
    x_budatom.set_jvalue(x_attribute, 77)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    x_budatom = budatom_shop(dimen, atom_delete())
    x_budatom.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_budatom(x_budatom)
    return sue_buddelta
