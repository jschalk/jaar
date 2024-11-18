from src.f01_road.road import default_wall_if_none
from src.f04_gift.atom_config import road_str, type_AcctID_str, type_GroupID_str
from src.f08_pidgin.pidgin import (
    pidginunit_shop,
    default_unknown_word,
    get_pidginunit_from_dict,
    get_pidginunit_from_json,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_clean_roadunit_bridgeunit,
    get_swim_groupid_bridgeunit,
    get_suita_acctid_bridgeunit,
    get_slash_roadunit_bridgeunit,
    get_slash_groupid_bridgeunit,
    get_slash_acctid_bridgeunit,
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
    assert sue_dict.get("bridgeunits")
    x_bridgeunits = sue_dict.get("bridgeunits")
    assert len(x_bridgeunits) == 3
    assert set(x_bridgeunits.keys()) == {
        type_AcctID_str(),
        type_GroupID_str(),
        road_str(),
    }
    acct_id_bridgeunit = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_pidginunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_pidginunit.get_bridgeunit(road_str())
    assert x_bridgeunits.get(type_AcctID_str()) == acct_id_bridgeunit.get_dict()
    assert x_bridgeunits.get(type_GroupID_str()) == group_id_bridgeunit.get_dict()
    assert x_bridgeunits.get(road_str()) == road_bridgeunit.get_dict()


def test_PidginUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    sue_pidginunit = pidginunit_shop(
        sue_str, 0, slash_otx_wall, colon_inx_wall, x_unknown_word
    )
    sue_pidginunit.set_bridgeunit(get_slash_roadunit_bridgeunit())
    sue_pidginunit.set_bridgeunit(get_slash_groupid_bridgeunit())
    sue_pidginunit.set_bridgeunit(get_slash_acctid_bridgeunit())

    # WHEN
    sue_dict = sue_pidginunit.get_dict()

    # THEN
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("otx_wall") == slash_otx_wall
    assert sue_dict.get("inx_wall") == colon_inx_wall
    assert sue_dict.get("unknown_word") == x_unknown_word
    assert sue_dict.get("bridgeunits")
    x_bridgeunits = sue_dict.get("bridgeunits")
    assert len(x_bridgeunits) == 3
    acct_id_bridgeunit = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_pidginunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_pidginunit.get_bridgeunit(road_str())
    assert acct_id_bridgeunit.get_dict() == get_slash_acctid_bridgeunit().get_dict()
    assert group_id_bridgeunit.get_dict() == get_slash_groupid_bridgeunit().get_dict()
    assert road_bridgeunit.get_dict() == get_slash_roadunit_bridgeunit().get_dict()


def test_PidginUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    sue_pidginunit.set_bridgeunit(get_clean_roadunit_bridgeunit())
    sue_pidginunit.set_bridgeunit(get_swim_groupid_bridgeunit())
    sue_pidginunit.set_bridgeunit(get_suita_acctid_bridgeunit())

    # WHEN
    sue_json = sue_pidginunit.get_json()

    # THEN
    assert sue_json.find("bridgeunits") == 5
    assert sue_json.find("otx_wall") == 244


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
    sue_pidginunit.set_bridgeunit(get_slash_roadunit_bridgeunit())
    sue_pidginunit.set_bridgeunit(get_slash_groupid_bridgeunit())
    sue_pidginunit.set_bridgeunit(get_slash_acctid_bridgeunit())

    # WHEN
    gen_pidginunit = get_pidginunit_from_dict(sue_pidginunit.get_dict())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_id == sue_str
    assert gen_pidginunit.event_id == sue_event_id
    assert gen_pidginunit.otx_wall == slash_otx_wall
    assert gen_pidginunit.inx_wall == colon_inx_wall
    assert gen_pidginunit.unknown_word == x_unknown_word
    x_bridgeunits = gen_pidginunit.bridgeunits
    assert len(x_bridgeunits) == 3
    acct_id_bridgeunit = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_pidginunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_pidginunit.get_bridgeunit(road_str())
    assert acct_id_bridgeunit.get_dict() == get_slash_acctid_bridgeunit().get_dict()
    assert group_id_bridgeunit.get_dict() == get_slash_groupid_bridgeunit().get_dict()
    assert road_bridgeunit.get_dict() == get_slash_roadunit_bridgeunit().get_dict()


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
    sue_pidginunit.set_bridgeunit(get_slash_roadunit_bridgeunit())
    sue_pidginunit.set_bridgeunit(get_slash_groupid_bridgeunit())
    sue_pidginunit.set_bridgeunit(get_slash_acctid_bridgeunit())

    # WHEN
    gen_pidginunit = get_pidginunit_from_json(sue_pidginunit.get_json())

    # THEN
    assert gen_pidginunit
    assert gen_pidginunit.face_id == sue_str
    assert gen_pidginunit.event_id == sue_event_id
    assert gen_pidginunit.otx_wall == slash_otx_wall
    assert gen_pidginunit.inx_wall == colon_inx_wall
    assert gen_pidginunit.unknown_word == x_unknown_word
    x_bridgeunits = gen_pidginunit.bridgeunits
    assert len(x_bridgeunits) == 3
    acct_id_bridgeunit = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_pidginunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_pidginunit.get_bridgeunit(road_str())
    assert acct_id_bridgeunit.get_dict() == get_slash_acctid_bridgeunit().get_dict()
    assert group_id_bridgeunit.get_dict() == get_slash_groupid_bridgeunit().get_dict()
    assert road_bridgeunit.get_dict() == get_slash_roadunit_bridgeunit().get_dict()
