from src.f01_road.road import default_wall_if_none
from src.f04_gift.atom_config import road_str, type_AcctID_str, type_GroupID_str
from src.f08_pidgin.bridge import acctbridge_shop, groupbridge_shop, roadbridge_shop
from src.f08_pidgin.pidgin import (
    pidginunit_shop,
    default_unknown_word,
    get_pidginunit_from_dict,
    get_pidginunit_from_json,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_clean_roadbridge,
    get_clean_ideabridge,
    get_swim_groupbridge,
    get_slash_acctbridge,
    get_slash_groupbridge,
    get_slash_ideabridge,
    get_slash_roadbridge,
    get_suita_acctbridge,
)


def test_PidginUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)

    # WHEN
    sue_dict = sue_pidginunit.get_dict()

    # THEN
    assert sue_dict
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("event_id") == sue_pidginunit.event_id
    assert sue_dict.get("otx_wall") == default_wall_if_none()
    assert sue_dict.get("inx_wall") == default_wall_if_none()
    assert sue_dict.get("unknown_word") == default_unknown_word()
    assert sue_dict.get("acctbridge") == sue_pidginunit.acctbridge.get_dict()
    assert sue_dict.get("groupbridge") == sue_pidginunit.groupbridge.get_dict()
    assert sue_dict.get("ideabridge") == sue_pidginunit.ideabridge.get_dict()
    assert sue_dict.get("roadbridge") == sue_pidginunit.roadbridge.get_dict()


def test_PidginUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str, 0, slash_otx_wall, colon_inx_wall, x_unknown_word
    )
    sue_pidginunit.set_acctbridge(get_slash_acctbridge())
    sue_pidginunit.set_groupbridge(get_slash_groupbridge())
    sue_pidginunit.set_ideabridge(get_slash_ideabridge())
    sue_pidginunit.set_roadbridge(get_slash_roadbridge())

    # WHEN
    sue_dict = sue_pidginunit.get_dict()

    # THEN
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("otx_wall") == slash_otx_wall
    assert sue_dict.get("inx_wall") == colon_inx_wall
    assert sue_dict.get("unknown_word") == x_unknown_word
    assert sue_dict.get("acctbridge") == sue_pidginunit.acctbridge.get_dict()
    assert sue_dict.get("groupbridge") == sue_pidginunit.groupbridge.get_dict()
    assert sue_dict.get("ideabridge") == sue_pidginunit.ideabridge.get_dict()
    assert sue_dict.get("roadbridge") == sue_pidginunit.roadbridge.get_dict()


def test_PidginUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    sue_pidginunit.set_groupbridge(get_swim_groupbridge())
    sue_pidginunit.set_acctbridge(get_suita_acctbridge())
    sue_pidginunit.set_ideabridge(get_clean_ideabridge())
    sue_pidginunit.set_roadbridge(get_clean_roadbridge())

    # WHEN
    sue_json = sue_pidginunit.get_json()

    # THEN
    print(f"{sue_json=}")
    assert sue_json.find("ideabridge") == 441
    assert sue_json.find("otx_wall") == 159


def test_get_pidginunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_id = 77
    x_unknown_word = "UnknownAcctId"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_id,
        slash_otx_wall,
        colon_inx_wall,
        x_unknown_word,
    )
    sue_pidginunit.set_acctbridge(get_slash_acctbridge())
    sue_pidginunit.set_roadbridge(get_slash_roadbridge())
    sue_pidginunit.set_ideabridge(get_slash_roadbridge())
    sue_pidginunit.set_groupbridge(get_slash_groupbridge())

    # WHEN
    gen_pidginunit = get_pidginunit_from_dict(sue_pidginunit.get_dict())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_id == sue_str
    assert gen_pidginunit.event_id == sue_event_id
    assert gen_pidginunit.otx_wall == slash_otx_wall
    assert gen_pidginunit.inx_wall == colon_inx_wall
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.acctbridge == get_slash_acctbridge()
    assert gen_pidginunit.roadbridge == get_slash_roadbridge()
    assert gen_pidginunit.groupbridge == get_slash_groupbridge()


def test_get_pidginunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_event_id = 77
    x_unknown_word = "UnknownAcctId"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str,
        sue_event_id,
        slash_otx_wall,
        colon_inx_wall,
        x_unknown_word,
    )
    sue_pidginunit.set_roadbridge(get_slash_roadbridge())
    sue_pidginunit.set_groupbridge(get_slash_groupbridge())
    sue_pidginunit.set_acctbridge(get_slash_acctbridge())

    # WHEN
    gen_pidginunit = get_pidginunit_from_json(sue_pidginunit.get_json())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_id == sue_str
    assert gen_pidginunit.event_id == sue_event_id
    assert gen_pidginunit.otx_wall == slash_otx_wall
    assert gen_pidginunit.inx_wall == colon_inx_wall
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.acctbridge.get_dict() == get_slash_acctbridge().get_dict()
    assert gen_pidginunit.groupbridge.get_dict() == get_slash_groupbridge().get_dict()
    assert gen_pidginunit.roadbridge.get_dict() == get_slash_roadbridge().get_dict()
