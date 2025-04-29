from src.a01_word_logic.road import create_road, FiscTag
from src.a06_bud_logic._utils.str_helpers import bud_itemunit_str
from src.a08_bud_atom_logic.atom_config import (
    atom_insert,
    parent_road_str,
    item_tag_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop, BudAtom


def get_atom_example_itemunit_sports(fisc_tag: FiscTag = None) -> BudAtom:
    if not fisc_tag:
        fisc_tag = "accord23"
    sports_str = "sports"
    x_dimen = bud_itemunit_str()
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_tag_str(), sports_str)
    insert_itemunit_budatom.set_jkey(parent_road_str(), fisc_tag)
    return insert_itemunit_budatom


def get_atom_example_itemunit_ball(fisc_tag: FiscTag = None) -> BudAtom:
    if not fisc_tag:
        fisc_tag = "accord23"
    sports_str = "sports"
    sports_road = create_road(fisc_tag, sports_str)
    ball_str = "basketball"
    x_dimen = bud_itemunit_str()
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_tag_str(), ball_str)
    insert_itemunit_budatom.set_jkey(parent_road_str(), sports_road)
    return insert_itemunit_budatom


def get_atom_example_itemunit_knee(fisc_tag: FiscTag = None) -> BudAtom:
    if not fisc_tag:
        fisc_tag = "accord23"
    sports_str = "sports"
    sports_road = create_road(fisc_tag, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = bud_itemunit_str()
    begin_str = "begin"
    close_str = "close"
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_tag_str(), knee_str)
    insert_itemunit_budatom.set_jkey(parent_road_str(), sports_road)
    insert_itemunit_budatom.set_jvalue(begin_str, knee_begin)
    insert_itemunit_budatom.set_jvalue(close_str, knee_close)
    return insert_itemunit_budatom
