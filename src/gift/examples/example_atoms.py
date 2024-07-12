from src._road.jaar_config import get_real_id_if_None
from src._road.road import create_road, RealID
from src.gift.atom import atomunit_shop, atom_insert, AtomUnit


def get_atom_example_ideaunit_sports(real_id: RealID = None) -> AtomUnit:
    real_id = get_real_id_if_None(real_id)
    sports_text = "sports"
    x_category = "world_ideaunit"
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
    x_category = "world_ideaunit"
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
    x_category = "world_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    begin_text = "_begin"
    close_text = "_close"
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_text, knee_text)
    insert_ideaunit_atomunit.set_required_arg(parent_road_text, sports_road)
    insert_ideaunit_atomunit.set_optional_arg(begin_text, knee_begin)
    insert_ideaunit_atomunit.set_optional_arg(close_text, knee_close)
    return insert_ideaunit_atomunit
