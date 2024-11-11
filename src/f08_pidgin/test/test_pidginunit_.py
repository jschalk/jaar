from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import (
    get_atom_args_obj_classs,
    road_str,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadNode_str,
    type_RoadUnit_str,
)
from src.f08_pidgin.pidgin import (
    PidginUnit,
    pidginunit_shop,
    bridgeunit_shop,
    default_unknown_word,
    pidginable_obj_classs,
    pidginable_atom_args,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_invalid_acctid_bridgeunit,
    get_invalid_groupid_bridgeunit,
    get_invalid_road_bridgeunit,
    get_clean_roadunit_bridgeunit,
    get_swim_groupid_bridgeunit,
    get_suita_acctid_bridgeunit,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy

# from otx.f08_pidgin.examples.pidgin_env import get_test_pidgins_dir, env_dir_setup_cleanup

# The goal of the pidgin function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_pidginable_obj_classs_ReturnsObj():
    # ESTABLISH / WHEN
    x_pidginable_obj_classs = pidginable_obj_classs()

    # THEN
    assert len(x_pidginable_obj_classs) == 4
    assert x_pidginable_obj_classs == {
        type_AcctID_str(),
        type_GroupID_str(),
        type_RoadNode_str(),
        type_RoadUnit_str(),
    }
    print(f"{set(get_atom_args_obj_classs().values())=}")
    all_atom_obj_classs = set(get_atom_args_obj_classs().values())
    inter_x = set(all_atom_obj_classs).intersection(x_pidginable_obj_classs)
    assert inter_x == x_pidginable_obj_classs


def test_pidginable_atom_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert len(pidginable_atom_args()) == 11
    assert pidginable_atom_args() == {
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

    print(f"{pidginable_obj_classs()=}")
    all_obj_classs = set(get_atom_args_obj_classs().keys())
    assert pidginable_atom_args().issubset(all_obj_classs)
    static_pidginable_atom_args = {
        x_arg
        for x_arg, obj_class in get_atom_args_obj_classs().items()
        if obj_class in pidginable_obj_classs()
    }
    assert pidginable_atom_args() == static_pidginable_atom_args


def test_PidginUnit_Exists():
    # ESTABLISH
    x_pidginunit = PidginUnit()

    # WHEN / THEN
    assert not x_pidginunit.eon_id
    assert not x_pidginunit.bridgeunits
    assert not x_pidginunit.unknown_word
    assert not x_pidginunit.otx_road_delimiter
    assert not x_pidginunit.inx_road_delimiter
    assert not x_pidginunit.face_id


def test_pidginunit_shop_ReturnsObj_scenario0():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    sue_pidginunit = pidginunit_shop(sue_str)

    # THEN
    assert sue_pidginunit.face_id == sue_str
    assert sue_pidginunit.eon_id == 0
    assert sue_pidginunit.unknown_word == default_unknown_word()
    assert sue_pidginunit.otx_road_delimiter == default_road_delimiter_if_none()
    assert sue_pidginunit.inx_road_delimiter == default_road_delimiter_if_none()

    acctid_bridgeunit = sue_pidginunit.bridgeunits.get(type_AcctID_str())
    assert acctid_bridgeunit.unknown_word == default_unknown_word()
    assert acctid_bridgeunit.otx_road_delimiter == default_road_delimiter_if_none()
    assert acctid_bridgeunit.inx_road_delimiter == default_road_delimiter_if_none()
    groupid_bridgeunit = sue_pidginunit.bridgeunits.get(type_GroupID_str())
    assert groupid_bridgeunit.unknown_word == default_unknown_word()
    assert groupid_bridgeunit.otx_road_delimiter == default_road_delimiter_if_none()
    assert groupid_bridgeunit.inx_road_delimiter == default_road_delimiter_if_none()
    road_bridgeunit = sue_pidginunit.bridgeunits.get(road_str())
    assert road_bridgeunit.unknown_word == default_unknown_word()
    assert road_bridgeunit.otx_road_delimiter == default_road_delimiter_if_none()
    assert road_bridgeunit.inx_road_delimiter == default_road_delimiter_if_none()


def test_pidginunit_shop_ReturnsObj_scenario1():
    # ESTABLISH
    sue_str = "Sue"
    five_eon_id = 5
    y_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"

    # WHEN
    sue_pidginunit = pidginunit_shop(
        sue_str,
        five_eon_id,
        slash_otx_road_delimiter,
        colon_inx_road_delimiter,
        y_unknown_word,
    )

    # THEN
    assert sue_pidginunit.eon_id == five_eon_id
    assert sue_pidginunit.unknown_word == y_unknown_word
    assert sue_pidginunit.otx_road_delimiter == slash_otx_road_delimiter
    assert sue_pidginunit.inx_road_delimiter == colon_inx_road_delimiter

    assert len(sue_pidginunit.bridgeunits) == 3
    acctid_bridgeunit = sue_pidginunit.bridgeunits.get(type_AcctID_str())
    assert acctid_bridgeunit.unknown_word == y_unknown_word
    assert acctid_bridgeunit.otx_road_delimiter == slash_otx_road_delimiter
    assert acctid_bridgeunit.inx_road_delimiter == colon_inx_road_delimiter
    assert acctid_bridgeunit.face_id == sue_str
    groupid_bridgeunit = sue_pidginunit.bridgeunits.get(type_GroupID_str())
    assert groupid_bridgeunit.unknown_word == y_unknown_word
    assert groupid_bridgeunit.otx_road_delimiter == slash_otx_road_delimiter
    assert groupid_bridgeunit.inx_road_delimiter == colon_inx_road_delimiter
    assert groupid_bridgeunit.face_id == sue_str
    road_bridgeunit = sue_pidginunit.bridgeunits.get(road_str())
    assert road_bridgeunit.unknown_word == y_unknown_word
    assert road_bridgeunit.otx_road_delimiter == slash_otx_road_delimiter
    assert road_bridgeunit.inx_road_delimiter == colon_inx_road_delimiter
    assert road_bridgeunit.face_id == sue_str


def test_PidginUnit_set_bridgeunit_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    acct_id_bridgeunit = bridgeunit_shop(type_AcctID_str(), x_face_id=sue_str)
    acct_id_bridgeunit.set_otx_to_inx("Bob", "Bob of Portland")
    assert sue_pidginunit.bridgeunits.get(type_AcctID_str()) != acct_id_bridgeunit

    # WHEN
    sue_pidginunit.set_bridgeunit(acct_id_bridgeunit)

    # THEN
    assert sue_pidginunit.bridgeunits.get(type_AcctID_str()) == acct_id_bridgeunit


def test_PidginUnit_set_bridgeunit_SetsAttr_SpecialCase_RoadUnit():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    road_bridgeunit = bridgeunit_shop(type_RoadUnit_str(), x_face_id=sue_str)
    road_bridgeunit.set_otx_to_inx("Bob", "Bob of Portland")
    assert sue_pidginunit.bridgeunits.get(road_str()) != road_bridgeunit

    # WHEN
    sue_pidginunit.set_bridgeunit(road_bridgeunit)

    # THEN
    assert sue_pidginunit.bridgeunits.get(road_str()) == road_bridgeunit


def test_PidginUnit_set_bridgeunit_SetsAttr_SpecialCase_RoadNode():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    roadnode_bridgeunit = bridgeunit_shop(type_RoadNode_str(), x_face_id=sue_str)
    roadnode_bridgeunit.set_otx_to_inx("Bob", "Bob of Portland")
    old_roadnode_bridgeunit = copy_deepcopy(roadnode_bridgeunit)
    assert sue_pidginunit.bridgeunits.get(road_str()) != old_roadnode_bridgeunit

    # WHEN
    sue_pidginunit.set_bridgeunit(roadnode_bridgeunit)

    # THEN
    roadunit_bridgeunit = bridgeunit_shop(type_RoadUnit_str(), x_face_id=sue_str)
    roadunit_bridgeunit.set_otx_to_inx("Bob", "Bob of Portland")
    assert sue_pidginunit.bridgeunits.get(road_str()) != old_roadnode_bridgeunit
    assert sue_pidginunit.bridgeunits.get(road_str()) == roadunit_bridgeunit


def test_PidginUnit_set_bridgeunit_RaisesErrorIf_bridgeunit_otx_road_delimiter_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_otx_road_delimiter = "/"
    acct_id_bridgeunit = bridgeunit_shop(
        type_AcctID_str(),
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_face_id=sue_str,
    )
    assert sue_pidginunit.otx_road_delimiter != acct_id_bridgeunit.otx_road_delimiter
    assert sue_pidginunit.bridgeunits.get(type_AcctID_str()) != acct_id_bridgeunit

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_bridgeunit(acct_id_bridgeunit)
    exception_str = f"set_bridgeunit Error: BridgeUnit otx_road_delimiter is '{sue_pidginunit.otx_road_delimiter}', BridgeUnit is '{slash_otx_road_delimiter}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_bridgeunit_RaisesErrorIf_bridgeunit_inx_road_delimiter_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    slash_inx_road_delimiter = "/"
    acct_id_bridgeunit = bridgeunit_shop(
        type_AcctID_str(),
        x_inx_road_delimiter=slash_inx_road_delimiter,
        x_face_id=sue_str,
    )
    assert sue_pidginunit.inx_road_delimiter != acct_id_bridgeunit.inx_road_delimiter
    assert sue_pidginunit.bridgeunits.get(type_AcctID_str()) != acct_id_bridgeunit

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_bridgeunit(acct_id_bridgeunit)
    exception_str = f"set_bridgeunit Error: BridgeUnit inx_road_delimiter is '{sue_pidginunit.inx_road_delimiter}', BridgeUnit is '{slash_inx_road_delimiter}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_bridgeunit_RaisesErrorIf_bridgeunit_unknown_word_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    casa_unknown_word = "Unknown_casa"
    acct_id_bridgeunit = bridgeunit_shop(
        type_AcctID_str(), x_unknown_word=casa_unknown_word, x_face_id=sue_str
    )
    assert sue_pidginunit.unknown_word != acct_id_bridgeunit.unknown_word
    assert sue_pidginunit.bridgeunits.get(type_AcctID_str()) != acct_id_bridgeunit

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_bridgeunit(acct_id_bridgeunit)
    exception_str = f"set_bridgeunit Error: BridgeUnit unknown_word is '{sue_pidginunit.unknown_word}', BridgeUnit is '{casa_unknown_word}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_set_bridgeunit_RaisesErrorIf_bridgeunit_face_id_IsNotSame():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    sue_pidginunit = pidginunit_shop(sue_str)
    acct_id_bridgeunit = bridgeunit_shop(type_AcctID_str(), x_face_id=yao_str)
    assert sue_pidginunit.face_id != acct_id_bridgeunit.face_id
    assert sue_pidginunit.bridgeunits.get(type_AcctID_str()) != acct_id_bridgeunit

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_pidginunit.set_bridgeunit(acct_id_bridgeunit)
    exception_str = f"set_bridgeunit Error: BridgeUnit face_id is '{sue_pidginunit.face_id}', BridgeUnit is '{yao_str}'."
    assert str(excinfo.value) == exception_str


def test_PidginUnit_get_bridgeunit_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_acct_id_bridgeunit = bridgeunit_shop(type_AcctID_str(), x_face_id=sue_str)
    static_acct_id_bridgeunit.set_otx_to_inx("Bob", "Bob of Portland")
    sue_pidginunit.set_bridgeunit(static_acct_id_bridgeunit)

    # WHEN
    gen_acct_id_bridgeunit = sue_pidginunit.get_bridgeunit(type_AcctID_str())

    # THEN
    assert gen_acct_id_bridgeunit == static_acct_id_bridgeunit


def test_PidginUnit_get_bridgeunit_ReturnsObj_SpecialCase_RoadUnit():
    # ESTABLISH
    sue_str = "Sue"
    sue_pidginunit = pidginunit_shop(sue_str)
    static_road_bridgeunit = bridgeunit_shop(type_RoadUnit_str(), x_face_id=sue_str)
    static_road_bridgeunit.set_otx_to_inx("Bob", "Bob of Portland")
    sue_pidginunit.set_bridgeunit(static_road_bridgeunit)

    # WHEN
    gen_road_bridgeunit = sue_pidginunit.get_bridgeunit(type_RoadUnit_str())

    # THEN
    assert gen_road_bridgeunit == static_road_bridgeunit


def test_PidginUnit_is_valid_ReturnsObj():
    # ESTABLISH
    invalid_acctid_bridgeunit = get_invalid_acctid_bridgeunit()
    invalid_groupid_bridgeunit = get_invalid_groupid_bridgeunit()
    invalid_road_bridgeunit = get_invalid_road_bridgeunit()
    valid_acctid_bridgeunit = get_suita_acctid_bridgeunit()
    valid_groupid_bridgeunit = get_swim_groupid_bridgeunit()
    valid_road_bridgeunit = get_clean_roadunit_bridgeunit()
    assert valid_acctid_bridgeunit.is_valid()
    assert valid_groupid_bridgeunit.is_valid()
    assert valid_road_bridgeunit.is_valid()
    assert invalid_road_bridgeunit.is_valid() is False
    assert invalid_groupid_bridgeunit.is_valid() is False
    assert invalid_acctid_bridgeunit.is_valid() is False

    # WHEN / THEN
    sue_pidginunit = pidginunit_shop("Sue")
    assert sue_pidginunit.is_valid()
    sue_pidginunit.set_bridgeunit(valid_acctid_bridgeunit)
    sue_pidginunit.set_bridgeunit(valid_groupid_bridgeunit)
    sue_pidginunit.set_bridgeunit(valid_road_bridgeunit)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_bridgeunit(invalid_acctid_bridgeunit)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_bridgeunit(valid_acctid_bridgeunit)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_bridgeunit(invalid_groupid_bridgeunit)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_bridgeunit(valid_groupid_bridgeunit)
    assert sue_pidginunit.is_valid()

    # WHEN / THEN
    sue_pidginunit.set_bridgeunit(invalid_road_bridgeunit)
    assert sue_pidginunit.is_valid() is False
    sue_pidginunit.set_bridgeunit(valid_road_bridgeunit)
    assert sue_pidginunit.is_valid()


def test_PidginUnit_set_otx_to_inx_SetsAttr_Scenario0_type_AcctID_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acctid_bridgeunit = zia_pidginunit.get_bridgeunit(type_AcctID_str())
    assert acctid_bridgeunit.otx_to_inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx_to_inx(type_AcctID_str(), sue_otx, sue_inx)

    # THEN
    assert acctid_bridgeunit.otx_to_inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx_to_inx_SetsAttr_Scenario1_type_RoadUnit_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_bridgeunit = zia_pidginunit.get_bridgeunit(type_RoadUnit_str())
    assert road_bridgeunit.otx_to_inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx_to_inx(type_RoadUnit_str(), sue_otx, sue_inx)

    # THEN
    assert road_bridgeunit.otx_to_inx_exists(sue_otx, sue_inx)


def test_PidginUnit_set_otx_to_inx_SetsAttr_Scenario2_type_RoadNode_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_bridgeunit = zia_pidginunit.get_bridgeunit(type_RoadNode_str())
    assert road_bridgeunit.otx_to_inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx_to_inx(type_RoadNode_str(), sue_otx, sue_inx)

    # THEN
    assert road_bridgeunit.otx_to_inx_exists(sue_otx, sue_inx)


def test_PidginUnit_otx_to_inx_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_type = type_RoadNode_str()
    assert zia_pidginunit.otx_to_inx_exists(road_type, sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_otx_to_inx(type_RoadNode_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.otx_to_inx_exists(road_type, sue_otx, sue_inx)


def test_PidginUnit_get_inx_value_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_inx_value(type_AcctID_str(), sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_otx_to_inx(type_AcctID_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_inx_value(type_AcctID_str(), sue_otx) == sue_inx


def test_PidginUnit_del_otx_to_inx_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_type = type_RoadNode_str()
    zia_pidginunit.set_otx_to_inx(type_RoadNode_str(), sue_otx, sue_inx)
    zia_pidginunit.set_otx_to_inx(type_RoadNode_str(), zia_str, zia_str)
    assert zia_pidginunit.otx_to_inx_exists(road_type, sue_otx, sue_inx)
    assert zia_pidginunit.otx_to_inx_exists(road_type, zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_otx_to_inx(road_type, sue_otx)

    # THEN
    assert zia_pidginunit.otx_to_inx_exists(road_type, sue_otx, sue_inx) is False
    assert zia_pidginunit.otx_to_inx_exists(road_type, zia_str, zia_str)


def test_PidginUnit_set_explicit_label_SetsAttr_Scenario0_type_AcctID_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    acctid_bridgeunit = zia_pidginunit.get_bridgeunit(type_AcctID_str())
    assert acctid_bridgeunit.explicit_label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_explicit_label(type_AcctID_str(), sue_otx, sue_inx)

    # THEN
    assert acctid_bridgeunit.explicit_label_exists(sue_otx, sue_inx)


def test_PidginUnit_set_explicit_label_SetsAttr_Scenario1_type_RoadUnit_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_bridgeunit = zia_pidginunit.get_bridgeunit(type_RoadUnit_str())
    assert road_bridgeunit.explicit_label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_explicit_label(type_RoadUnit_str(), sue_otx, sue_inx)

    # THEN
    assert road_bridgeunit.explicit_label_exists(sue_otx, sue_inx)


def test_PidginUnit_set_explicit_label_SetsAttr_Scenario2_type_RoadNode_str():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_bridgeunit = zia_pidginunit.get_bridgeunit(type_RoadNode_str())
    assert road_bridgeunit.explicit_label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_pidginunit.set_explicit_label(type_RoadNode_str(), sue_otx, sue_inx)

    # THEN
    assert road_bridgeunit.explicit_label_exists(sue_otx, sue_inx)


def test_PidginUnit_explicit_label_exists_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_type = type_RoadNode_str()
    sue_exists = zia_pidginunit.explicit_label_exists(road_type, sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_pidginunit.set_explicit_label(type_RoadNode_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit.explicit_label_exists(road_type, sue_otx, sue_inx)


def test_PidginUnit_get_explicit_inx_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    assert zia_pidginunit._get_explicit_inx_label(type_AcctID_str(), sue_otx) != sue_inx

    # WHEN
    zia_pidginunit.set_explicit_label(type_AcctID_str(), sue_otx, sue_inx)

    # THEN
    assert zia_pidginunit._get_explicit_inx_label(type_AcctID_str(), sue_otx) == sue_inx


def test_PidginUnit_del_explicit_label_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_pidginunit = pidginunit_shop(zia_str)
    road_type = type_RoadNode_str()
    zia_pidginunit.set_explicit_label(type_RoadNode_str(), sue_otx, sue_inx)
    zia_pidginunit.set_explicit_label(type_RoadNode_str(), zia_str, zia_str)
    assert zia_pidginunit.explicit_label_exists(road_type, sue_otx, sue_inx)
    assert zia_pidginunit.explicit_label_exists(road_type, zia_str, zia_str)

    # WHEN
    zia_pidginunit.del_explicit_label(road_type, sue_otx)

    # THEN
    sue_exists = zia_pidginunit.explicit_label_exists(road_type, sue_otx, sue_inx)
    assert sue_exists is False
    assert zia_pidginunit.explicit_label_exists(road_type, zia_str, zia_str)
