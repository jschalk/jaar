from src.ch02_rope_logic.rope import default_knot_if_None
from src.ch16_translate_logic._ref.ch16_keywords import (
    Ch16Keywords as wx,
    event_int_str,
    face_name_str,
)
from src.ch16_translate_logic.test._util.ch16_examples import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_slash_labelmap,
    get_slash_namemap,
    get_slash_ropemap,
    get_slash_titlemap,
    get_suita_namemap,
    get_swim_titlemap,
)
from src.ch16_translate_logic.translate_config import default_unknown_str_if_None
from src.ch16_translate_logic.translate_main import (
    get_translateunit_from_dict,
    get_translateunit_from_json,
    translateunit_shop,
)


def _get_rid_of_translate_core_keys(map_dict: dict) -> dict:
    map_dict.pop(event_int_str())
    map_dict.pop(face_name_str())
    map_dict.pop(wx.otx_knot)
    map_dict.pop(wx.inx_knot)
    map_dict.pop(wx.unknown_str)
    return map_dict


def test_TranslateUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)

    # WHEN
    sue_dict = sue_translateunit.to_dict()

    # THEN
    print(sue_dict)
    assert sue_dict
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(event_int_str()) == sue_translateunit.event_int
    assert sue_dict.get(wx.otx_knot) == default_knot_if_None()
    assert sue_dict.get(wx.inx_knot) == default_knot_if_None()
    assert sue_dict.get(wx.unknown_str) == default_unknown_str_if_None()
    sue_namemap = sue_translateunit.namemap.to_dict()
    sue_titlemap = sue_translateunit.titlemap.to_dict()
    sue_labelmap = sue_translateunit.labelmap.to_dict()
    sue_ropemap = sue_translateunit.ropemap.to_dict()
    assert sue_dict.get("namemap") == _get_rid_of_translate_core_keys(sue_namemap)
    assert sue_dict.get("titlemap") == _get_rid_of_translate_core_keys(sue_titlemap)
    assert sue_dict.get("labelmap") == _get_rid_of_translate_core_keys(sue_labelmap)
    assert sue_dict.get("ropemap") == _get_rid_of_translate_core_keys(sue_ropemap)


def test_TranslateUnit_to_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_translateunit = translateunit_shop(
        sue_str, 0, slash_otx_knot, colon_inx_knot, x_unknown_str
    )
    sue_translateunit.set_namemap(get_slash_namemap())
    sue_translateunit.set_titlemap(get_slash_titlemap())
    sue_translateunit.set_labelmap(get_slash_labelmap())
    sue_translateunit.set_ropemap(get_slash_ropemap())

    # WHEN
    sue_dict = sue_translateunit.to_dict()

    # THEN
    assert sue_dict.get(face_name_str()) == sue_str
    assert sue_dict.get(wx.otx_knot) == slash_otx_knot
    assert sue_dict.get(wx.inx_knot) == colon_inx_knot
    assert sue_dict.get(wx.unknown_str) == x_unknown_str
    sue_namemap = sue_translateunit.namemap.to_dict()
    sue_titlemap = sue_translateunit.titlemap.to_dict()
    sue_labelmap = sue_translateunit.labelmap.to_dict()
    sue_ropemap = sue_translateunit.ropemap.to_dict()
    assert sue_dict.get("namemap") == _get_rid_of_translate_core_keys(sue_namemap)
    assert sue_dict.get("titlemap") == _get_rid_of_translate_core_keys(sue_titlemap)
    assert sue_dict.get("labelmap") == _get_rid_of_translate_core_keys(sue_labelmap)
    assert sue_dict.get("ropemap") == _get_rid_of_translate_core_keys(sue_ropemap)


def test_TranslateUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_translateunit = translateunit_shop(sue_str)
    sue_translateunit.set_titlemap(get_swim_titlemap())
    sue_translateunit.set_namemap(get_suita_namemap())
    sue_translateunit.set_labelmap(get_clean_labelmap())
    sue_translateunit.set_ropemap(get_clean_ropemap())

    # WHEN
    sue_json = sue_translateunit.get_json()

    # THEN
    # print(f"{sue_json=}")
    assert sue_json.find("labelmap") == 64
    assert sue_json.find(wx.otx_knot) == 266


def test_get_translateunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 7
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_translateunit = translateunit_shop(
        sue_str,
        sue_event_int,
        slash_otx_knot,
        colon_inx_knot,
        x_unknown_str,
    )
    sue_translateunit.set_namemap(get_slash_namemap())
    sue_translateunit.set_labelmap(get_slash_labelmap())
    sue_translateunit.set_ropemap(get_slash_ropemap())
    sue_translateunit.set_titlemap(get_slash_titlemap())

    # WHEN
    gen_translateunit = get_translateunit_from_dict(sue_translateunit.to_dict())

    # THEN
    assert gen_translateunit
    assert gen_translateunit.face_name == sue_str
    assert gen_translateunit.event_int == sue_event_int
    assert gen_translateunit.otx_knot == slash_otx_knot
    assert gen_translateunit.inx_knot == colon_inx_knot
    assert gen_translateunit.unknown_str == x_unknown_str
    assert gen_translateunit.namemap == get_slash_namemap()
    assert gen_translateunit.ropemap == get_slash_ropemap()
    assert gen_translateunit.titlemap == get_slash_titlemap()


def test_get_translateunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_int = 7
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_translateunit = translateunit_shop(
        sue_str,
        sue_event_int,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
    )
    sue_translateunit.set_titlemap(get_slash_titlemap())
    sue_translateunit.set_namemap(get_slash_namemap())
    sue_translateunit.set_ropemap(get_slash_ropemap())

    # WHEN
    gen_translateunit = get_translateunit_from_json(sue_translateunit.get_json())

    # THEN
    assert gen_translateunit
    assert gen_translateunit.face_name == sue_str
    assert gen_translateunit.event_int == sue_event_int
    assert gen_translateunit.otx_knot == slash_otx_knot
    assert gen_translateunit.inx_knot == colon_inx_knot
    assert gen_translateunit.unknown_str == x_unknown_str
    assert gen_translateunit.namemap.to_dict() == get_slash_namemap().to_dict()
    assert gen_translateunit.titlemap.to_dict() == get_slash_titlemap().to_dict()
    assert gen_translateunit.ropemap.to_dict() == get_slash_ropemap().to_dict()
