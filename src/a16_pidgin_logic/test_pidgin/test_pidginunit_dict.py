from src.a01_way_logic.way import default_bridge_if_None
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    otx_bridge_str,
    inx_bridge_str,
    unknown_term_str,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_term_if_None
from src.a16_pidgin_logic.pidgin import (
    pidginunit_shop,
    get_pidginunit_from_dict,
    get_pidginunit_from_json,
)
from src.a16_pidgin_logic._utils.example_pidgins import (
    get_clean_waymap,
    get_clean_tagmap,
    get_swim_labelmap,
    get_slash_namemap,
    get_slash_labelmap,
    get_slash_tagmap,
    get_slash_waymap,
    get_suita_namemap,
)


def _get_rid_of_pidgin_core_keys(map_dict: dict) -> dict:
    map_dict.pop(event_int_str())
    map_dict.pop(face_name_str())
    map_dict.pop(otx_bridge_str())
    map_dict.pop(inx_bridge_str())
    map_dict.pop(unknown_term_str())
    return map_dict


def test_PidginUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)

    # WHEN
    sue_dict = sue_pidginunit.get_dict()

    # THEN
    print(sue_dict)
    assert sue_dict
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(event_int_str()) == sue_pidginunit.event_int
    assert sue_dict.get(otx_bridge_str()) == default_bridge_if_None()
    assert sue_dict.get(inx_bridge_str()) == default_bridge_if_None()
    assert sue_dict.get(unknown_term_str()) == default_unknown_term_if_None()
    sue_namemap = sue_pidginunit.namemap.get_dict()
    sue_labelmap = sue_pidginunit.labelmap.get_dict()
    sue_tagmap = sue_pidginunit.tagmap.get_dict()
    sue_waymap = sue_pidginunit.waymap.get_dict()
    assert sue_dict.get("namemap") == _get_rid_of_pidgin_core_keys(sue_namemap)
    assert sue_dict.get("labelmap") == _get_rid_of_pidgin_core_keys(sue_labelmap)
    assert sue_dict.get("tagmap") == _get_rid_of_pidgin_core_keys(sue_tagmap)
    assert sue_dict.get("waymap") == _get_rid_of_pidgin_core_keys(sue_waymap)


def test_PidginUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str, 0, slash_otx_bridge, colon_inx_bridge, x_unknown_term
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    sue_pidginunit.set_labelmap(get_slash_labelmap())
    sue_pidginunit.set_tagmap(get_slash_tagmap())
    sue_pidginunit.set_waymap(get_slash_waymap())

    # WHEN
    sue_dict = sue_pidginunit.get_dict()

    # THEN
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(otx_bridge_str()) == slash_otx_bridge
    assert sue_dict.get(inx_bridge_str()) == colon_inx_bridge
    assert sue_dict.get(unknown_term_str()) == x_unknown_term
    sue_namemap = sue_pidginunit.namemap.get_dict()
    sue_labelmap = sue_pidginunit.labelmap.get_dict()
    sue_tagmap = sue_pidginunit.tagmap.get_dict()
    sue_waymap = sue_pidginunit.waymap.get_dict()
    assert sue_dict.get("namemap") == _get_rid_of_pidgin_core_keys(sue_namemap)
    assert sue_dict.get("labelmap") == _get_rid_of_pidgin_core_keys(sue_labelmap)
    assert sue_dict.get("tagmap") == _get_rid_of_pidgin_core_keys(sue_tagmap)
    assert sue_dict.get("waymap") == _get_rid_of_pidgin_core_keys(sue_waymap)


def test_PidginUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    sue_pidginunit.set_labelmap(get_swim_labelmap())
    sue_pidginunit.set_namemap(get_suita_namemap())
    sue_pidginunit.set_tagmap(get_clean_tagmap())
    sue_pidginunit.set_waymap(get_clean_waymap())

    # WHEN
    sue_json = sue_pidginunit.get_json()

    # THEN
    # print(f"{sue_json=}")
    assert sue_json.find("tagmap") == 290
    assert sue_json.find(otx_bridge_str()) == 269


def test_get_pidginunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 7
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_int,
        slash_otx_bridge,
        colon_inx_bridge,
        x_unknown_term,
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    sue_pidginunit.set_tagmap(get_slash_tagmap())
    sue_pidginunit.set_waymap(get_slash_waymap())
    sue_pidginunit.set_labelmap(get_slash_labelmap())

    # WHEN
    gen_pidginunit = get_pidginunit_from_dict(sue_pidginunit.get_dict())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_name == sue_str
    assert gen_pidginunit.event_int == sue_event_int
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    assert gen_pidginunit.unknown_term == x_unknown_term
    assert gen_pidginunit.namemap == get_slash_namemap()
    assert gen_pidginunit.waymap == get_slash_waymap()
    assert gen_pidginunit.labelmap == get_slash_labelmap()


def test_get_pidginunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 7
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_int,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
    )
    sue_pidginunit.set_labelmap(get_slash_labelmap())
    sue_pidginunit.set_namemap(get_slash_namemap())
    sue_pidginunit.set_waymap(get_slash_waymap())

    # WHEN
    gen_pidginunit = get_pidginunit_from_json(sue_pidginunit.get_json())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_name == sue_str
    assert gen_pidginunit.event_int == sue_event_int
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    assert gen_pidginunit.unknown_term == x_unknown_term
    assert gen_pidginunit.namemap.get_dict() == get_slash_namemap().get_dict()
    assert gen_pidginunit.labelmap.get_dict() == get_slash_labelmap().get_dict()
    assert gen_pidginunit.waymap.get_dict() == get_slash_waymap().get_dict()
