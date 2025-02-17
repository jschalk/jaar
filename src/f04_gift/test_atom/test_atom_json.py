from src.f01_road.road import create_road
from src.f02_bud.bud_tool import bud_item_factunit_str
from src.f04_gift.atom_config import (
    jkeys_str,
    jvalues_str,
    dimen_str,
    crud_str,
    road_str,
    base_str,
)
from src.f04_gift.atom import (
    atomunit_shop,
    atom_insert,
    get_from_json as atomunit_get_from_json,
)
from src.f00_instrument.dict_toolbox import x_is_json


def test_AtomUnit_get_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    x_dimen = bud_item_factunit_str()
    knee_open = 7
    knee_nigh = 13
    insert_factunit_atomunit = atomunit_shop(x_dimen, atom_insert())
    insert_factunit_atomunit.set_jkey(road_str(), ball_road)
    insert_factunit_atomunit.set_jkey(base_str(), knee_road)
    insert_factunit_atomunit.set_jvalue("open", knee_open)
    insert_factunit_atomunit.set_jvalue("nigh", knee_nigh)

    # WHEN
    atom_dict = insert_factunit_atomunit.get_dict()

    # THEN
    assert atom_dict == {
        dimen_str(): x_dimen,
        crud_str(): atom_insert(),
        jkeys_str(): {road_str(): ball_road, base_str(): knee_road},
        jvalues_str(): {"open": knee_open, "nigh": knee_nigh},
    }


def test_AtomUnit_get_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    x_dimen = bud_item_factunit_str()
    road_str = "road"
    open_str = "open"
    nigh_str = "nigh"
    knee_open = 7
    knee_nigh = 13
    insert_factunit_atomunit = atomunit_shop(x_dimen, atom_insert())
    insert_factunit_atomunit.set_jkey(road_str, ball_road)
    insert_factunit_atomunit.set_jkey(base_str(), knee_road)
    insert_factunit_atomunit.set_jvalue(open_str, knee_open)
    insert_factunit_atomunit.set_jvalue(nigh_str, knee_nigh)

    # WHEN
    atom_json = insert_factunit_atomunit.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_atomunit_get_from_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    x_dimen = bud_item_factunit_str()
    road_str = "road"
    open_str = "open"
    nigh_str = "nigh"
    knee_open = 7
    knee_nigh = 13
    gen_atomunit = atomunit_shop(x_dimen, atom_insert())
    gen_atomunit.set_jkey(road_str, ball_road)
    gen_atomunit.set_jkey(base_str(), knee_road)
    gen_atomunit.set_jvalue(open_str, knee_open)
    gen_atomunit.set_jvalue(nigh_str, knee_nigh)
    atom_json = gen_atomunit.get_json()

    # WHEN
    json_atomunit = atomunit_get_from_json(atom_json)

    # THEN
    assert json_atomunit.dimen == gen_atomunit.dimen
    assert json_atomunit.crud_str == gen_atomunit.crud_str
    assert json_atomunit.jkeys == gen_atomunit.jkeys
    assert json_atomunit.jvalues == gen_atomunit.jvalues
    assert json_atomunit == gen_atomunit
