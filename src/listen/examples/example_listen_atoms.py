from src._road.jaar_config import get_real_id_if_None
from src._road.road import create_road, RealID
from src.gift.atom import (
    atomunit_shop,
    atom_delete,
    atom_insert,
    atom_update,
    AtomUnit,
)
from src.gift.change import changeunit_shop, ChangeUnit


def get_atom_example_ideaunit_sports(real_id: RealID = None) -> AtomUnit:
    real_id = get_real_id_if_None(real_id)
    sports_text = "sports"
    x_category = "bud_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_text, sports_text)
    insert_ideaunit_atomunit.set_required_arg(parent_road_text, real_id)
    return insert_ideaunit_atomunit


def get_atom_example_ideaunit_ball(real_id: RealID = None) -> AtomUnit:
    real_id = get_real_id_if_None(real_id)
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    ball_text = "basketball"
    x_category = "bud_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_text, ball_text)
    insert_ideaunit_atomunit.set_required_arg(parent_road_text, sports_road)
    return insert_ideaunit_atomunit


def get_atom_example_ideaunit_knee(real_id: RealID = None) -> AtomUnit:
    real_id = get_real_id_if_None(real_id)
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    knee_text = "knee"
    knee_begin = 1
    knee_close = 71
    x_category = "bud_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    begin_text = "begin"
    close_text = "close"
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_text, knee_text)
    insert_ideaunit_atomunit.set_required_arg(parent_road_text, sports_road)
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
    knee_open = 7
    knee_nigh = 23
    x_category = "bud_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    insert_factunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_factunit_atomunit.set_required_arg(road_text, ball_road)
    insert_factunit_atomunit.set_required_arg(base_text, knee_road)
    insert_factunit_atomunit.set_optional_arg(open_text, knee_open)
    insert_factunit_atomunit.set_optional_arg(nigh_text, knee_nigh)
    return insert_factunit_atomunit


def get_changeunit_sue_example() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    budunit_text = "budunit"
    pool_atomunit = atomunit_shop(budunit_text, atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 77)
    sue_changeunit.set_atomunit(pool_atomunit)

    category = "bud_acctunit"
    sue_text = "Sue"
    sue_atomunit = atomunit_shop(category, atom_delete())
    sue_atomunit.set_required_arg("acct_id", sue_text)
    sue_changeunit.set_atomunit(sue_atomunit)
    return sue_changeunit
