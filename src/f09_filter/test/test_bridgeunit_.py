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
)
from src.f09_filter.examples.example_bridges import (
    get_invalid_acctid_bridgekind,
    get_invalid_groupid_bridgekind,
    get_invalid_road_bridgekind,
    get_clean_roadunit_bridgekind,
    get_swim_groupid_bridgekind,
    get_suita_acctid_bridgekind,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy

# from src.f09_filter.examples.filter_env import get_test_filters_dir, env_dir_setup_cleanup

# The goal of the filter function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_filterable_python_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_filterable_python_types = filterable_python_types()

    # THEN
    assert len(x_filterable_python_types) == 4
    assert x_filterable_python_types == {
        type_AcctID_str(),
        type_GroupID_str(),
        type_RoadNode_str(),
        type_RoadUnit_str(),
    }
    print(f"{set(get_atom_args_python_types().values())=}")
    all_atom_python_types = set(get_atom_args_python_types().values())
    inter_x = set(all_atom_python_types).intersection(x_filterable_python_types)
    assert inter_x == x_filterable_python_types


def test_filterable_atom_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert len(filterable_atom_args()) == 11
    assert filterable_atom_args() == {
        "acct_id",
        "awardee_id",
        "road",
        "parent_road",
        "label",
        "healer_id",
        "need",
        "base",
        "pick",
        "group_id",
        "team_id",
    }

    print(f"{filterable_python_types()=}")
    all_python_types = set(get_atom_args_python_types().keys())
    assert filterable_atom_args().issubset(all_python_types)
    static_filterable_atom_args = {
        x_arg
        for x_arg, python_type in get_atom_args_python_types().items()
        if python_type in filterable_python_types()
    }
    assert filterable_atom_args() == static_filterable_atom_args


def test_BridgeUnit_Exists():
    # ESTABLISH
    x_bridgeunit = BridgeUnit()

    # WHEN / THEN
    assert not x_bridgeunit.bridgekinds
    assert not x_bridgeunit.unknown_word
    assert not x_bridgeunit.src_road_delimiter
    assert not x_bridgeunit.dst_road_delimiter
    assert not x_bridgeunit.face_id


def test_bridgeunit_shop_ReturnsObj_scenario0():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    sue_bridgeunit = bridgeunit_shop(sue_str)

    # THEN
    assert sue_bridgeunit.face_id == sue_str
    assert sue_bridgeunit.unknown_word == default_unknown_word()
    assert sue_bridgeunit.src_road_delimiter == default_road_delimiter_if_none()
    assert sue_bridgeunit.dst_road_delimiter == default_road_delimiter_if_none()

    acctid_bridgekind = sue_bridgeunit.bridgekinds.get(type_AcctID_str())
    assert acctid_bridgekind.unknown_word == default_unknown_word()
    assert acctid_bridgekind.src_road_delimiter == default_road_delimiter_if_none()
    assert acctid_bridgekind.dst_road_delimiter == default_road_delimiter_if_none()
    groupid_bridgekind = sue_bridgeunit.bridgekinds.get(type_GroupID_str())
    assert groupid_bridgekind.unknown_word == default_unknown_word()
    assert groupid_bridgekind.src_road_delimiter == default_road_delimiter_if_none()
    assert groupid_bridgekind.dst_road_delimiter == default_road_delimiter_if_none()
    road_bridgekind = sue_bridgeunit.bridgekinds.get(road_str())
    assert road_bridgekind.unknown_word == default_unknown_word()
    assert road_bridgekind.src_road_delimiter == default_road_delimiter_if_none()
    assert road_bridgekind.dst_road_delimiter == default_road_delimiter_if_none()


def test_bridgeunit_shop_ReturnsObj_scenario1():
    # ESTABLISH
    sue_str = "Sue"
    y_unknown_word = "UnknownAcctId"
    slash_src_road_delimiter = "/"
    colon_dst_road_delimiter = ":"

    # WHEN
    sue_bridgeunit = bridgeunit_shop(
        sue_str, slash_src_road_delimiter, colon_dst_road_delimiter, y_unknown_word
    )

    # THEN
    assert sue_bridgeunit.unknown_word == y_unknown_word
    assert sue_bridgeunit.src_road_delimiter == slash_src_road_delimiter
    assert sue_bridgeunit.dst_road_delimiter == colon_dst_road_delimiter

    assert len(sue_bridgeunit.bridgekinds) == 3
    acctid_bridgekind = sue_bridgeunit.bridgekinds.get(type_AcctID_str())
    assert acctid_bridgekind.unknown_word == y_unknown_word
    assert acctid_bridgekind.src_road_delimiter == slash_src_road_delimiter
    assert acctid_bridgekind.dst_road_delimiter == colon_dst_road_delimiter
    groupid_bridgekind = sue_bridgeunit.bridgekinds.get(type_GroupID_str())
    assert groupid_bridgekind.unknown_word == y_unknown_word
    assert groupid_bridgekind.src_road_delimiter == slash_src_road_delimiter
    assert groupid_bridgekind.dst_road_delimiter == colon_dst_road_delimiter
    road_bridgekind = sue_bridgeunit.bridgekinds.get(road_str())
    assert road_bridgekind.unknown_word == y_unknown_word
    assert road_bridgekind.src_road_delimiter == slash_src_road_delimiter
    assert road_bridgekind.dst_road_delimiter == colon_dst_road_delimiter


def test_BridgeUnit_set_bridgekind_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    acct_id_bridgekind = bridgekind_shop(type_AcctID_str(), x_face_id=sue_str)
    acct_id_bridgekind.set_src_to_dst("Bob", "Bob of Portland")
    assert sue_bridgeunit.bridgekinds.get(type_AcctID_str()) != acct_id_bridgekind

    # WHEN
    sue_bridgeunit.set_bridgekind(acct_id_bridgekind)

    # THEN
    assert sue_bridgeunit.bridgekinds.get(type_AcctID_str()) == acct_id_bridgekind


def test_BridgeUnit_set_bridgekind_SetsAttr_SpecialCase_RoadUnit():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    road_bridgekind = bridgekind_shop(type_RoadUnit_str(), x_face_id=sue_str)
    road_bridgekind.set_src_to_dst("Bob", "Bob of Portland")
    assert sue_bridgeunit.bridgekinds.get(road_str()) != road_bridgekind

    # WHEN
    sue_bridgeunit.set_bridgekind(road_bridgekind)

    # THEN
    assert sue_bridgeunit.bridgekinds.get(road_str()) == road_bridgekind


def test_BridgeUnit_set_bridgekind_SetsAttr_SpecialCase_RoadNode():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    roadnode_bridgekind = bridgekind_shop(type_RoadNode_str(), x_face_id=sue_str)
    roadnode_bridgekind.set_src_to_dst("Bob", "Bob of Portland")
    old_roadnode_bridgekind = copy_deepcopy(roadnode_bridgekind)
    assert sue_bridgeunit.bridgekinds.get(road_str()) != old_roadnode_bridgekind

    # WHEN
    sue_bridgeunit.set_bridgekind(roadnode_bridgekind)

    # THEN
    roadunit_bridgekind = bridgekind_shop(type_RoadUnit_str(), x_face_id=sue_str)
    roadunit_bridgekind.set_src_to_dst("Bob", "Bob of Portland")
    assert sue_bridgeunit.bridgekinds.get(road_str()) != old_roadnode_bridgekind
    assert sue_bridgeunit.bridgekinds.get(road_str()) == roadunit_bridgekind


def test_BridgeUnit_set_bridgekind_RaisesErrorIf_bridgekind_src_road_delimiter_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    slash_src_road_delimiter = "/"
    acct_id_bridgekind = bridgekind_shop(
        type_AcctID_str(),
        x_src_road_delimiter=slash_src_road_delimiter,
        x_face_id=sue_str,
    )
    assert sue_bridgeunit.src_road_delimiter != acct_id_bridgekind.src_road_delimiter
    assert sue_bridgeunit.bridgekinds.get(type_AcctID_str()) != acct_id_bridgekind

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bridgeunit.set_bridgekind(acct_id_bridgekind)
    exception_str = f"set_bridgekind Error: BrideUnit src_road_delimiter is '{sue_bridgeunit.src_road_delimiter}', BridgeKind is '{slash_src_road_delimiter}'."
    assert str(excinfo.value) == exception_str


def test_BridgeUnit_set_bridgekind_RaisesErrorIf_bridgekind_dst_road_delimiter_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    slash_dst_road_delimiter = "/"
    acct_id_bridgekind = bridgekind_shop(
        type_AcctID_str(),
        x_dst_road_delimiter=slash_dst_road_delimiter,
        x_face_id=sue_str,
    )
    assert sue_bridgeunit.dst_road_delimiter != acct_id_bridgekind.dst_road_delimiter
    assert sue_bridgeunit.bridgekinds.get(type_AcctID_str()) != acct_id_bridgekind

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bridgeunit.set_bridgekind(acct_id_bridgekind)
    exception_str = f"set_bridgekind Error: BrideUnit dst_road_delimiter is '{sue_bridgeunit.dst_road_delimiter}', BridgeKind is '{slash_dst_road_delimiter}'."
    assert str(excinfo.value) == exception_str


def test_BridgeUnit_set_bridgekind_RaisesErrorIf_bridgekind_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    acct_id_bridgekind = bridgekind_shop(
        type_AcctID_str(), x_unknown_word=casa_unknown_word, x_face_id=sue_str
    )
    assert sue_bridgeunit.unknown_word != acct_id_bridgekind.unknown_word
    assert sue_bridgeunit.bridgekinds.get(type_AcctID_str()) != acct_id_bridgekind

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bridgeunit.set_bridgekind(acct_id_bridgekind)
    exception_str = f"set_bridgekind Error: BrideUnit unknown_word is '{sue_bridgeunit.unknown_word}', BridgeKind is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_BridgeUnit_set_bridgekind_RaisesErrorIf_bridgekind_face_id_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    acct_id_bridgekind = bridgekind_shop(type_AcctID_str(), x_face_id=yao_str)
    assert sue_bridgeunit.face_id != acct_id_bridgekind.face_id
    assert sue_bridgeunit.bridgekinds.get(type_AcctID_str()) != acct_id_bridgekind

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bridgeunit.set_bridgekind(acct_id_bridgekind)
    exception_str = f"set_bridgekind Error: BrideUnit face_id is '{sue_bridgeunit.face_id}', BridgeKind is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_BridgeUnit_get_bridgekind_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    static_acct_id_bridgekind = bridgekind_shop(type_AcctID_str(), x_face_id=sue_str)
    static_acct_id_bridgekind.set_src_to_dst("Bob", "Bob of Portland")
    sue_bridgeunit.set_bridgekind(static_acct_id_bridgekind)

    # WHEN
    gen_acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())

    # THEN
    assert gen_acct_id_bridgekind == static_acct_id_bridgekind


