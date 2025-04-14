from src.a01_word_logic.road import create_road, FiscTitle
from src.a06_bud_logic.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_itemunit_str,
    bud_item_factunit_str,
)
from src.a08_bud_atom_logic.atom_config import (
    atom_insert,
    atom_update,
    atom_delete,
    acct_name_str,
    parent_road_str,
    item_title_str,
    fopen_str,
    fnigh_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop, BudAtom
from src.a09_pack_logic.delta import buddelta_shop, BudDelta


def get_atom_example_itemunit_sports(fisc_title: FiscTitle = None) -> BudAtom:
    if not fisc_title:
        fisc_title = "accord23"
    sports_str = "sports"
    x_dimen = bud_itemunit_str()
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_title_str(), sports_str)
    insert_itemunit_budatom.set_jkey(parent_road_str(), fisc_title)
    return insert_itemunit_budatom


def get_atom_example_itemunit_ball(fisc_title: FiscTitle = None) -> BudAtom:
    if not fisc_title:
        fisc_title = "accord23"
    sports_str = "sports"
    sports_road = create_road(fisc_title, sports_str)
    ball_str = "basketball"
    x_dimen = bud_itemunit_str()
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_title_str(), ball_str)
    insert_itemunit_budatom.set_jkey(parent_road_str(), sports_road)
    return insert_itemunit_budatom


def get_atom_example_itemunit_knee(fisc_title: FiscTitle = None) -> BudAtom:
    if not fisc_title:
        fisc_title = "accord23"
    sports_str = "sports"
    sports_road = create_road(fisc_title, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = bud_itemunit_str()
    begin_str = "begin"
    close_str = "close"
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_title_str(), knee_str)
    insert_itemunit_budatom.set_jkey(parent_road_str(), sports_road)
    insert_itemunit_budatom.set_jvalue(begin_str, knee_begin)
    insert_itemunit_budatom.set_jvalue(close_str, knee_close)
    return insert_itemunit_budatom


def get_atom_example_factunit_knee(fisc_title: FiscTitle = None) -> BudAtom:
    if not fisc_title:
        fisc_title = "accord23"
    sports_str = "sports"
    sports_road = create_road(fisc_title, sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road(fisc_title, knee_str)
    knee_fopen = 7
    knee_fnigh = 23
    x_dimen = bud_item_factunit_str()
    road_str = "road"
    base_str = "base"
    insert_factunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_factunit_budatom.set_jkey(road_str, ball_road)
    insert_factunit_budatom.set_jkey(base_str, knee_road)
    insert_factunit_budatom.set_jvalue(fopen_str(), knee_fopen)
    insert_factunit_budatom.set_jvalue(fnigh_str(), knee_fnigh)
    return insert_factunit_budatom


def get_buddelta_sue_example() -> BudDelta:
    sue_buddelta = buddelta_shop()

    pool_budatom = budatom_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_budatom.set_jvalue(pool_attribute, 77)
    sue_buddelta.set_budatom(pool_budatom)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    sue_budatom = budatom_shop(dimen, atom_delete())
    sue_budatom.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_budatom(sue_budatom)
    return sue_buddelta
