from src.ch02_rope_logic.rope import default_knot_if_None
from src.ch16_lire_logic._ref.ch16_keywords import (
    event_int_str,
    face_name_str,
    inx_knot_str,
    otx_knot_str,
    unknown_str_str,
)
from src.ch16_lire_logic.lire_config import default_unknown_str_if_None
from src.ch16_lire_logic.lire_main import (
    get_lireunit_from_dict,
    get_lireunit_from_json,
    lireunit_shop,
)
from src.ch16_lire_logic.test._util.example_lires import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_slash_labelmap,
    get_slash_namemap,
    get_slash_ropemap,
    get_slash_titlemap,
    get_suita_namemap,
    get_swim_titlemap,
)


def _get_rid_of_lire_core_keys(map_dict: dict) -> dict:
    map_dict.pop(event_int_str())
    map_dict.pop(face_name_str())
    map_dict.pop(otx_knot_str())
    map_dict.pop(inx_knot_str())
    map_dict.pop(unknown_str_str())
    return map_dict


def test_LireUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)

    # WHEN
    sue_dict = sue_lireunit.to_dict()

    # THEN
    print(sue_dict)
    assert sue_dict
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(event_int_str()) == sue_lireunit.event_int
    assert sue_dict.get(otx_knot_str()) == default_knot_if_None()
    assert sue_dict.get(inx_knot_str()) == default_knot_if_None()
    assert sue_dict.get(unknown_str_str()) == default_unknown_str_if_None()
    sue_namemap = sue_lireunit.namemap.to_dict()
    sue_titlemap = sue_lireunit.titlemap.to_dict()
    sue_labelmap = sue_lireunit.labelmap.to_dict()
    sue_ropemap = sue_lireunit.ropemap.to_dict()
    assert sue_dict.get("namemap") == _get_rid_of_lire_core_keys(sue_namemap)
    assert sue_dict.get("titlemap") == _get_rid_of_lire_core_keys(sue_titlemap)
    assert sue_dict.get("labelmap") == _get_rid_of_lire_core_keys(sue_labelmap)
    assert sue_dict.get("ropemap") == _get_rid_of_lire_core_keys(sue_ropemap)


def test_LireUnit_to_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_lireunit = lireunit_shop(
        sue_str, 0, slash_otx_knot, colon_inx_knot, x_unknown_str
    )
    sue_lireunit.set_namemap(get_slash_namemap())
    sue_lireunit.set_titlemap(get_slash_titlemap())
    sue_lireunit.set_labelmap(get_slash_labelmap())
    sue_lireunit.set_ropemap(get_slash_ropemap())

    # WHEN
    sue_dict = sue_lireunit.to_dict()

    # THEN
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(otx_knot_str()) == slash_otx_knot
    assert sue_dict.get(inx_knot_str()) == colon_inx_knot
    assert sue_dict.get(unknown_str_str()) == x_unknown_str
    sue_namemap = sue_lireunit.namemap.to_dict()
    sue_titlemap = sue_lireunit.titlemap.to_dict()
    sue_labelmap = sue_lireunit.labelmap.to_dict()
    sue_ropemap = sue_lireunit.ropemap.to_dict()
    assert sue_dict.get("namemap") == _get_rid_of_lire_core_keys(sue_namemap)
    assert sue_dict.get("titlemap") == _get_rid_of_lire_core_keys(sue_titlemap)
    assert sue_dict.get("labelmap") == _get_rid_of_lire_core_keys(sue_labelmap)
    assert sue_dict.get("ropemap") == _get_rid_of_lire_core_keys(sue_ropemap)


def test_LireUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_lireunit = lireunit_shop(sue_str)
    sue_lireunit.set_titlemap(get_swim_titlemap())
    sue_lireunit.set_namemap(get_suita_namemap())
    sue_lireunit.set_labelmap(get_clean_labelmap())
    sue_lireunit.set_ropemap(get_clean_ropemap())

    # WHEN
    sue_json = sue_lireunit.get_json()

    # THEN
    # print(f"{sue_json=}")
    assert sue_json.find("labelmap") == 64
    assert sue_json.find(otx_knot_str()) == 266


def test_get_lireunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 7
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_lireunit = lireunit_shop(
        sue_str,
        sue_event_int,
        slash_otx_knot,
        colon_inx_knot,
        x_unknown_str,
    )
    sue_lireunit.set_namemap(get_slash_namemap())
    sue_lireunit.set_labelmap(get_slash_labelmap())
    sue_lireunit.set_ropemap(get_slash_ropemap())
    sue_lireunit.set_titlemap(get_slash_titlemap())

    # WHEN
    gen_lireunit = get_lireunit_from_dict(sue_lireunit.to_dict())

    # THEN
    assert gen_lireunit
    assert gen_lireunit.face_name == sue_str
    assert gen_lireunit.event_int == sue_event_int
    assert gen_lireunit.otx_knot == slash_otx_knot
    assert gen_lireunit.inx_knot == colon_inx_knot
    assert gen_lireunit.unknown_str == x_unknown_str
    assert gen_lireunit.namemap == get_slash_namemap()
    assert gen_lireunit.ropemap == get_slash_ropemap()
    assert gen_lireunit.titlemap == get_slash_titlemap()


def test_get_lireunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 7
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_lireunit = lireunit_shop(
        sue_str,
        sue_event_int,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
    )
    sue_lireunit.set_titlemap(get_slash_titlemap())
    sue_lireunit.set_namemap(get_slash_namemap())
    sue_lireunit.set_ropemap(get_slash_ropemap())

    # WHEN
    gen_lireunit = get_lireunit_from_json(sue_lireunit.get_json())

    # THEN
    assert gen_lireunit
    assert gen_lireunit.face_name == sue_str
    assert gen_lireunit.event_int == sue_event_int
    assert gen_lireunit.otx_knot == slash_otx_knot
    assert gen_lireunit.inx_knot == colon_inx_knot
    assert gen_lireunit.unknown_str == x_unknown_str
    assert gen_lireunit.namemap.to_dict() == get_slash_namemap().to_dict()
    assert gen_lireunit.titlemap.to_dict() == get_slash_titlemap().to_dict()
    assert gen_lireunit.ropemap.to_dict() == get_slash_ropemap().to_dict()
