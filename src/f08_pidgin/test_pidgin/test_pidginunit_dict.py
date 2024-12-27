from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f01_road.road import default_bridge_if_None
from src.f04_gift.atom_config import face_id_str
from src.f08_pidgin.pidgin_config import (
    event_id_str,
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
    get_clean_ideamap,
    get_swim_groupmap,
    get_slash_acctmap,
    get_slash_groupmap,
    get_slash_ideamap,
    get_slash_roadmap,
    get_suita_acctmap,
)


def test_PidginUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)

    # WHEN
    sue_dict = sue_pidginunit.get_dict()

    # THEN
    assert sue_dict
    assert sue_dict.get(face_id_str()) == sue_str
    assert sue_dict.get(event_id_str()) == sue_pidginunit.event_id
    assert sue_dict.get(otx_bridge_str()) == default_bridge_if_None()
    assert sue_dict.get(inx_bridge_str()) == default_bridge_if_None()
    assert sue_dict.get(unknown_word_str()) == default_unknown_word_if_None()
    assert sue_dict.get("acctmap") == sue_pidginunit.acctmap.get_dict()
    assert sue_dict.get("groupmap") == sue_pidginunit.groupmap.get_dict()
    assert sue_dict.get("ideamap") == sue_pidginunit.ideamap.get_dict()
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
    sue_pidginunit.set_acctmap(get_slash_acctmap())
    sue_pidginunit.set_groupmap(get_slash_groupmap())
    sue_pidginunit.set_ideamap(get_slash_ideamap())
    sue_pidginunit.set_roadmap(get_slash_roadmap())

    # WHEN
    sue_dict = sue_pidginunit.get_dict()

    # THEN
    assert sue_dict.get(face_id_str()) == sue_str
    assert sue_dict.get(otx_bridge_str()) == slash_otx_bridge
    assert sue_dict.get(inx_bridge_str()) == colon_inx_bridge
    assert sue_dict.get(unknown_word_str()) == x_unknown_word
    assert sue_dict.get("acctmap") == sue_pidginunit.acctmap.get_dict()
    assert sue_dict.get("groupmap") == sue_pidginunit.groupmap.get_dict()
    assert sue_dict.get("ideamap") == sue_pidginunit.ideamap.get_dict()
    assert sue_dict.get("roadmap") == sue_pidginunit.roadmap.get_dict()


def test_PidginUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    sue_pidginunit.set_groupmap(get_swim_groupmap())
    sue_pidginunit.set_acctmap(get_suita_acctmap())
    sue_pidginunit.set_ideamap(get_clean_ideamap())
    sue_pidginunit.set_roadmap(get_clean_roadmap())

    # WHEN
    sue_json = sue_pidginunit.get_json()

    # THEN
    print(f"{sue_json=}")
    assert sue_json.find("ideamap") == 481
    assert sue_json.find(otx_bridge_str()) == 177


def test_get_pidginunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_id = 77
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_id,
        slash_otx_bridge,
        colon_inx_bridge,
        x_unknown_word,
    )
    sue_pidginunit.set_acctmap(get_slash_acctmap())
    sue_pidginunit.set_ideamap(get_slash_ideamap())
    sue_pidginunit.set_roadmap(get_slash_roadmap())
    sue_pidginunit.set_groupmap(get_slash_groupmap())

    # WHEN
    gen_pidginunit = get_pidginunit_from_dict(sue_pidginunit.get_dict())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_id == sue_str
    assert gen_pidginunit.event_id == sue_event_id
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.acctmap == get_slash_acctmap()
    assert gen_pidginunit.roadmap == get_slash_roadmap()
    assert gen_pidginunit.groupmap == get_slash_groupmap()


def test_get_pidginunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_id = 77
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_id,
        slash_otx_bridge,
        colon_inx_bridge,
        x_unknown_word,
    )
    sue_pidginunit.set_groupmap(get_slash_groupmap())
    sue_pidginunit.set_acctmap(get_slash_acctmap())
    sue_pidginunit.set_roadmap(get_slash_roadmap())

    # WHEN
    gen_pidginunit = get_pidginunit_from_json(sue_pidginunit.get_json())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_id == sue_str
    assert gen_pidginunit.event_id == sue_event_id
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.acctmap.get_dict() == get_slash_acctmap().get_dict()
    assert gen_pidginunit.groupmap.get_dict() == get_slash_groupmap().get_dict()
    assert gen_pidginunit.roadmap.get_dict() == get_slash_roadmap().get_dict()
