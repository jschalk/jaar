from src.a01_way_logic.way import create_way, FiscTag
from src.a06_bud_logic._utils.str_a06 import bud_itemunit_str
from src.a06_bud_logic._utils.str_a06 import item_way_str
from src.a08_bud_atom_logic._utils.str_a08 import atom_insert
from src.a08_bud_atom_logic.atom import budatom_shop, BudAtom


def get_atom_example_itemunit_sports(fisc_tag: FiscTag = None) -> BudAtom:
    if not fisc_tag:
        fisc_tag = "accord23"
    sports_str = "sports"
    x_dimen = bud_itemunit_str()
    sports_way = create_way(fisc_tag, sports_str)
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_way_str(), sports_way)
    return insert_itemunit_budatom


def get_atom_example_itemunit_ball(fisc_tag: FiscTag = None) -> BudAtom:
    if not fisc_tag:
        fisc_tag = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_tag, sports_str)
    ball_str = "basketball"
    x_dimen = bud_itemunit_str()
    ball_way = create_way(sports_way, ball_str)
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_way_str(), ball_way)
    return insert_itemunit_budatom


def get_atom_example_itemunit_knee(fisc_tag: FiscTag = None) -> BudAtom:
    if not fisc_tag:
        fisc_tag = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_tag, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = bud_itemunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_way = create_way(sports_way, knee_str)
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_way_str(), knee_way)
    insert_itemunit_budatom.set_jvalue(begin_str, knee_begin)
    insert_itemunit_budatom.set_jvalue(close_str, knee_close)
    return insert_itemunit_budatom
