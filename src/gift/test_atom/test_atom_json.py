from src._road.road import create_road
from src.gift.atom import (
    atomunit_shop,
    atom_insert,
    get_from_json as atomunit_get_from_json,
)
from src._instrument.python import x_is_json


def test_AtomUnit_get_dict_ReturnsCorrectObj():
    # ESTABLISH
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    x_category = "bud_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    knee_open = 7
    knee_nigh = 13
    insert_factunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_factunit_atomunit.set_required_arg(road_text, ball_road)
    insert_factunit_atomunit.set_required_arg(base_text, knee_road)
    insert_factunit_atomunit.set_optional_arg(open_text, knee_open)
    insert_factunit_atomunit.set_optional_arg(nigh_text, knee_nigh)

    # WHEN
    atom_dict = insert_factunit_atomunit.get_dict()

    # THEN
    assert atom_dict == {
        "category": x_category,
        "crud_text": atom_insert(),
        "required_args": {road_text: ball_road, base_text: knee_road},
        "optional_args": {open_text: knee_open, nigh_text: knee_nigh},
    }


def test_AtomUnit_get_json_ReturnsCorrectObj():
    # ESTABLISH
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    x_category = "bud_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    knee_open = 7
    knee_nigh = 13
    insert_factunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_factunit_atomunit.set_required_arg(road_text, ball_road)
    insert_factunit_atomunit.set_required_arg(base_text, knee_road)
    insert_factunit_atomunit.set_optional_arg(open_text, knee_open)
    insert_factunit_atomunit.set_optional_arg(nigh_text, knee_nigh)

    # WHEN
    atom_json = insert_factunit_atomunit.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_atomunit_get_from_json_ReturnsCorrectObj():
    # ESTABLISH
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    x_category = "bud_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    knee_open = 7
    knee_nigh = 13
    gen_atomunit = atomunit_shop(x_category, atom_insert())
    gen_atomunit.set_required_arg(road_text, ball_road)
    gen_atomunit.set_required_arg(base_text, knee_road)
    gen_atomunit.set_optional_arg(open_text, knee_open)
    gen_atomunit.set_optional_arg(nigh_text, knee_nigh)
    atom_json = gen_atomunit.get_json()

    # WHEN
    json_atomunit = atomunit_get_from_json(atom_json)

    # THEN
    assert json_atomunit.category == gen_atomunit.category
    assert json_atomunit.crud_text == gen_atomunit.crud_text
    assert json_atomunit.required_args == gen_atomunit.required_args
    assert json_atomunit.optional_args == gen_atomunit.optional_args
    assert json_atomunit == gen_atomunit
