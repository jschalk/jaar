from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import road_str, type_AcctID_str, type_GroupID_str
from src.f08_filter.filter import (
    filterunit_shop,
    default_unknown_word,
    get_filterunit_from_dict,
    get_filterunit_from_json,
)
from src.f08_filter.examples.example_filters import (
    get_clean_roadunit_bridgeunit,
    get_swim_groupid_bridgeunit,
    get_suita_acctid_bridgeunit,
    get_slash_roadunit_bridgeunit,
    get_slash_groupid_bridgeunit,
    get_slash_acctid_bridgeunit,
)


def test_FilterUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_filterunit = filterunit_shop(sue_str)

    # WHEN
    sue_dict = sue_filterunit.get_dict()

    # THEN
    assert sue_dict
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("eon_id") == sue_filterunit.eon_id
    assert sue_dict.get("otx_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("inx_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("unknown_word") == default_unknown_word()
    assert sue_dict.get("bridgeunits")
    x_bridgeunits = sue_dict.get("bridgeunits")
    assert len(x_bridgeunits) == 3
    assert set(x_bridgeunits.keys()) == {
        type_AcctID_str(),
        type_GroupID_str(),
        road_str(),
    }
    acct_id_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_filterunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_filterunit.get_bridgeunit(road_str())
    assert x_bridgeunits.get(type_AcctID_str()) == acct_id_bridgeunit.get_dict()
    assert x_bridgeunits.get(type_GroupID_str()) == group_id_bridgeunit.get_dict()
    assert x_bridgeunits.get(road_str()) == road_bridgeunit.get_dict()


def test_FilterUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_filterunit = filterunit_shop(
        sue_str, 0, slash_otx_road_delimiter, colon_inx_road_delimiter, x_unknown_word
    )
    sue_filterunit.set_bridgeunit(get_slash_roadunit_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_groupid_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_acctid_bridgeunit())

    # WHEN
    sue_dict = sue_filterunit.get_dict()

    # THEN
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("otx_road_delimiter") == slash_otx_road_delimiter
    assert sue_dict.get("inx_road_delimiter") == colon_inx_road_delimiter
    assert sue_dict.get("unknown_word") == x_unknown_word
    assert sue_dict.get("bridgeunits")
    x_bridgeunits = sue_dict.get("bridgeunits")
    assert len(x_bridgeunits) == 3
    acct_id_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_filterunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_filterunit.get_bridgeunit(road_str())
    assert acct_id_bridgeunit.get_dict() == get_slash_acctid_bridgeunit().get_dict()
    assert group_id_bridgeunit.get_dict() == get_slash_groupid_bridgeunit().get_dict()
    assert road_bridgeunit.get_dict() == get_slash_roadunit_bridgeunit().get_dict()


def test_FilterUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_filterunit = filterunit_shop(sue_str)
    sue_filterunit.set_bridgeunit(get_clean_roadunit_bridgeunit())
    sue_filterunit.set_bridgeunit(get_swim_groupid_bridgeunit())
    sue_filterunit.set_bridgeunit(get_suita_acctid_bridgeunit())

    # WHEN
    sue_json = sue_filterunit.get_json()

    # THEN
    assert sue_json.find("bridgeunits") == 5
    assert sue_json.find("otx_road_delimiter") == 158


def test_get_filterunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_eon_id = 77
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_filterunit = filterunit_shop(
        sue_str,
        sue_eon_id,
        slash_otx_road_delimiter,
        colon_inx_road_delimiter,
        x_unknown_word,
    )
    sue_filterunit.set_bridgeunit(get_slash_roadunit_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_groupid_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_acctid_bridgeunit())

    # WHEN
    gen_filterunit = get_filterunit_from_dict(sue_filterunit.get_dict())

    # THEN
    assert gen_filterunit
    assert gen_filterunit.face_id == sue_str
    assert gen_filterunit.eon_id == sue_eon_id
    assert gen_filterunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_filterunit.inx_road_delimiter == colon_inx_road_delimiter
    assert gen_filterunit.unknown_word == x_unknown_word
    x_bridgeunits = gen_filterunit.bridgeunits
    assert len(x_bridgeunits) == 3
    acct_id_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_filterunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_filterunit.get_bridgeunit(road_str())
    assert acct_id_bridgeunit.get_dict() == get_slash_acctid_bridgeunit().get_dict()
    assert group_id_bridgeunit.get_dict() == get_slash_groupid_bridgeunit().get_dict()
    assert road_bridgeunit.get_dict() == get_slash_roadunit_bridgeunit().get_dict()


def test_get_filterunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_eon_id = 77
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_filterunit = filterunit_shop(
        sue_str,
        sue_eon_id,
        slash_otx_road_delimiter,
        colon_inx_road_delimiter,
        x_unknown_word,
    )
    sue_filterunit.set_bridgeunit(get_slash_roadunit_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_groupid_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_acctid_bridgeunit())

    # WHEN
    gen_filterunit = get_filterunit_from_json(sue_filterunit.get_json())

    # THEN
    assert gen_filterunit
    assert gen_filterunit.face_id == sue_str
    assert gen_filterunit.eon_id == sue_eon_id
    assert gen_filterunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_filterunit.inx_road_delimiter == colon_inx_road_delimiter
    assert gen_filterunit.unknown_word == x_unknown_word
    x_bridgeunits = gen_filterunit.bridgeunits
    assert len(x_bridgeunits) == 3
    acct_id_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_filterunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_filterunit.get_bridgeunit(road_str())
    assert acct_id_bridgeunit.get_dict() == get_slash_acctid_bridgeunit().get_dict()
    assert group_id_bridgeunit.get_dict() == get_slash_groupid_bridgeunit().get_dict()
    assert road_bridgeunit.get_dict() == get_slash_roadunit_bridgeunit().get_dict()
