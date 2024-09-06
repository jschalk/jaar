from src._road.jaar_config import get_real_id_if_None
from src._road.road import create_road, RealID
from src.bud.bud_tool import (
    budunit_text,
    bud_acctunit_text,
    bud_ideaunit_text,
    bud_idea_factunit_text,
)
from src.gift.atom_config import (
    atom_insert,
    atom_update,
    atom_delete,
    acct_id_str,
    parent_road_str,
    label_str,
    fopen_str,
    fnigh_str,
)
from src.gift.atom import atomunit_shop, AtomUnit
from src.gift.change import changeunit_shop, ChangeUnit


def get_atom_example_ideaunit_sports(real_id: RealID = None) -> AtomUnit:
    real_id = get_real_id_if_None(real_id)
    sports_text = "sports"
    x_category = bud_ideaunit_text()
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_str(), sports_text)
    insert_ideaunit_atomunit.set_required_arg(parent_road_str(), real_id)
    return insert_ideaunit_atomunit


def get_atom_example_ideaunit_ball(real_id: RealID = None) -> AtomUnit:
    real_id = get_real_id_if_None(real_id)
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    ball_text = "basketball"
    x_category = bud_ideaunit_text()
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_str(), ball_text)
    insert_ideaunit_atomunit.set_required_arg(parent_road_str(), sports_road)
    return insert_ideaunit_atomunit


def get_atom_example_ideaunit_knee(real_id: RealID = None) -> AtomUnit:
    real_id = get_real_id_if_None(real_id)
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    knee_text = "knee"
    knee_begin = 1
    knee_close = 71
    x_category = bud_ideaunit_text()
    begin_text = "begin"
    close_text = "close"
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_str(), knee_text)
    insert_ideaunit_atomunit.set_required_arg(parent_road_str(), sports_road)
    insert_ideaunit_atomunit.set_optional_arg(begin_text, knee_begin)
    insert_ideaunit_atomunit.set_optional_arg(close_text, knee_close)
    return insert_ideaunit_atomunit


def get_atom_example_factunit_knee(real_id: RealID = None) -> AtomUnit:
    real_id = get_real_id_if_None(real_id)
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road(real_id, knee_text)
    knee_fopen = 7
    knee_fnigh = 23
    x_category = bud_idea_factunit_text()
    road_text = "road"
    base_text = "base"
    insert_factunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_factunit_atomunit.set_required_arg(road_text, ball_road)
    insert_factunit_atomunit.set_required_arg(base_text, knee_road)
    insert_factunit_atomunit.set_optional_arg(fopen_str(), knee_fopen)
    insert_factunit_atomunit.set_optional_arg(fnigh_str(), knee_fnigh)
    return insert_factunit_atomunit


def get_changeunit_sue_example() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    pool_atomunit = atomunit_shop(budunit_text(), atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 77)
    sue_changeunit.set_atomunit(pool_atomunit)

    category = bud_acctunit_text()
    sue_text = "Sue"
    sue_atomunit = atomunit_shop(category, atom_delete())
    sue_atomunit.set_required_arg(acct_id_str(), sue_text)
    sue_changeunit.set_atomunit(sue_atomunit)
    return sue_changeunit
