from src.f01_road.jaar_config import get_fiscal_title_if_None
from src.f01_road.road import create_road, FiscalTitle
from src.f02_bud.bud_tool import bud_itemunit_str
from src.f04_gift.atom_config import atom_insert, parent_road_str, item_title_str
from src.f04_gift.atom import atomunit_shop, AtomUnit


def get_atom_example_itemunit_sports(fiscal_title: FiscalTitle = None) -> AtomUnit:
    fiscal_title = get_fiscal_title_if_None(fiscal_title)
    sports_str = "sports"
    x_category = bud_itemunit_str()
    insert_itemunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_itemunit_atomunit.set_jkey(item_title_str(), sports_str)
    insert_itemunit_atomunit.set_jkey(parent_road_str(), fiscal_title)
    return insert_itemunit_atomunit


def get_atom_example_itemunit_ball(fiscal_title: FiscalTitle = None) -> AtomUnit:
    fiscal_title = get_fiscal_title_if_None(fiscal_title)
    sports_str = "sports"
    sports_road = create_road(fiscal_title, sports_str)
    ball_str = "basketball"
    x_category = bud_itemunit_str()
    insert_itemunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_itemunit_atomunit.set_jkey(item_title_str(), ball_str)
    insert_itemunit_atomunit.set_jkey(parent_road_str(), sports_road)
    return insert_itemunit_atomunit


def get_atom_example_itemunit_knee(fiscal_title: FiscalTitle = None) -> AtomUnit:
    fiscal_title = get_fiscal_title_if_None(fiscal_title)
    sports_str = "sports"
    sports_road = create_road(fiscal_title, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_category = bud_itemunit_str()
    begin_str = "begin"
    close_str = "close"
    insert_itemunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_itemunit_atomunit.set_jkey(item_title_str(), knee_str)
    insert_itemunit_atomunit.set_jkey(parent_road_str(), sports_road)
    insert_itemunit_atomunit.set_jvalue(begin_str, knee_begin)
    insert_itemunit_atomunit.set_jvalue(close_str, knee_close)
    return insert_itemunit_atomunit
