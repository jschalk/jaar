from src.f01_road.jaar_config import get_fisc_title_if_None
from src.f01_road.road import create_road, FiscTitle
from src.f02_bud.bud_tool import bud_itemunit_str
from src.f04_vow.atom_config import atom_insert, parent_road_str, item_title_str
from src.f04_vow.atom import budatom_shop, BudAtom


def get_atom_example_itemunit_sports(fisc_title: FiscTitle = None) -> BudAtom:
    fisc_title = get_fisc_title_if_None(fisc_title)
    sports_str = "sports"
    x_dimen = bud_itemunit_str()
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_title_str(), sports_str)
    insert_itemunit_budatom.set_jkey(parent_road_str(), fisc_title)
    return insert_itemunit_budatom


def get_atom_example_itemunit_ball(fisc_title: FiscTitle = None) -> BudAtom:
    fisc_title = get_fisc_title_if_None(fisc_title)
    sports_str = "sports"
    sports_road = create_road(fisc_title, sports_str)
    ball_str = "basketball"
    x_dimen = bud_itemunit_str()
    insert_itemunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_itemunit_budatom.set_jkey(item_title_str(), ball_str)
    insert_itemunit_budatom.set_jkey(parent_road_str(), sports_road)
    return insert_itemunit_budatom


def get_atom_example_itemunit_knee(fisc_title: FiscTitle = None) -> BudAtom:
    fisc_title = get_fisc_title_if_None(fisc_title)
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
