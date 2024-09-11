from src._road.jaar_config import get_tribe_id_if_None
from src._road.road import create_road, TribeID
from src.bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_ideaunit_str,
    bud_idea_factunit_str,
)
from src.change.atom_config import (
    atom_insert,
    atom_update,
    atom_delete,
    acct_id_str,
    parent_road_str,
    label_str,
    fopen_str,
    fnigh_str,
)
from src.change.atom import atomunit_shop, AtomUnit
from src.change.change import changeunit_shop, ChangeUnit


def get_atom_example_ideaunit_sports(tribe_id: TribeID = None) -> AtomUnit:
    tribe_id = get_tribe_id_if_None(tribe_id)
    sports_str = "sports"
    x_category = bud_ideaunit_str()
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_str(), sports_str)
    insert_ideaunit_atomunit.set_required_arg(parent_road_str(), tribe_id)
    return insert_ideaunit_atomunit


def get_atom_example_ideaunit_ball(tribe_id: TribeID = None) -> AtomUnit:
    tribe_id = get_tribe_id_if_None(tribe_id)
    sports_str = "sports"
    sports_road = create_road(tribe_id, sports_str)
    ball_str = "basketball"
    x_category = bud_ideaunit_str()
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_str(), ball_str)
    insert_ideaunit_atomunit.set_required_arg(parent_road_str(), sports_road)
    return insert_ideaunit_atomunit


def get_atom_example_ideaunit_knee(tribe_id: TribeID = None) -> AtomUnit:
    tribe_id = get_tribe_id_if_None(tribe_id)
    sports_str = "sports"
    sports_road = create_road(tribe_id, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_category = bud_ideaunit_str()
    begin_str = "begin"
    close_str = "close"
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_str(), knee_str)
    insert_ideaunit_atomunit.set_required_arg(parent_road_str(), sports_road)
    insert_ideaunit_atomunit.set_optional_arg(begin_str, knee_begin)
    insert_ideaunit_atomunit.set_optional_arg(close_str, knee_close)
    return insert_ideaunit_atomunit


def get_atom_example_factunit_knee(tribe_id: TribeID = None) -> AtomUnit:
    tribe_id = get_tribe_id_if_None(tribe_id)
    sports_str = "sports"
    sports_road = create_road(tribe_id, sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road(tribe_id, knee_str)
    knee_fopen = 7
    knee_fnigh = 23
    x_category = bud_idea_factunit_str()
    road_str = "road"
    base_str = "base"
    insert_factunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_factunit_atomunit.set_required_arg(road_str, ball_road)
    insert_factunit_atomunit.set_required_arg(base_str, knee_road)
    insert_factunit_atomunit.set_optional_arg(fopen_str(), knee_fopen)
    insert_factunit_atomunit.set_optional_arg(fnigh_str(), knee_fnigh)
    return insert_factunit_atomunit


def get_changeunit_sue_example() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 77)
    sue_changeunit.set_atomunit(pool_atomunit)

    category = bud_acctunit_str()
    sue_str = "Sue"
    sue_atomunit = atomunit_shop(category, atom_delete())
    sue_atomunit.set_required_arg(acct_id_str(), sue_str)
    sue_changeunit.set_atomunit(sue_atomunit)
    return sue_changeunit
