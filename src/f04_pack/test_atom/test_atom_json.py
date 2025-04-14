from src.f01_word_logic.road import create_road
from src.f02_bud.bud_tool import bud_item_factunit_str
from src.f04_pack.atom_config import (
    jkeys_str,
    jvalues_str,
    dimen_str,
    crud_str,
    road_str,
    base_str,
)
from src.f04_pack.atom import (
    budatom_shop,
    atom_insert,
    get_from_json as budatom_get_from_json,
)
from src.f00_data_toolboxs.dict_toolbox import x_is_json


def test_BudAtom_get_dict_ReturnsObj():
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
    insert_factunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_factunit_budatom.set_jkey(road_str(), ball_road)
    insert_factunit_budatom.set_jkey(base_str(), knee_road)
    insert_factunit_budatom.set_jvalue("open", knee_open)
    insert_factunit_budatom.set_jvalue("nigh", knee_nigh)

    # WHEN
    atom_dict = insert_factunit_budatom.get_dict()

    # THEN
    assert atom_dict == {
        dimen_str(): x_dimen,
        crud_str(): atom_insert(),
        jkeys_str(): {road_str(): ball_road, base_str(): knee_road},
        jvalues_str(): {"open": knee_open, "nigh": knee_nigh},
    }


def test_BudAtom_get_json_ReturnsObj():
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
    insert_factunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_factunit_budatom.set_jkey(road_str, ball_road)
    insert_factunit_budatom.set_jkey(base_str(), knee_road)
    insert_factunit_budatom.set_jvalue(open_str, knee_open)
    insert_factunit_budatom.set_jvalue(nigh_str, knee_nigh)

    # WHEN
    atom_json = insert_factunit_budatom.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_budatom_get_from_json_ReturnsObj():
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
    gen_budatom = budatom_shop(x_dimen, atom_insert())
    gen_budatom.set_jkey(road_str, ball_road)
    gen_budatom.set_jkey(base_str(), knee_road)
    gen_budatom.set_jvalue(open_str, knee_open)
    gen_budatom.set_jvalue(nigh_str, knee_nigh)
    atom_json = gen_budatom.get_json()

    # WHEN
    json_budatom = budatom_get_from_json(atom_json)

    # THEN
    assert json_budatom.dimen == gen_budatom.dimen
    assert json_budatom.crud_str == gen_budatom.crud_str
    assert json_budatom.jkeys == gen_budatom.jkeys
    assert json_budatom.jvalues == gen_budatom.jvalues
    assert json_budatom == gen_budatom
