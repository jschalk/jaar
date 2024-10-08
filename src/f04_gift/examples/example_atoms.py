from src.f01_road.jaar_config import get_fiscal_id_if_None
from src.f01_road.road import create_road, FiscalID
from src.f02_bud.bud_tool import bud_itemunit_str
from src.f04_gift.atom_config import atom_insert, parent_road_str, label_str
from src.f04_gift.atom import atomunit_shop, AtomUnit


def get_atom_example_itemunit_sports(fiscal_id: FiscalID = None) -> AtomUnit:
    fiscal_id = get_fiscal_id_if_None(fiscal_id)
    sports_str = "sports"
    x_category = bud_itemunit_str()
    insert_itemunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_itemunit_atomunit.set_required_arg(label_str(), sports_str)
    insert_itemunit_atomunit.set_required_arg(parent_road_str(), fiscal_id)
    return insert_itemunit_atomunit


def get_atom_example_itemunit_ball(fiscal_id: FiscalID = None) -> AtomUnit:
    fiscal_id = get_fiscal_id_if_None(fiscal_id)
    sports_str = "sports"
    sports_road = create_road(fiscal_id, sports_str)
    ball_str = "basketball"
    x_category = bud_itemunit_str()
    insert_itemunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_itemunit_atomunit.set_required_arg(label_str(), ball_str)
    insert_itemunit_atomunit.set_required_arg(parent_road_str(), sports_road)
    return insert_itemunit_atomunit


def get_atom_example_itemunit_knee(fiscal_id: FiscalID = None) -> AtomUnit:
    fiscal_id = get_fiscal_id_if_None(fiscal_id)
    sports_str = "sports"
    sports_road = create_road(fiscal_id, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_category = bud_itemunit_str()
    begin_str = "begin"
    close_str = "close"
    insert_itemunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_itemunit_atomunit.set_required_arg(label_str(), knee_str)
    insert_itemunit_atomunit.set_required_arg(parent_road_str(), sports_road)
    insert_itemunit_atomunit.set_optional_arg(begin_str, knee_begin)
    insert_itemunit_atomunit.set_optional_arg(close_str, knee_close)
    return insert_itemunit_atomunit