def test_BridgeUnit_get_bridgekind_ReturnsObj_SpecialCase_RoadUnit():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    static_road_bridgekind = bridgekind_shop(type_RoadUnit_str(), x_face_id=sue_str)
    static_road_bridgekind.set_src_to_dst("Bob", "Bob of Portland")
    sue_bridgeunit.set_bridgekind(static_road_bridgekind)

    # WHEN
    gen_road_bridgekind = sue_bridgeunit.get_bridgekind(type_RoadUnit_str())

    # THEN
    assert gen_road_bridgekind == static_road_bridgekind


def test_BridgeUnit_is_valid_ReturnsObj():
    # ESTABLISH
    invalid_acctid_bridgekind = get_invalid_acctid_bridgekind()
    invalid_groupid_bridgekind = get_invalid_groupid_bridgekind()
    invalid_road_bridgekind = get_invalid_road_bridgekind()
    valid_acctid_bridgekind = get_suita_acctid_bridgekind()
    valid_groupid_bridgekind = get_swim_groupid_bridgekind()
    valid_road_bridgekind = get_clean_roadunit_bridgekind()
    assert valid_acctid_bridgekind.is_valid()
    assert valid_groupid_bridgekind.is_valid()
    assert valid_road_bridgekind.is_valid()
    assert invalid_road_bridgekind.is_valid() is False
    assert invalid_groupid_bridgekind.is_valid() is False
    assert invalid_acctid_bridgekind.is_valid() is False

    # WHEN / THEN
    sue_bridgeunit = bridgeunit_shop("Sue")
    assert sue_bridgeunit.is_valid()
    sue_bridgeunit.set_bridgekind(valid_acctid_bridgekind)
    sue_bridgeunit.set_bridgekind(valid_groupid_bridgekind)
    sue_bridgeunit.set_bridgekind(valid_road_bridgekind)
    assert sue_bridgeunit.is_valid()

    # WHEN / THEN
    sue_bridgeunit.set_bridgekind(invalid_acctid_bridgekind)
    assert sue_bridgeunit.is_valid() is False
    sue_bridgeunit.set_bridgekind(valid_acctid_bridgekind)
    assert sue_bridgeunit.is_valid()

    # WHEN / THEN
    sue_bridgeunit.set_bridgekind(invalid_groupid_bridgekind)
    assert sue_bridgeunit.is_valid() is False
    sue_bridgeunit.set_bridgekind(valid_groupid_bridgekind)
    assert sue_bridgeunit.is_valid()

    # WHEN / THEN
    sue_bridgeunit.set_bridgekind(invalid_road_bridgekind)
    assert sue_bridgeunit.is_valid() is False
    sue_bridgeunit.set_bridgekind(valid_road_bridgekind)
    assert sue_bridgeunit.is_valid()


