from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import (
    get_atom_args_python_types,
    road_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
)
from src.f09_filter.bridge import (
    BridgeUnit,
    bridgeunit_shop,
    bridgekind_shop,
    default_unknown_word,
    filterable_python_types,
    filterable_atom_args,
    get_bridgeunit_from_dict,
    get_bridgeunit_from_json,
)
from src.f09_filter.examples.examples_filter import (
    get_invalid_acctid_bridgekind,
    get_invalid_groupid_bridgekind,
    get_invalid_road_bridgekind,
    get_clean_roadunit_bridgekind,
    get_swim_groupid_bridgekind,
    get_suita_acctid_bridgekind,
    get_slash_roadunit_bridgekind,
    get_slash_groupid_bridgekind,
    get_slash_acctid_bridgekind,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_BridgeUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)

    # WHEN
    sue_dict = sue_bridgeunit.get_dict()

    # THEN
    assert sue_dict
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("src_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("dst_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("unknown_word") == default_unknown_word()
    assert sue_dict.get("bridgekinds")
    x_bridgekinds = sue_dict.get("bridgekinds")
    assert len(x_bridgekinds) == 3
    assert set(x_bridgekinds.keys()) == {
        type_AcctID_str(),
        type_GroupID_str(),
        road_str(),
    }
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert x_bridgekinds.get(type_AcctID_str()) == acct_id_bridgekind.get_dict()
    assert x_bridgekinds.get(type_GroupID_str()) == group_id_bridgekind.get_dict()
    assert x_bridgekinds.get(road_str()) == road_bridgekind.get_dict()


def test_BridgeUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_src_road_delimiter = "/"
    colon_dst_road_delimiter = ":"
    sue_bridgeunit = bridgeunit_shop(
        sue_str, slash_src_road_delimiter, colon_dst_road_delimiter, x_unknown_word
    )
    sue_bridgeunit.set_bridgekind(get_slash_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_groupid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())

    # WHEN
    sue_dict = sue_bridgeunit.get_dict()

    # THEN
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("src_road_delimiter") == slash_src_road_delimiter
    assert sue_dict.get("dst_road_delimiter") == colon_dst_road_delimiter
    assert sue_dict.get("unknown_word") == x_unknown_word
    assert sue_dict.get("bridgekinds")
    x_bridgekinds = sue_dict.get("bridgekinds")
    assert len(x_bridgekinds) == 3
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert acct_id_bridgekind.get_dict() == get_slash_acctid_bridgekind().get_dict()
    assert group_id_bridgekind.get_dict() == get_slash_groupid_bridgekind().get_dict()
    assert road_bridgekind.get_dict() == get_slash_roadunit_bridgekind().get_dict()


def test_BridgeUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    sue_bridgeunit.set_bridgekind(get_clean_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_swim_groupid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_suita_acctid_bridgekind())

    # WHEN
    sue_json = sue_bridgeunit.get_json()

    # THEN
    assert sue_json.find("bridgekinds") == 5
    assert sue_json.find("src_road_delimiter") == 164


def test_get_bridgeunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_src_road_delimiter = "/"
    colon_dst_road_delimiter = ":"
    sue_bridgeunit = bridgeunit_shop(
        sue_str, slash_src_road_delimiter, colon_dst_road_delimiter, x_unknown_word
    )
    sue_bridgeunit.set_bridgekind(get_slash_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_groupid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())

    # WHEN
    gen_bridgeunit = get_bridgeunit_from_dict(sue_bridgeunit.get_dict())

    # THEN
    assert gen_bridgeunit
    assert gen_bridgeunit.face_id == sue_str
    assert gen_bridgeunit.src_road_delimiter == slash_src_road_delimiter
    assert gen_bridgeunit.dst_road_delimiter == colon_dst_road_delimiter
    assert gen_bridgeunit.unknown_word == x_unknown_word
    x_bridgekinds = gen_bridgeunit.bridgekinds
    assert len(x_bridgekinds) == 3
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert acct_id_bridgekind.get_dict() == get_slash_acctid_bridgekind().get_dict()
    assert group_id_bridgekind.get_dict() == get_slash_groupid_bridgekind().get_dict()
    assert road_bridgekind.get_dict() == get_slash_roadunit_bridgekind().get_dict()


def test_get_bridgeunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_src_road_delimiter = "/"
    colon_dst_road_delimiter = ":"
    sue_bridgeunit = bridgeunit_shop(
        sue_str, slash_src_road_delimiter, colon_dst_road_delimiter, x_unknown_word
    )
    sue_bridgeunit.set_bridgekind(get_slash_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_groupid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())

    # WHEN
    gen_bridgeunit = get_bridgeunit_from_json(sue_bridgeunit.get_json())

    # THEN
    assert gen_bridgeunit
    assert gen_bridgeunit.face_id == sue_str
    assert gen_bridgeunit.src_road_delimiter == slash_src_road_delimiter
    assert gen_bridgeunit.dst_road_delimiter == colon_dst_road_delimiter
    assert gen_bridgeunit.unknown_word == x_unknown_word
    x_bridgekinds = gen_bridgeunit.bridgekinds
    assert len(x_bridgekinds) == 3
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert acct_id_bridgekind.get_dict() == get_slash_acctid_bridgekind().get_dict()
    assert group_id_bridgekind.get_dict() == get_slash_groupid_bridgekind().get_dict()
    assert road_bridgekind.get_dict() == get_slash_roadunit_bridgekind().get_dict()
