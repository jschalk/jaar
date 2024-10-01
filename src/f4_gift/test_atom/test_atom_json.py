from src.f1_road.road import create_road
from src.f2_bud.bud_tool import bud_idea_factunit_str
from src.f4_gift.atom_config import (
    required_args_str,
    optional_args_str,
    category_str,
    crud_str_str,
)
from src.f4_gift.atom import (
    atomunit_shop,
    atom_insert,
    get_from_json as atomunit_get_from_json,
)
from src.f0_instrument.dict_tool import x_is_json


def test_AtomUnit_get_dict_ReturnsCorrectObj():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    x_category = bud_idea_factunit_str()
    road_str = "road"
    base_str = "base"
    open_str = "open"
    nigh_str = "nigh"
    knee_open = 7
    knee_nigh = 13
    insert_factunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_factunit_atomunit.set_required_arg(road_str, ball_road)
    insert_factunit_atomunit.set_required_arg(base_str, knee_road)
    insert_factunit_atomunit.set_optional_arg(open_str, knee_open)
    insert_factunit_atomunit.set_optional_arg(nigh_str, knee_nigh)

    # WHEN
    atom_dict = insert_factunit_atomunit.get_dict()

    # THEN
    assert atom_dict == {
        category_str(): x_category,
        crud_str_str(): atom_insert(),
        required_args_str(): {road_str: ball_road, base_str: knee_road},
        optional_args_str(): {open_str: knee_open, nigh_str: knee_nigh},
    }


def test_AtomUnit_get_json_ReturnsCorrectObj():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    x_category = bud_idea_factunit_str()
    road_str = "road"
    base_str = "base"
    open_str = "open"
    nigh_str = "nigh"
    knee_open = 7
    knee_nigh = 13
    insert_factunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_factunit_atomunit.set_required_arg(road_str, ball_road)
    insert_factunit_atomunit.set_required_arg(base_str, knee_road)
    insert_factunit_atomunit.set_optional_arg(open_str, knee_open)
    insert_factunit_atomunit.set_optional_arg(nigh_str, knee_nigh)

    # WHEN
    atom_json = insert_factunit_atomunit.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_atomunit_get_from_json_ReturnsCorrectObj():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    x_category = bud_idea_factunit_str()
    road_str = "road"
    base_str = "base"
    open_str = "open"
    nigh_str = "nigh"
    knee_open = 7
    knee_nigh = 13
    gen_atomunit = atomunit_shop(x_category, atom_insert())
    gen_atomunit.set_required_arg(road_str, ball_road)
    gen_atomunit.set_required_arg(base_str, knee_road)
    gen_atomunit.set_optional_arg(open_str, knee_open)
    gen_atomunit.set_optional_arg(nigh_str, knee_nigh)
    atom_json = gen_atomunit.get_json()

    # WHEN
    json_atomunit = atomunit_get_from_json(atom_json)

    # THEN
    assert json_atomunit.category == gen_atomunit.category
    assert json_atomunit.crud_str == gen_atomunit.crud_str
    assert json_atomunit.required_args == gen_atomunit.required_args
    assert json_atomunit.optional_args == gen_atomunit.optional_args
    assert json_atomunit == gen_atomunit