def test_BridgeUnit_set_src_to_dst_SetsAttr_Scenario0_type_AcctID_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    apptid_bridgekind = zia_bridgeunit.get_bridgekind(type_AcctID_str())
    assert apptid_bridgekind.src_to_dst_exists(sue_src, sue_dst) is False

    # WHEN
    zia_bridgeunit.set_src_to_dst(type_AcctID_str(), sue_src, sue_dst)

    # THEN
    assert apptid_bridgekind.src_to_dst_exists(sue_src, sue_dst)


def test_BridgeUnit_set_src_to_dst_SetsAttr_Scenario1_type_RoadUnit_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    road_bridgekind = zia_bridgeunit.get_bridgekind(type_RoadUnit_str())
    assert road_bridgekind.src_to_dst_exists(sue_src, sue_dst) is False

    # WHEN
    zia_bridgeunit.set_src_to_dst(type_RoadUnit_str(), sue_src, sue_dst)

    # THEN
    assert road_bridgekind.src_to_dst_exists(sue_src, sue_dst)


def test_BridgeUnit_set_src_to_dst_SetsAttr_Scenario2_type_RoadNode_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    road_bridgekind = zia_bridgeunit.get_bridgekind(type_RoadNode_str())
    assert road_bridgekind.src_to_dst_exists(sue_src, sue_dst) is False

    # WHEN
    zia_bridgeunit.set_src_to_dst(type_RoadNode_str(), sue_src, sue_dst)

    # THEN
    assert road_bridgekind.src_to_dst_exists(sue_src, sue_dst)


