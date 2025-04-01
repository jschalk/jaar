from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_bridge_if_None
from src.f04_vow.atom_config import face_name_str, event_int_str
from src.f08_pidgin.pidgin_config import (
    otx_bridge_str,
    inx_bridge_str,
    unknown_word_str,
)
from src.f08_pidgin.pidgin import (
    pidginunit_shop,
    get_pidginunit_from_dict,
    get_pidginunit_from_json,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_clean_roadmap,
    get_clean_titlemap,
    get_swim_labelmap,
    get_slash_namemap,
    get_slash_labelmap,
    get_slash_titlemap,
    get_slash_roadmap,
    get_suita_namemap,
)


def test_PidginUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)

    # WHEN
    sue_dict = sue_pidginunit.get_dict()

    # THEN
    assert sue_dict
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(event_int_str()) == sue_pidginunit.event_int
    assert sue_dict.get(otx_bridge_str()) == default_bridge_if_None()
    assert sue_dict.get(inx_bridge_str()) == default_bridge_if_None()
    assert sue_dict.get(unknown_word_str()) == default_unknown_word_if_None()
    assert sue_dict.get("namemap") == sue_pidginunit.namemap.get_dict()
    assert sue_dict.get("labelmap") == sue_pidginunit.labelmap.get_dict()
    assert sue_dict.get("titlemap") == sue_pidginunit.titlemap.get_dict()
    assert sue_dict.get("roadmap") == sue_pidginunit.roadmap.get_dict()


def test_PidginUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str, 0, slash_otx_bridge, colon_inx_bridge, x_unknown_word
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    sue_pidginunit.set_labelmap(get_slash_labelmap())
    sue_pidginunit.set_titlemap(get_slash_titlemap())
    sue_pidginunit.set_roadmap(get_slash_roadmap())

    # WHEN
    sue_dict = sue_pidginunit.get_dict()

    # THEN
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(otx_bridge_str()) == slash_otx_bridge
    assert sue_dict.get(inx_bridge_str()) == colon_inx_bridge
    assert sue_dict.get(unknown_word_str()) == x_unknown_word
    assert sue_dict.get("namemap") == sue_pidginunit.namemap.get_dict()
    assert sue_dict.get("labelmap") == sue_pidginunit.labelmap.get_dict()
    assert sue_dict.get("titlemap") == sue_pidginunit.titlemap.get_dict()
    assert sue_dict.get("roadmap") == sue_pidginunit.roadmap.get_dict()


def test_PidginUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    sue_pidginunit.set_labelmap(get_swim_labelmap())
    sue_pidginunit.set_namemap(get_suita_namemap())
    sue_pidginunit.set_titlemap(get_clean_titlemap())
    sue_pidginunit.set_roadmap(get_clean_roadmap())

    # WHEN
    sue_json = sue_pidginunit.get_json()

    # THEN
    # print(f"{sue_json=}")
    assert sue_json.find("titlemap") == 766
    assert sue_json.find(otx_bridge_str()) == 224


def test_get_pidginunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 77
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_int,
        slash_otx_bridge,
        colon_inx_bridge,
        x_unknown_word,
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    sue_pidginunit.set_titlemap(get_slash_titlemap())
    sue_pidginunit.set_roadmap(get_slash_roadmap())
    sue_pidginunit.set_labelmap(get_slash_labelmap())

    # WHEN
    gen_pidginunit = get_pidginunit_from_dict(sue_pidginunit.get_dict())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_name == sue_str
    assert gen_pidginunit.event_int == sue_event_int
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.namemap == get_slash_namemap()
    assert gen_pidginunit.roadmap == get_slash_roadmap()
    assert gen_pidginunit.labelmap == get_slash_labelmap()


def test_get_pidginunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 77
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_int,
        slash_otx_bridge,
        colon_inx_bridge,
        x_unknown_word,
    )
    sue_pidginunit.set_labelmap(get_slash_labelmap())
    sue_pidginunit.set_namemap(get_slash_namemap())
    sue_pidginunit.set_roadmap(get_slash_roadmap())

    # WHEN
    gen_pidginunit = get_pidginunit_from_json(sue_pidginunit.get_json())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_name == sue_str
    assert gen_pidginunit.event_int == sue_event_int
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.namemap.get_dict() == get_slash_namemap().get_dict()
    assert gen_pidginunit.labelmap.get_dict() == get_slash_labelmap().get_dict()
    assert gen_pidginunit.roadmap.get_dict() == get_slash_roadmap().get_dict()
