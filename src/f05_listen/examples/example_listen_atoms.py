from src.f01_road.jaar_config import get_fisc_title_if_None
from src.f01_road.road import create_road, FiscTitle
from src.f02_bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_itemunit_str,
    bud_item_factunit_str,
)
from src.f04_gift.atom_config import (
    atom_insert,
    atom_update,
    atom_delete,
    acct_name_str,
    parent_road_str,
    item_title_str,
    fopen_str,
    fnigh_str,
)
from src.f04_gift.atom import atomunit_shop, AtomUnit
from src.f04_gift.delta import buddelta_shop, BudDelta


def get_atom_example_itemunit_sports(fisc_title: FiscTitle = None) -> AtomUnit:
    fisc_title = get_fisc_title_if_None(fisc_title)
    sports_str = "sports"
    x_dimen = bud_itemunit_str()
    insert_itemunit_atomunit = atomunit_shop(x_dimen, atom_insert())
    insert_itemunit_atomunit.set_jkey(item_title_str(), sports_str)
    insert_itemunit_atomunit.set_jkey(parent_road_str(), fisc_title)
    return insert_itemunit_atomunit


def get_atom_example_itemunit_ball(fisc_title: FiscTitle = None) -> AtomUnit:
    fisc_title = get_fisc_title_if_None(fisc_title)
    sports_str = "sports"
    sports_road = create_road(fisc_title, sports_str)
    ball_str = "basketball"
    x_dimen = bud_itemunit_str()
    insert_itemunit_atomunit = atomunit_shop(x_dimen, atom_insert())
    insert_itemunit_atomunit.set_jkey(item_title_str(), ball_str)
    insert_itemunit_atomunit.set_jkey(parent_road_str(), sports_road)
    return insert_itemunit_atomunit


def get_atom_example_itemunit_knee(fisc_title: FiscTitle = None) -> AtomUnit:
    fisc_title = get_fisc_title_if_None(fisc_title)
    sports_str = "sports"
    sports_road = create_road(fisc_title, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = bud_itemunit_str()
    begin_str = "begin"
    close_str = "close"
    insert_itemunit_atomunit = atomunit_shop(x_dimen, atom_insert())
    insert_itemunit_atomunit.set_jkey(item_title_str(), knee_str)
    insert_itemunit_atomunit.set_jkey(parent_road_str(), sports_road)
    insert_itemunit_atomunit.set_jvalue(begin_str, knee_begin)
    insert_itemunit_atomunit.set_jvalue(close_str, knee_close)
    return insert_itemunit_atomunit


def get_atom_example_factunit_knee(fisc_title: FiscTitle = None) -> AtomUnit:
    fisc_title = get_fisc_title_if_None(fisc_title)
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
    insert_factunit_atomunit = atomunit_shop(x_dimen, atom_insert())
    insert_factunit_atomunit.set_jkey(road_str, ball_road)
    insert_factunit_atomunit.set_jkey(base_str, knee_road)
    insert_factunit_atomunit.set_jvalue(fopen_str(), knee_fopen)
    insert_factunit_atomunit.set_jvalue(fnigh_str(), knee_fnigh)
    return insert_factunit_atomunit


def get_buddelta_sue_example() -> BudDelta:
    sue_buddelta = buddelta_shop()

    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_jvalue(pool_attribute, 77)
    sue_buddelta.set_atomunit(pool_atomunit)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    sue_atomunit = atomunit_shop(dimen, atom_delete())
    sue_atomunit.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_atomunit(sue_atomunit)
    return sue_buddelta