def test_BridgeUnit_src_to_dst_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    road_type = type_RoadNode_str()
    assert zia_bridgeunit.src_to_dst_exists(road_type, sue_src, sue_dst) is False

    # WHEN
    zia_bridgeunit.set_src_to_dst(type_RoadNode_str(), sue_src, sue_dst)

    # THEN
    assert zia_bridgeunit.src_to_dst_exists(road_type, sue_src, sue_dst)


def test_BridgeUnit_get_dst_value_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    assert zia_bridgeunit._get_dst_value(type_AcctID_str(), sue_src) != sue_dst

    # WHEN
    zia_bridgeunit.set_src_to_dst(type_AcctID_str(), sue_src, sue_dst)

    # THEN
    assert zia_bridgeunit._get_dst_value(type_AcctID_str(), sue_src) == sue_dst


def test_BridgeUnit_del_src_to_dst_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    road_type = type_RoadNode_str()
    zia_bridgeunit.set_src_to_dst(type_RoadNode_str(), sue_src, sue_dst)
    zia_bridgeunit.set_src_to_dst(type_RoadNode_str(), zia_str, zia_str)
    assert zia_bridgeunit.src_to_dst_exists(road_type, sue_src, sue_dst)
    assert zia_bridgeunit.src_to_dst_exists(road_type, zia_str, zia_str)

    # WHEN
    zia_bridgeunit.del_src_to_dst(road_type, sue_src)

    # THEN
    assert zia_bridgeunit.src_to_dst_exists(road_type, sue_src, sue_dst) is False
    assert zia_bridgeunit.src_to_dst_exists(road_type, zia_str, zia_str)


