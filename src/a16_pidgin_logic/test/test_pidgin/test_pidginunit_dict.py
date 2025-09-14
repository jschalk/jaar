from src.a01_rope_logic.rope import default_knot_if_None
from src.a16_pidgin_logic._ref.a16_terms import (
    event_int_str,
    face_name_str,
    inx_knot_str,
    otx_knot_str,
    unknown_str_str,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_str_if_None
from src.a16_pidgin_logic.pidgin_main import (
    get_pidginunit_from_dict,
    get_pidginunit_from_json,
    pidginunit_shop,
)
from src.a16_pidgin_logic.test._util.example_pidgins import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_slash_labelmap,
    get_slash_namemap,
    get_slash_ropemap,
    get_slash_titlemap,
    get_suita_namemap,
    get_swim_titlemap,
)


def _get_rid_of_pidgin_core_keys(map_dict: dict) -> dict:
    map_dict.pop(event_int_str())
    map_dict.pop(face_name_str())
    map_dict.pop(otx_knot_str())
    map_dict.pop(inx_knot_str())
    map_dict.pop(unknown_str_str())
    return map_dict


def test_PidginUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)

    # WHEN
    sue_dict = sue_pidginunit.to_dict()

    # THEN
    print(sue_dict)
    assert sue_dict
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(event_int_str()) == sue_pidginunit.event_int
    assert sue_dict.get(otx_knot_str()) == default_knot_if_None()
    assert sue_dict.get(inx_knot_str()) == default_knot_if_None()
    assert sue_dict.get(unknown_str_str()) == default_unknown_str_if_None()
    sue_namemap = sue_pidginunit.namemap.to_dict()
    sue_titlemap = sue_pidginunit.titlemap.to_dict()
    sue_labelmap = sue_pidginunit.labelmap.to_dict()
    sue_ropemap = sue_pidginunit.ropemap.to_dict()
    assert sue_dict.get("namemap") == _get_rid_of_pidgin_core_keys(sue_namemap)
    assert sue_dict.get("titlemap") == _get_rid_of_pidgin_core_keys(sue_titlemap)
    assert sue_dict.get("labelmap") == _get_rid_of_pidgin_core_keys(sue_labelmap)
    assert sue_dict.get("ropemap") == _get_rid_of_pidgin_core_keys(sue_ropemap)


def test_PidginUnit_to_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str, 0, slash_otx_knot, colon_inx_knot, x_unknown_str
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    sue_pidginunit.set_titlemap(get_slash_titlemap())
    sue_pidginunit.set_labelmap(get_slash_labelmap())
    sue_pidginunit.set_ropemap(get_slash_ropemap())

    # WHEN
    sue_dict = sue_pidginunit.to_dict()

    # THEN
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(otx_knot_str()) == slash_otx_knot
    assert sue_dict.get(inx_knot_str()) == colon_inx_knot
    assert sue_dict.get(unknown_str_str()) == x_unknown_str
    sue_namemap = sue_pidginunit.namemap.to_dict()
    sue_titlemap = sue_pidginunit.titlemap.to_dict()
    sue_labelmap = sue_pidginunit.labelmap.to_dict()
    sue_ropemap = sue_pidginunit.ropemap.to_dict()
    assert sue_dict.get("namemap") == _get_rid_of_pidgin_core_keys(sue_namemap)
    assert sue_dict.get("titlemap") == _get_rid_of_pidgin_core_keys(sue_titlemap)
    assert sue_dict.get("labelmap") == _get_rid_of_pidgin_core_keys(sue_labelmap)
    assert sue_dict.get("ropemap") == _get_rid_of_pidgin_core_keys(sue_ropemap)


def test_PidginUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    sue_pidginunit.set_titlemap(get_swim_titlemap())
    sue_pidginunit.set_namemap(get_suita_namemap())
    sue_pidginunit.set_labelmap(get_clean_labelmap())
    sue_pidginunit.set_ropemap(get_clean_ropemap())

    # WHEN
    sue_json = sue_pidginunit.get_json()

    # THEN
    # print(f"{sue_json=}")
    assert sue_json.find("labelmap") == 64
    assert sue_json.find(otx_knot_str()) == 266


def test_get_pidginunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 7
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_int,
        slash_otx_knot,
        colon_inx_knot,
        x_unknown_str,
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    sue_pidginunit.set_labelmap(get_slash_labelmap())
    sue_pidginunit.set_ropemap(get_slash_ropemap())
    sue_pidginunit.set_titlemap(get_slash_titlemap())

    # WHEN
    gen_pidginunit = get_pidginunit_from_dict(sue_pidginunit.to_dict())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_name == sue_str
    assert gen_pidginunit.event_int == sue_event_int
    assert gen_pidginunit.otx_knot == slash_otx_knot
    assert gen_pidginunit.inx_knot == colon_inx_knot
    assert gen_pidginunit.unknown_str == x_unknown_str
    assert gen_pidginunit.namemap == get_slash_namemap()
    assert gen_pidginunit.ropemap == get_slash_ropemap()
    assert gen_pidginunit.titlemap == get_slash_titlemap()


def test_get_pidginunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 7
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_int,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
    )
    sue_pidginunit.set_titlemap(get_slash_titlemap())
    sue_pidginunit.set_namemap(get_slash_namemap())
    sue_pidginunit.set_ropemap(get_slash_ropemap())

    # WHEN
    gen_pidginunit = get_pidginunit_from_json(sue_pidginunit.get_json())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_name == sue_str
    assert gen_pidginunit.event_int == sue_event_int
    assert gen_pidginunit.otx_knot == slash_otx_knot
    assert gen_pidginunit.inx_knot == colon_inx_knot
    assert gen_pidginunit.unknown_str == x_unknown_str
    assert gen_pidginunit.namemap.to_dict() == get_slash_namemap().to_dict()
    assert gen_pidginunit.titlemap.to_dict() == get_slash_titlemap().to_dict()
    assert gen_pidginunit.ropemap.to_dict() == get_slash_ropemap().to_dict()