def test_BridgeUnit_set_explicit_label_map_SetsAttr_Scenario0_type_AcctID_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    apptid_bridgekind = zia_bridgeunit.get_bridgekind(type_AcctID_str())
    assert apptid_bridgekind.explicit_label_map_exists(sue_src, sue_dst) is False

    # WHEN
    zia_bridgeunit.set_explicit_label_map(type_AcctID_str(), sue_src, sue_dst)

    # THEN
    assert apptid_bridgekind.explicit_label_map_exists(sue_src, sue_dst)


def test_BridgeUnit_set_explicit_label_map_SetsAttr_Scenario1_type_RoadUnit_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    road_bridgekind = zia_bridgeunit.get_bridgekind(type_RoadUnit_str())
    assert road_bridgekind.explicit_label_map_exists(sue_src, sue_dst) is False

    # WHEN
    zia_bridgeunit.set_explicit_label_map(type_RoadUnit_str(), sue_src, sue_dst)

    # THEN
    assert road_bridgekind.explicit_label_map_exists(sue_src, sue_dst)


def test_BridgeUnit_set_explicit_label_map_SetsAttr_Scenario2_type_RoadNode_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    road_bridgekind = zia_bridgeunit.get_bridgekind(type_RoadNode_str())
    assert road_bridgekind.explicit_label_map_exists(sue_src, sue_dst) is False

    # WHEN
    zia_bridgeunit.set_explicit_label_map(type_RoadNode_str(), sue_src, sue_dst)

    # THEN
    assert road_bridgekind.explicit_label_map_exists(sue_src, sue_dst)


def test_BridgeUnit_explicit_label_map_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    road_type = type_RoadNode_str()
    sue_exists = zia_bridgeunit.explicit_label_map_exists(road_type, sue_src, sue_dst)
    assert sue_exists is False

    # WHEN
    zia_bridgeunit.set_explicit_label_map(type_RoadNode_str(), sue_src, sue_dst)

    # THEN
    assert zia_bridgeunit.explicit_label_map_exists(road_type, sue_src, sue_dst)


def test_BridgeUnit_get_explicit_dst_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    assert zia_bridgeunit._get_explicit_dst_label(type_AcctID_str(), sue_src) != sue_dst

    # WHEN
    zia_bridgeunit.set_explicit_label_map(type_AcctID_str(), sue_src, sue_dst)

    # THEN
    assert zia_bridgeunit._get_explicit_dst_label(type_AcctID_str(), sue_src) == sue_dst


def test_BridgeUnit_del_explicit_label_map_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_src = "Sue"
    sue_dst = "Suita"
    zia_bridgeunit = bridgeunit_shop(zia_str)
    road_type = type_RoadNode_str()
    zia_bridgeunit.set_explicit_label_map(type_RoadNode_str(), sue_src, sue_dst)
    zia_bridgeunit.set_explicit_label_map(type_RoadNode_str(), zia_str, zia_str)
    assert zia_bridgeunit.explicit_label_map_exists(road_type, sue_src, sue_dst)
    assert zia_bridgeunit.explicit_label_map_exists(road_type, zia_str, zia_str)

    # WHEN
    zia_bridgeunit.del_explicit_label_map(road_type, sue_src)

    # THEN
    sue_exists = zia_bridgeunit.explicit_label_map_exists(road_type, sue_src, sue_dst)
    assert sue_exists is False
    assert zia_bridgeunit.explicit_label_map_exists(road_type, zia_str, zia_str)
